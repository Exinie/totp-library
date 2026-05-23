from flask import Blueprint, render_template, request, redirect, url_for, session
from services.auth_service import register_user, authenticate_user
from models.user_model import get_user_by_id
from totp.totp_library import Totp


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template("register.html", error="Username and password required")

        ok, error = register_user(username, password)
        if not ok:
            return render_template("register.html", error=error)
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = authenticate_user(username, password)
        if not user:
            return render_template("login.html", error="Invalid credentials")

        if user["totp_enabled"]:
            session["pre_2fa_user_id"] = user["id"]
            session["pre_2fa_username"] = username
            return redirect(url_for("auth.totp_verify"))

        session["user_id"] = user["id"]
        session["username"] = username
        return redirect(url_for("dashboard.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/totp-verify", methods=["GET", "POST"])
def totp_verify():
    user_id = session.get("pre_2fa_user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = get_user_by_id(user_id)
    if not user or not user["totp_secret"]:
        session.pop("pre_2fa_user_id", None)
        session.pop("pre_2fa_username", None)
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if not code:
            return render_template("totp_verify.html", error="Code required")

        totp = Totp()
        if not totp.verify_digits(user["totp_secret"], code):
            return render_template("totp_verify.html", error="Invalid code")

        session.pop("pre_2fa_user_id", None)
        session["user_id"] = user["id"]
        session["username"] = session.pop("pre_2fa_username", user["username"])
        return redirect(url_for("dashboard.index"))

    return render_template("totp_verify.html")
