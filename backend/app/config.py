import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _build_database_uri():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    name = os.getenv("DB_NAME")

    # Cloud Run talks to Cloud SQL over a unix socket mounted at
    # /cloudsql/<project>:<region>:<instance> (via --add-cloudsql-instances),
    # not a TCP host:port — there's no VPC networking to a host/port for it.
    cloud_sql_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    if cloud_sql_connection_name:
        socket_path = f"/cloudsql/{cloud_sql_connection_name}"
        return (
            f"mysql+pymysql://{user}:{password}@/{name}"
            f"?unix_socket={socket_path}&charset=utf8mb4"
        )

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    SQLALCHEMY_DATABASE_URI = _build_database_uri()

    SQLALCHEMY_TRACK_MODIFICATIONS = False