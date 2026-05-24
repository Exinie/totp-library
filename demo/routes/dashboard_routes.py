from flask import Blueprint, render_template, session, redirect, url_for, request, flash
import sys
import os
import secrets
import string
import qrcode
import io
import base64
import urllib.parse
from models.user_model import UserModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from totp.totp_library import Totp

dashboard_bp = Blueprint('dashboard', __name__)
user_model = UserModel()

@dashboard_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    return render_template('dashboard.html', username=session['username'])

@dashboard_bp.route('/options')
def options():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user = user_model.get_user_by_id(session['user_id'])
    yedek_kodlar = []
    if user[4] == 1:
        backup_data = user_model.get_backup_codes(user[0])
        if backup_data and backup_data[0]:
            yedek_kodlar = backup_data[0].split(',')

    return render_template('user_options.html', user=user, yedek_kodlar=yedek_kodlar)


@dashboard_bp.route('/setup_totp', methods=['GET', 'POST'])
def setup_totp():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user = user_model.get_user_by_id(session['user_id'])
    if user[4] == 1:
        flash("2AD zaten aktif")
        return redirect(url_for('dashboard.options'))

    totp = Totp()

    if request.method == 'POST':
        code = request.form['code']
        secret = session.get('temp_totp_secret')
        backup_codes_str = session.get('temp_backup_codes')
        
        if totp.verify_digits(secret, code):
            user_model.save_totp_details(session['user_id'], secret, backup_codes_str)
            session.pop('temp_totp_secret', None)
            session.pop('temp_backup_codes', None)
            flash("2AD başarıyla kuruldu")
            return redirect(url_for('dashboard.options'))
        else:
            flash("Girilen kod hatalı, tekrar deneyin")

    if 'temp_totp_secret' not in session:
        session['temp_totp_secret'] = totp.generate_secret_key()
        backups = [''.join(secrets.choice(string.digits) for _ in range(8)) for _ in range(10)]
        session['temp_backup_codes'] = ",".join(backups)
        
    secret = session['temp_totp_secret']
    backup_codes = session['temp_backup_codes'].split(',')
    
    # QR Kod oluşturma
    app_name = urllib.parse.quote("TOTP Demo")
    user_name = urllib.parse.quote(session.get('username', 'Kullanici'))
    totp_uri = f"otpauth://totp/{app_name}:{user_name}?secret={secret}&issuer={app_name}"
    
    img = qrcode.make(totp_uri)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    qr_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    
    return render_template('setup_totp.html', secret=secret, backup_codes=backup_codes, qr_base64=qr_base64)


@dashboard_bp.route('/disable_totp', methods=['POST'])
def disable_totp():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_model.disable_totp(session['user_id'])
    flash("2AD devre dışı bırakıldı")
    return redirect(url_for('dashboard.options'))
