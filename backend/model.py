# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)
from utils import prepare_features_from_raw


# ------------------------------------------------------------
# LOAD & PREPARE DATA
# ------------------------------------------------------------
print("Loading and preparing dataset...")

# Load dataset
df = pd.read_csv("dataset/heart_disease_cleaned.csv")

# Separate features (X) and target (y)
X = df.drop(columns=["Heart_Risk", "Gender"])   # Remove target and unnecessary column
y = df["Heart_Risk"]

# Split into training (80%) and test (20%) sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Dataset loaded successfully!")
print(f"Training samples: {X_train.shape[0]}")
print(f"Testing samples : {X_test.shape[0]}")
print("-" * 60)

# ------------------------------------------------------------
# TRAIN MODELS
# ------------------------------------------------------------
print("Training models...")

# Logistic Regression Model
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)

# Random Forest Model
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

# Decision Tree Model
dt = DecisionTreeClassifier(
    max_depth=6,
    random_state=42
)
dt.fit(X_train, y_train)



print("Model training complete!")
print("-" * 60)

# ------------------------------------------------------------
# MODEL PREDICTIONS
# ------------------------------------------------------------
print("Making predictions...")

# Predictions
lr_predict = lr.predict(X_test)
rf_predict = rf.predict(X_test)
dt_predict = dt.predict(X_test)
xgb_predict = xgb.predict(X_test)


print("Predictions generated!")
print("-" * 60)

# ------------------------------------------------------------
# EVALUATION FUNCTIONS
# ------------------------------------------------------------
def print_metrics(name, y_true, y_predicted, pos_label=0):
    """Display accuracy, precision, recall, and F1-score."""
    ac = accuracy_score(y_true, y_predicted)
    prec = precision_score(y_true, y_predicted, pos_label=pos_label)
    rec = recall_score(y_true, y_predicted, pos_label=pos_label)
    f1 = f1_score(y_true, y_predicted, pos_label=pos_label)

    print(f"{name} Performance Metrics:")
    print(f"Accuracy : {ac:.3f}")
    print(f"Precision: {prec:.3f}")
    print(f"Recall   : {rec:.3f}")
    print(f"F1-Score : {f1:.3f}")
    print("-" * 60)


def print_cm(name, y_true, y_predicted):
    """Display confusion matrix in readable format."""
    cm = confusion_matrix(y_true, y_predicted, labels=[1, 0])
    cm_df = pd.DataFrame(
        cm,
        index=["Actual Positive(1)", "Actual Negative(0)"],
        columns=["Pred Positive(1)", "Pred Negative(0)"]
    )
    print(f"{name} - Confusion Matrix:\n{cm_df}\n")
    print("-" * 60)

# ------------------------------------------------------------
# MODEL EVALUATION
# ------------------------------------------------------------
print("Evaluating models...\n")

# Logistic Regression results
print_metrics("Logistic Regression", y_test, lr_predict)
print_cm("Logistic Regression", y_test, lr_predict)

# Random Forest results
print_metrics("Random Forest", y_test, rf_predict)
print_cm("Random Forest", y_test, rf_predict)
print("=" * 60)

# Decision Tree results
print_metrics("Decision Tree", y_test, dt_predict)
print_cm("Decision Tree", y_test, dt_predict)




# ------------------------------------------------------------
# SAMPLE PREDICTIONS (SANITY CHECK)
# ------------------------------------------------------------
print("Sanity Check Sample Predictions:\n")
def bin2str(v): 

    """Convert 0/1 to readable labels."""
    return "💚 Low Risk (0)" if v == 0 else "❤️ High Risk (1)"

sample_indices = [13, 4, 6,7000,9354,12345,]

for i in sample_indices:
    x_one = X_test.iloc[[i]]      # Single test sample
    y_true = y_test.iloc[i]       # Actual label
    p_lr = int(lr.predict(x_one)[0])
    p_rf = int(rf.predict(x_one)[0])
    p_dt = int(dt.predict(x_one)[0])
 

    print(f"Sample {i}:")
    print(f"Actual Heart_Risk: {bin2str(y_true)}")
    print(f"Logistic Regression Prediction: {bin2str(p_lr)}")
    print(f"Random Forest Prediction      : {bin2str(p_rf)}")
    print(f"Decision Tree Prediction      : {bin2str(p_dt)}")
    
    print("-" * 60)

custom = {
    "Chest_Pain": 1,
    "Shortness_of_Breath": 1,
    "Fatigue": 0,
    "Palpitations": 1,
    "Dizziness": 0,
    "Swelling": 1,
    "Pain_Arms_Jaw_Back": 1,
    "Cold_Sweats_Nausea": 1,
    "High_BP": 1,
    "High_Cholesterol": 1,
    "Diabetes": 1,
    "Smoking": 1,
    "Obesity": 1,
    "Sedentary_Lifestyle": 1,
    "Family_History": 1,
    "Chronic_Stress": 1,
    "Age": 65
}
x_new_df = prepare_features_from_raw(custom)
print("\n=== Custom Input Prediction ===")
print("Logistic Regression:", float(lr.predict(x_new_df)[0]))
print("Random Forest    :", float(rf.predict(x_new_df)[0])) 
print("Decision Tree    :", float(dt.predict(x_new_df)[0]))


# SAVE MODELS 
joblib.dump(lr, "models/lr_model.joblib")
joblib.dump(rf, "models/rf_model.joblib")
joblib.dump(dt, "models/dt_model.joblib")
# ------------------------------------------------------------
# END OF SCRIPT
# ------------------------------------------------------------
print("Model training, testing, and evaluation completed successfully!")
