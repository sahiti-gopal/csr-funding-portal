import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}?charset=utf8mb4"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False