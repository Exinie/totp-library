import os
from flask import Flask, redirect, url_for

from init_db import init_db
from db import close_db
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.totp_setup_routes import totp_setup_bp


def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret")

	base_dir = os.path.dirname(os.path.abspath(__file__))
	app.config["DB_PATH"] = os.path.join(base_dir, "app.db")

	init_db(app.config["DB_PATH"])

	app.register_blueprint(auth_bp)
	app.register_blueprint(dashboard_bp)
	app.register_blueprint(totp_setup_bp)
	app.teardown_appcontext(close_db)

	@app.route("/")
	def index():
		return redirect(url_for("auth.login"))

	return app


if __name__ == "__main__":
	create_app().run(debug=True)
