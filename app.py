from flask import Flask, jsonify, request
from config import Config
from extensions import db, bcrypt, jwt, mail
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from routes.auth import auth
    from routes.upload import upload
    from routes.email import email_bp

    app.register_blueprint(auth)
    app.register_blueprint(upload)
    app.register_blueprint(email_bp)


    from models.user import User
    with app.app_context():
        db.create_all()

    # ⚙️ MIDDLEWARE

    @app.before_request
    def before_request():
        # runs before every request
        request.start_time = time.time()
        logger.info(f"→ {request.method} {request.path}")

    @app.after_request
    def after_request(response):
        # runs after every request
        duration = time.time() - request.start_time
        logger.info(f"← {response.status_code} | {duration:.3f}s")

        # add security headers to every response
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"

        return response

    @app.route("/")
    def home():
        return "Hello, Harsh!"

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Route not found!"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed!"}), 405

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error!"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
