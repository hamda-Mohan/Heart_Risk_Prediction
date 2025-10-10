import pandas as pd
import numpy as np
import joblib, json, os 
from sklearn.preprocessing import StandardScaler
# ================================
# Step 1: Load & Inspect
# ================================
CSV_PATH = "dataset/heart_disease_risk_dataset_earlymed.csv"
df = pd.read_csv(CSV_PATH)
print("=== INITIAL HEAD (10) ===")
print(df.head(10))
print("=== INITIAL SHAPE ===")
print(df.shape)
print("=== INITIAL INFO ===")
print(df.info())
print("=== INITIAL MISSING VALUE ===")
print(df.isnull().sum())
print("=== INITIAL DESCRIPE ===")
print(df.describe())
# ================================
# Step 2: Changing datatypes 
# ================================
# Binary columns
binary_cols = ['Chest_Pain','Shortness_of_Breath','Fatigue','Palpitations','Dizziness',
               'Swelling','Pain_Arms_Jaw_Back','Cold_Sweats_Nausea','High_BP','High_Cholesterol',
               'Diabetes','Smoking','Obesity','Sedentary_Lifestyle','Family_History','Chronic_Stress','Gender','Heart_Risk']

# Convert to int
df[binary_cols] = df[binary_cols].astype(int)

# ================================
# Step 3: Remove Duplicates
# ================================
befre = df.shape
print("before removing duplicate : ",befre)
df.duplicated().sum()

df = df.drop_duplicates()

after = df.shape
print("after removing duplicate : ",after)
# ================================
# Step 4: Target variable distribution (Heart_Risk):
# ================================
print("=== TARGET VARIABLE DISTRIBUTION (Heart_Risk) ===")
print(df['Heart_Risk'].value_counts(normalize=True))
### dataset is balanced
# ================================
# Step 5:  Scaling Age Feature 
# ================================
scaler = StandardScaler()
df["Age"]= scaler.fit_transform(df[["Age"]])
print("after scalinggg")
print(df.head(3))
# Save the scaler and the training feature order (X columns) for serving
os.makedirs("models", exist_ok=True)
joblib.dump(scaler, "models/scaler.pkl")

TRAIN_COLUMNS = df.drop(columns=["Heart_Risk", "Gender"]).columns.tolist()
json.dump(TRAIN_COLUMNS, open("models/train_columns.json", "w"))
# ================================
# Step 6: Save Cleaned Dataset
# ================================
OUT_PATH = "dataset/heart_disease_cleaned.csv"
df.to_csv(OUT_PATH, index=False)
print(f"Cleaned dataset saved to {OUT_PATH}")
