import json
import joblib
import pandas as pd

# ============================================================
# Load pre-fitted scaler and training column order
# ============================================================
TRAIN_COLUMNS = json.load(open("models/train_columns.json"))
SCALER = joblib.load("models/scaler.pkl")  # created in preprocess.py

# ============================================================
# Binary columns in dataset
# ============================================================
BINARY_COLS = [
    'Chest_Pain','Shortness_of_Breath','Fatigue','Palpitations','Dizziness',
    'Swelling','Pain_Arms_Jaw_Back','Cold_Sweats_Nausea','High_BP','High_Cholesterol',
    'Diabetes','Smoking','Obesity','Sedentary_Lifestyle','Family_History','Chronic_Stress'
]

# ============================================================
# Prepare raw user input into model-ready DataFrame
# ============================================================
def prepare_features_from_raw(record: dict) -> pd.DataFrame:
    """
    Convert raw input dictionary (symptoms + health features)
    into a properly ordered, scaled 1-row DataFrame matching training data.
    
    Args:
        record: dict containing user input, e.g. {"Chest_Pain": 1, "Age": 54, ...}
    
    Returns:
        pd.DataFrame: 1-row DataFrame ready for model prediction
    """
    # Initialize all expected columns with 0 (binary) or 0.0 (continuous)
    row = {col: (0 if col in BINARY_COLS else 0.0) for col in TRAIN_COLUMNS}

    # Fill in user-provided values
    for key, val in record.items():
        if key not in row:
            print(f"Warning: Input contains unknown column '{key}' – skipping.")
            continue
        if key in BINARY_COLS:
            row[key] = int(val)
        else:
            row[key] = float(val)


    # Create 1-row DataFrame with correct column order
    df_one = pd.DataFrame([row], columns=TRAIN_COLUMNS)
    # Scale Age column AFTER creating DataFrame
    if "Age" in df_one.columns:
        df_one["Age"] = SCALER.transform(df_one[["Age"]]).ravel()



    return df_one

# ============================================================
# Optional: check missing columns
# ============================================================
def check_missing_columns(df: pd.DataFrame):
    missing_cols = set(TRAIN_COLUMNS) - set(df.columns)
    if missing_cols:
        print(f"Warning: Missing columns in DataFrame: {missing_cols}")
    else:
        print("All columns present.")

# ============================================================
# Example usage (for testing)
# ============================================================
if __name__ == "__main__":
    example_input = {
        "Chest_Pain": 1,
        "Shortness_of_Breath": 1,
        "Fatigue": 0,
        "Palpitations": 1,
        "Dizziness": 0,
        "Swelling": 0,
        "Pain_Arms_Jaw_Back": 1,
        "Cold_Sweats_Nausea": 1,
        "High_BP": 1,
        "High_Cholesterol": 1,
        "Diabetes": 0,
        "Smoking": 0,
        "Obesity": 1,
        "Sedentary_Lifestyle": 1,
        "Family_History": 1,
        "Chronic_Stress": 1,
        "Age": 54
    }

    df_ready = prepare_features_from_raw(example_input)
    print("Prepared features:\n", df_ready.head())

    # Optional check
    check_missing_columns(df_ready)
