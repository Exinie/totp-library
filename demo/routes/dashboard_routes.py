from flask import Blueprint, render_template, session
from services.auth_service import login_required


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    return render_template("dashboard.html", username=session.get("username"))
