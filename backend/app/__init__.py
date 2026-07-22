import os

from flask import Flask

from app.config import Config
from app.extensions import db, migrate, cors
from app.models import *
from app.routes.project_type_routes import project_type_bp
from app.routes.beneficiary_category_routes import beneficiary_category_bp
from app.routes.role_routes import role_bp
from app.routes.project_routes import project_bp
from app.routes.donor_routes import donor_bp
from app.routes.risk_routes import risk_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.alert_routes import alert_bp
from app.routes.payments import payments_bp
from app.routes.chat_routes import chat_bp
from app.routes.report_routes import report_bp
from app.routes.auth_routes import auth_bp
from app.routes.document_routes import document_bp

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    allowed_origins = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    ]

    cors.init_app(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
    )
   
    @app.get("/")
    def home():
        return {
            "message": "CSR Funding Portal API",
            "status": "running",
            "version": "1.0.0"
        }
    
    app.register_blueprint(project_type_bp, url_prefix="/api")
    app.register_blueprint(beneficiary_category_bp, url_prefix="/api")
    app.register_blueprint(role_bp, url_prefix="/api")
    app.register_blueprint(project_bp, url_prefix="/api")
    app.register_blueprint(donor_bp, url_prefix="/api")
    app.register_blueprint(risk_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(
        payments_bp,
        url_prefix="/api",
    )

    app.register_blueprint(alert_bp, url_prefix="/api")
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(report_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(document_bp, url_prefix="/api")

    if os.getenv("FLASK_ENV") != "production":
        print("\n========== REGISTERED ROUTES ==========")
        for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
            print(f"{rule.endpoint:35} {rule}")
        print("=======================================\n")

    return app