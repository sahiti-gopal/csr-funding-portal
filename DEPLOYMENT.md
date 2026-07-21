# Deployment Runbook

Target setup: **everything on one EC2 instance** — MySQL (Docker), the Flask API (gunicorn),
and the built React/Vite frontend, all fronted by a single nginx server.

This deploys the app **as it is today** — auth isn't wired into the router yet, so every
route is publicly reachable once this is live. That's fine for a staging/demo deploy; just
know it until the login page lands.

Everything living on one box keeps this simple in two ways:
- **MySQL never touches the internet.** It's bound to `127.0.0.1`, reachable only by the
  Flask process running right next to it. Nothing to open in the security group for it.
- **Frontend and API share one origin.** nginx serves the built frontend as static files and
  reverse-proxies `/api/*` to gunicorn on the same domain, so there's no cross-origin request
  in production at all — CORS stops being something you have to get right.

## 1. Launch the EC2 instance

1. AWS Console → EC2 → Launch instance. Ubuntu 22.04 LTS, `t3.small` is plenty for a portal
   this size. Create/reuse a key pair for SSH.
2. Security group — this is the entire exposure surface:
   | Port | Source | Purpose |
   |------|--------|---------|
   | 22 | your IP only | SSH |
   | 80 | 0.0.0.0/0 | HTTP (redirects to HTTPS) |
   | 443 | 0.0.0.0/0 | HTTPS — frontend + API, both served here |

   That's it. Nothing else is ever opened — not MySQL, not gunicorn's port — because nginx
   is the only thing the internet talks to, and it only listens on 80/443.
3. Allocate an Elastic IP and associate it with the instance, so the address doesn't change
   on reboot.
4. Point a domain (e.g. `yourdomain.com`) at the Elastic IP via an A record — needed for
   step 5's TLS cert (Let's Encrypt won't issue for a bare IP).

## 2. Install dependencies on the instance

SSH in, then:
```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip nginx certbot python3-certbot-nginx git

# Node, for building the frontend on the box (skip if you'd rather build locally and scp dist/ over)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

curl -fsSL https://get.docker.com | sh
sudo apt-get install -y docker-compose-plugin
sudo usermod -aG docker $USER   # log out/in once for this to take effect
```

## 3. MySQL (Docker, localhost-only)

```bash
git clone <your-repo-url> ~/csr-funding-portal
cd ~/csr-funding-portal/deploy
cp .env.example .env
# edit .env — long, random MYSQL_ROOT_PASSWORD and MYSQL_PASSWORD
docker compose -f docker-compose.mysql.yml up -d
```
`docker-compose.mysql.yml` binds to `127.0.0.1:3306` — this never touches the security group.

## 4. Flask API (gunicorn + systemd)

```bash
cd ~/csr-funding-portal/backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

cp .env.example .env
```
Edit `backend/.env`:
```
FLASK_APP=run.py
SECRET_KEY=<generate a real random value>
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=csr_funding_portal
DB_USER=csr_user
DB_PASSWORD=<same value you put in deploy/.env>
GEMINI_API_KEY=<your key>
ALLOWED_ORIGINS=https://yourdomain.com
```
(`ALLOWED_ORIGINS` is mostly a formality here since frontend and API share an origin — it
just matters if anything ever calls the API cross-origin.)

Apply migrations and (optionally) seed demo data:
```bash
.venv/bin/flask db upgrade
.venv/bin/python seed.py   # optional — wipes + reseeds demo data
```
Install the systemd service (already written for you at `deploy/csr-backend.service`,
assuming the repo lives at `/home/ubuntu/csr-funding-portal` — edit the paths in that file
first if yours differs):
```bash
sudo cp ~/csr-funding-portal/deploy/csr-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now csr-backend
sudo systemctl status csr-backend   # should be active (running)
```
Gunicorn binds to `127.0.0.1:8000` — internal only, nginx is what the internet reaches.

## 5. Frontend build

Since frontend and API now share an origin, point the build at a **relative** API path
instead of a full URL:
```bash
cd ~/csr-funding-portal/frontend
echo "VITE_API_URL=/api" > .env.production
npm install
npm run build
```
This produces `frontend/dist`, which is what nginx serves as static files in the next step.

## 6. nginx (single entry point + TLS)

```bash
sudo cp ~/csr-funding-portal/deploy/nginx-csr-app.conf /etc/nginx/sites-available/csr-app
# edit server_name and the root path in that file to match your domain/repo location
sudo ln -s /etc/nginx/sites-available/csr-app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default   # avoid the default site conflicting
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d yourdomain.com   # issues + wires up the HTTPS cert
```
`nginx-csr-app.conf` serves `frontend/dist` at `/`, proxies `/api/*` to gunicorn, and falls
back to `index.html` for any other path so React Router's client-side routes work on a
direct load or refresh.

## 7. Post-deploy checklist

- [ ] `curl https://yourdomain.com/api/` returns the `{"status": "running"}` JSON.
- [ ] Load `https://yourdomain.com/` in a browser, confirm the dashboard pulls real data
      (Network tab — requests should go to `/api/...` on the same origin, no CORS errors).
- [ ] Refresh the browser on a deep link like `/reports` directly — should load the app, not
      404 (confirms nginx's SPA fallback is working).
- [ ] `sudo systemctl status csr-backend` and `docker ps` both healthy after a reboot test.
- [ ] Rotate `SECRET_KEY` and both DB passwords away from anything used in local dev.

## Redeploying after code changes

```bash
cd ~/csr-funding-portal && git pull

# backend, if it changed
cd backend
.venv/bin/pip install -r requirements.txt   # if deps changed
.venv/bin/flask db upgrade                  # if there's a new migration
sudo systemctl restart csr-backend

# frontend, if it changed
cd ../frontend
npm run build
```
Frontend redeploys are just an `npm run build` — nginx serves straight from `dist/` on disk,
no separate deploy step or restart needed.

## Later: wiring up login

When the login page is ready, the router currently has no auth guard (see
`AuthContext`/`authService`/`useAuth` — built but unused). Wiring that in doesn't change
anything above; it's a frontend routing change plus whatever session/token verification you
add server-side. No redeploy-process changes needed, just a normal deploy of the updated
code through the same pipeline.
