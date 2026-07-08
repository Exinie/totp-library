For Turkish, please visit [here](./README.md)

# TOTP Library

A zero-dependency Python library for generating and verifying Time-Based One-Time Passwords (TOTP) based on the RFC 6238 standard. The project includes a Flask demo application that presents the usage of the library.

This project was developed as part of the Directed Study course in the Information Security Technology Program.

# Requirements
- Python 3.x

Additionally for the demo application:
- Flask
- bcrypt
- qrcode
- Pillow

# Usage

```python
from totp.totp_library import Totp

totp = Totp()

# Generate a secret key
secret_key = totp.generate_secret_key()

# Generate a 6-digit code
code = totp.generate_digits(secret_key)

# Verify the code
is_valid = totp.verify_digits(secret_key, code)
```

# Demo Application Setup

1. Clone the repository:

```bash
git clone https://github.com/Exinie/totp-library.git
cd totp-library
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

```bash
# Windows:
.venv\Scripts\activate

# Linux / macOS:
. .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r demo/requirements.txt
```

4. Run the application:

```bash
cd demo
python app.py
```

The application will be available at `http://localhost:5000`. There is no default user, you need to create a new account at `/register`.
