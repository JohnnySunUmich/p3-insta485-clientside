"""Insta485 development configuration."""


from pathlib import Path


# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'


# Secret key for encrypting cookies
SECRET_KEY = b'\xb4e\x1e>\x1b\x0b\x04\xdf+\x80\xc2}\x02r;'
'\xb1$\x98\x0f\x85u\xea\xdbj'
SESSION_COOKIE_NAME = 'login'


# File Upload to var/uploads/
INSTA485_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = INSTA485_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# Database file is var/insta485.sqlite3
DATABASE_FILENAME = INSTA485_ROOT/'var'/'insta485.sqlite3'
