import re
import json
import os
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
USERS_FILE = "users.json"

# ------------------ Users File ------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

# ------------------ Validation ------------------
def is_valid_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

def is_strong_password(password):
    return (
        len(password) >= 6 and
        any(c.isupper() for c in password) and
        any(c.islower() for c in password) and
        any(c.isdigit() for c in password)
    )

# ------------------ Password Hashing ------------------
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")

def check_password(password, hashed):
    return bcrypt.check_password_hash(hashed, password)
