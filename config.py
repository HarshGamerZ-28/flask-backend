from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD", ""))

class Config:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://root:{password}@localhost/flaskdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
```

Key change — `SQLALCHEMY_DATABASE_URI` now reads from `DATABASE_URL` environment variable first. Render will provide this automatically when you add a database.

---

### ✅ Step 4 — Push to GitHub

Make sure your project is on GitHub. Check your `.gitignore` has:
```
venv/
.env
__pycache__/
*.pyc