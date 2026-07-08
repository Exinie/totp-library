For English, please visit [here](./README_EN.md)

# TOTP Library

RFC 6238 standardına dayanan, zamana dayalı tek kullanımlık parola (TOTP) üretimi ve doğrulaması için harici bağımlılığı olmayan bir Python kütüphanesi. Proje, kütüphanenin kullanımını gösteren bir Flask demo uygulaması içerir.

Bu proje, Bilişim Güvenliği Teknolojisi bölümü Yönlendirilmiş Çalışma dersi kapsamında geliştirilmiştir.

# Gereksinimler
- Python 3.x

Demo uygulama için ek olarak:
- Flask
- bcrypt
- qrcode
- Pillow

# Kullanım

```python
from totp.totp_library import Totp

totp = Totp()

# Gizli anahtar üret
secret_key = totp.generate_secret_key()

# 6 haneli kod üret
code = totp.generate_digits(secret_key)

# Kodu doğrula
is_valid = totp.verify_digits(secret_key, code)
```

# Demo Uygulamanın Kurulumu

1. Depoyu klonlayın:

```bash
git clone https://github.com/Exinie/totp-library.git
cd totp-library
```

2. Sanal ortam oluşturun ve etkinleştirin:

```bash
python -m venv .venv
```

```bash
# Windows:
.venv\Scripts\activate

# Linux / macOS:
. .venv/bin/activate
```

3. Bağımlılıkları yükleyin:

```bash
pip install -r demo/requirements.txt
```

4. Uygulamayı çalıştırın:

```bash
cd demo
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışır. Varsayılan kullanıcı bulunmamaktadır, `/register` sayfasından yeni bir hesap oluşturmanız gerekmektedir.
