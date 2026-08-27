import os

# Cloud Run injects PORT and requires the container to listen on it;
# docker-compose/EC2 don't set it, so fall back to the port baked into the
# image's EXPOSE/compose config.
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"


def when_ready(server):
    from run import ensure_seeded

    ensure_seeded()
