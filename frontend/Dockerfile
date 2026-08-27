FROM node:20-slim AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:1.27-alpine

# PORT: what nginx listens on (Cloud Run injects this; docker-compose
# doesn't, hence the default). BACKEND_ORIGIN: where /api gets proxied —
# override at `docker run`/Cloud Run deploy time to point at the backend's
# actual address (a compose service name locally, a Cloud Run URL in prod).
ENV PORT=80
ENV BACKEND_ORIGIN=http://backend:8000

COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
