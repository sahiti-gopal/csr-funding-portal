#!/bin/sh
set -e

# MySQL's official image briefly runs a temporary in-container server while
# initializing a fresh, empty data directory, then restarts for the real
# one. The compose healthcheck can observe that temporary server as
# "healthy" moments before it drops the connection, which can land right in
# the middle of `flask db upgrade` and leave a half-applied migration behind
# (tables created, but the revision never recorded). Wait for a connection
# that survives a couple of seconds before running migrations, and retry the
# upgrade itself in case one still lands in that window.

python - <<'PYEOF'
import os
import time

import pymysql

host = os.environ["DB_HOST"]
port = int(os.environ["DB_PORT"])
user = os.environ["DB_USER"]
password = os.environ["DB_PASSWORD"]

for attempt in range(30):
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, connect_timeout=5)
        conn.close()
        time.sleep(2)
        conn = pymysql.connect(host=host, port=port, user=user, password=password, connect_timeout=5)
        conn.close()
        break
    except Exception as exc:
        print(f"Waiting for MySQL ({attempt + 1}/30): {exc}")
        time.sleep(2)
else:
    raise SystemExit("MySQL never became reachable")
PYEOF

migrated=0
for attempt in 1 2 3; do
    if flask db upgrade; then
        migrated=1
        break
    fi
    echo "flask db upgrade failed (attempt $attempt/3), retrying..."
    sleep 3
done

if [ "$migrated" -ne 1 ]; then
    echo "flask db upgrade failed after 3 attempts, not starting the app."
    exit 1
fi

exec "$@"
