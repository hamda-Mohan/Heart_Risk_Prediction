from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import secrets
from utils import prepare_features_from_raw
from auth_utils import (
    load_users, save_users, is_valid_email, is_strong_password, hash_password, check_password
)

app = Flask(__name__)

# ✅ Secure & full CORS config for frontend on port 3000
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

# ---------------- ML Models ----------------
MODELS = {
    "lr": joblib.load("models/lr_model.joblib"),  # Logistic Regression
    "rf": joblib.load("models/rf_model.joblib"),  # Random Forest
    "xgb": joblib.load("models/xgb_model.joblib"),  # XGBoost
}

session_tokens = {}  # token: email mapping

def require_login(request):
    token = request.headers.get("Authorization")
    if not token:
        return None
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    if token not in session_tokens:
        return None
    return session_tokens[token]

# ---------------- Auth Endpoints ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format."}), 400
    if not is_strong_password(password):
        return jsonify({"error": "Password must be 6+ chars, include upper, lower, number."}), 400

    users = load_users()
    if any(u["email"] == email for u in users):
        return jsonify({"error": "Email already registered."}), 400

    users.append({"email": email, "password": hash_password(password)})
    save_users(users)
    return jsonify({"message": "Registration successful!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    users = load_users()
    user = next((u for u in users if u["email"] == email), None)
    if not user or not check_password(password, user["password"]):
        return jsonify({"error": "Invalid email or password."}), 401

    token = secrets.token_hex(16)
    session_tokens[token] = email
    return jsonify({"message": "Login successful!", "token": token})

# ---------------- Logout Endpoint ----------------
@app.route("/logout", methods=["POST"])
def logout():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Authorization token required."}), 400
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    if token in session_tokens:
        del session_tokens[token]
        return jsonify({"message": "Logout successful!"})
    else:
        return jsonify({"error": "Invalid token."}), 400

# ---------------- Health Check ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Heart Risk Prediction API is running."})

# ---------------- Prediction Endpoint ----------------
@app.route("/predict", methods=["POST"])
def predict():
    user = require_login(request)
    if not user:
        return jsonify({"error": "Unauthorized. Please log in first."}), 401

    data = request.get_json()
    model_name = (request.args.get("model") or "").lower()
    if model_name not in MODELS:
        return jsonify({"error": "Unknown model. Use model=lr or model=rf or model=xgb"}), 400

    model = MODELS[model_name]

    required = [
        "Chest_Pain","Shortness_of_Breath","Fatigue","Palpitations","Dizziness",
        "Swelling","Pain_Arms_Jaw_Back","Cold_Sweats_Nausea","High_BP","High_Cholesterol",
        "Diabetes","Smoking","Obesity","Sedentary_Lifestyle","Family_History","Chronic_Stress","Age"
    ]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        x_new = prepare_features_from_raw(data)
        pred = int(model.predict(x_new)[0])
        prob = float(model.predict_proba(x_new)[0][1]) if hasattr(model, "predict_proba") else None
    except Exception as e:
        return jsonify({"error": f"Failed to prepare/predict: {e}"}), 500

    return jsonify({
        "model": "logistic_regression" if model_name == "lr" else
                  "random_forest" if model_name == "rf" else
                  "xgboost" if model_name == "xgb" else "unknown",
        "input": data,
        "prediction": pred,
        "probability": round(prob, 2) if prob is not None else "N/A"
    })

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

# ---------------- END ---------------- 

# To run the app:
# 1. Install dependencies: pip install flask flask-cors joblib scikit-learn xgboost bcrypt
# 2. Ensure models are in the 'models' directory.
# 3. Start the server: python backend/app.py    
# 4. Access API at http://localhost:8000
# ---------------- END ----------------



