from urllib.parse import quote
from flask import Blueprint, render_template, request, session, redirect, url_for
from services.auth_service import login_required
from models.user_model import get_user_by_id, set_totp_secret, enable_totp
from totp.totp_library import Totp


totp_setup_bp = Blueprint("totp_setup", __name__)


@totp_setup_bp.route("/totp-setup", methods=["GET", "POST"])
@login_required
def index():
    user_id = session.get("user_id")
    user = get_user_by_id(user_id)
    if not user:
        return redirect(url_for("auth.login"))

    totp = Totp()
    secret = user["totp_secret"]
    if not secret:
        secret = totp.generate_secret_key()
        set_totp_secret(user_id, secret)

    label = quote(f"TOTP Demo:{user['username']}")
    issuer = quote("TOTP Demo")
    otp_uri = f"otpauth://totp/{label}?secret={secret}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={quote(otp_uri)}"

    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if not code:
            return render_template(
                "totp_setup.html",
                error="Code required",
                totp_enabled=user["totp_enabled"],
                secret=secret,
                otp_uri=otp_uri,
                qr_url=qr_url,
            )

        if not totp.verify_digits(secret, code):
            return render_template(
                "totp_setup.html",
                error="Invalid code",
                totp_enabled=user["totp_enabled"],
                secret=secret,
                otp_uri=otp_uri,
                qr_url=qr_url,
            )

        enable_totp(user_id)
        user = get_user_by_id(user_id)

    return render_template(
        "totp_setup.html",
        totp_enabled=user["totp_enabled"],
        secret=secret,
        otp_uri=otp_uri,
        qr_url=qr_url,
    )
