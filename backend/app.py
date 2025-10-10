from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from utils import prepare_features_from_raw
from auth_utils import (
    load_users, save_users, is_valid_email, is_strong_password, hash_password, check_password
)

app = Flask(__name__)
CORS(app)

# ---------------- ML Models ----------------
MODELS = {
    "lr": joblib.load("models/lr_model.joblib"),
    "rf": joblib.load("models/rf_model.joblib"),
    "dt": joblib.load("models/dt_model.joblib")
}

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

    return jsonify({"message": "Login successful!"})

# ---------------- Prediction Endpoint ----------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    model_name = (request.args.get("model") or "").lower()
    if model_name not in MODELS:
        return jsonify({"error": "Unknown model. Use model=lr or model=rf or model=dt"}), 400
    model = MODELS[model_name]

    required = [
        "Chest_Pain","Shortness_of_Breath","Fatigue","Palpitations","Dizziness",
        "Swelling","Pain_Arms_Jaw_Back","Cold_Sweats_Nausea","High_BP","High_Cholesterol",
        "Diabetes","Smoking","Obesity","Sedentary_Lifestyle","Family_History","Chronic_Stress",
        "Age"
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
        "model": "logistic_regression" if model_name=="lr" else "random_forest" if model_name=="rf" else "decision_tree",
        "input": data,
        "prediction": pred,
        "probability": round(prob, 2) if prob is not None else "N/A"
    })

# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
