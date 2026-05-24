from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import bcrypt
import sys
import os
from models.user_model import UserModel

# totp_library.py dizinini system path'ine ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from totp.totp_library import Totp

auth_bp = Blueprint('auth', __name__)
user_model = UserModel()

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash("Kullanıcı adı ve şifre boş bırakılamaz")
            return render_template('register.html')
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        if user_model.create_user(username, hashed_password):
            flash("Kayıt başarılı, giriş yapabilirsiniz")
            return redirect(url_for('auth.login'))
        else:
            flash("Bu kullanıcı adı zaten alınmış")
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash("Kullanıcı adı ve şifre boş bırakılamaz")
            return render_template('login.html')
        
        user = user_model.get_user_by_username(username)
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            if user[4] == 1:  # totp_enabled
                session['pre_auth_user_id'] = user[0]
                session['pre_auth_username'] = user[1]
                return redirect(url_for('auth.verify_totp'))
            else:
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('dashboard.index'))
        else:
            flash("Geçersiz kullanıcı adı veya şifre")
            
    return render_template('login.html')

@auth_bp.route('/verify_totp', methods=['GET', 'POST'])
def verify_totp():
    if 'pre_auth_user_id' not in session:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        code = request.form['code']
        user_id = session['pre_auth_user_id']
        user = user_model.get_user_by_id(user_id)
        secret = user[3]
        
        totp = Totp()
        
        # Normal Kod
        if totp.verify_digits(secret, code):
            session['user_id'] = session['pre_auth_user_id']
            session['username'] = session['pre_auth_username']
            session.pop('pre_auth_user_id', None)
            session.pop('pre_auth_username', None)
            return redirect(url_for('dashboard.index'))
            
        # Yedek Kod
        backup_data = user_model.get_backup_codes(user_id)
        if backup_data:
            unused_codes_str = backup_data[0]
            used_codes_str = backup_data[1] if backup_data[1] else ""
            
            unused_codes = unused_codes_str.split(',') if unused_codes_str else []
            used_codes = used_codes_str.split(',') if used_codes_str else []
            
            if code in unused_codes:
                unused_codes.remove(code)
                used_codes.append(code)
                user_model.update_backup_codes(user_id, ",".join(unused_codes), ",".join(used_codes))
                
                session['user_id'] = session['pre_auth_user_id']
                session['username'] = session['pre_auth_username']
                session.pop('pre_auth_user_id', None)
                session.pop('pre_auth_username', None)
                flash("Yedek kod kullanılarak giriş yapıldı")
                return redirect(url_for('dashboard.index'))
                
        flash("Geçersiz veya kullanılmış kod")

    return render_template('verify_totp.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
