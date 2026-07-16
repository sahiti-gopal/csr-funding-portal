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

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
    app,
    resources={r"/api/*": {"origins": "http://localhost:5173"}}
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

    app.register_blueprint(
    alert_bp,
    url_prefix="/api"
)
    print("\n========== REGISTERED ROUTES ==========")

    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:35} {rule}")

    print("=======================================\n")
    return app