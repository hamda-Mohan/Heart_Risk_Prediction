
# Heart Disease Risk Prediction – Project Paper

## 1. Problem Statement & Motivation

Heart disease is one of the leading causes of death worldwide. Early detection of individuals at high risk can help in timely interventions and reduce mortality. This project aims to predict the risk of heart disease (low/high) based on a set of 17 binary health indicators and age. By leveraging machine learning models and deploying them as an API, healthcare professionals or individuals can get a quick assessment of their heart disease risk.

---


## **2. Dataset & Preprocessing**

### **2.1 Dataset Overview**

The dataset used for this project is the **Heart Disease Risk Prediction Dataset** sourced from **Kaggle** [Kaggle – Heart Disease Risk Prediction Dataset](https://www.kaggle.com/datasets/mahatiratusher/heart-disease-risk-prediction-dataset)  .
It originally contained **70,000 samples and 19 columns**, each representing a health-related feature or demographic indicator.

| Attribute Type  |     Count    | Description                                      |
| :-------------- | :----------: | :----------------------------------------------- |
| **Features**    |      18      | Symptoms, lifestyle, and health metrics          |
| **Target**      |       1      | `Heart_Risk` (0 = Low Risk 💚, 1 = High Risk ❤️) |
| **Shape**       | (70,000, 19) | Before cleaning                                  |
| **Final Shape** | (63,755, 19) | After removing duplicates                        |

### **2.2 Feature Details**

Some of the most important binary indicators include:

* **Chest_Pain, Shortness_of_Breath, Fatigue, Palpitations**
* **Dizziness, Swelling, Pain_Arms_Jaw_Back**
* **Cold_Sweats_Nausea, High_BP, High_Cholesterol**
* **Diabetes, Smoking, Obesity, Sedentary_Lifestyle**
* **Family_History, Chronic_Stress, Gender**
* **Age** (numeric, standardized)

### **2.3 Sample Data (Head – 10 rows)**

| Chest_Pain | Shortness_of_Breath | Fatigue | Palpitations | High_BP | Family_History | Age | Heart_Risk |
| :--------- | :-----------------: | :-----: | :----------: | :-----: | :----: | :-: | :--------: |
| 0          |          0          |    0    |       1      |    0    |    0   |  48 |      0     |
| 0          |          1          |    0    |       1      |    0    |    0   |  46 |      0     |
| 1          |          0          |    0    |       1      |    0    |    1   |  66 |      0     |
| 1          |          1          |    0    |       1      |    1    |    1   |  60 |      1     |
| 0          |          0          |    1    |       0      |    0    |    0   |  69 |      0     |
| 1          |          1          |    0    |       1      |    0    |    1   |  55 |      1     |
| 1          |          1          |    1    |       1      |    0    |    1   |  51 |      1     |
| 1          |          1          |    1    |       1      |    1    |    0   |  67 |      1     |
| 1          |          1          |    1    |       1      |    0    |    1   |  71 |      1     |
| 0          |          0          |    0    |       0      |    0    |    1   |  65 |      0     |

---

### **2.4 Data Cleaning**

* Verified **no missing values** in any column.
* Removed **6,245 duplicate rows**, resulting in a clean dataset of **63,755 samples**.
* Ensured all categorical features are encoded as **0 or 1**.

---

### **2.5 Feature Scaling**

* The `Age` column was **standardized** using `StandardScaler` to ensure uniform scale among features.
  Example after scaling:

| Chest_Pain | Shortness_of_Breath | Fatigue | Palpitations | Family_History | Age (Scaled) | Heart_Risk |
| :--------: | :-----------------: | :-----: | :----------: | :----: | :----------: | :--------: |
|      0     |          0          |    0    |       1      |    0   |    -0.3855   |      0     |
|      0     |          1          |    0    |       1      |    0   |    -0.5073   |      0     |
|      1     |          0          |    0    |       1      |    1   |    0.7110    |      0     |

---

### **2.6 Target Distribution**

| Class                | Count (%) |
| :------------------- | :-------: |
| 💚 **Low Risk (0)**  |   50.6%   |
| ❤️ **High Risk (1)** |   49.4%   |

This balanced distribution helps prevent bias in the model.

---

### **2.7 Preprocessing Steps Summary**

1. **Data Cleaning:** Removed duplicates and validated binary encoding (0/1).
2. **Feature Scaling:** Applied `StandardScaler` to `Age`.
3. **Train-Test Split:** 80% for training, 20% for testing.
4. **Persistence:** Saved column order and scaler object for consistent preprocessing during model inference.

---
---

## 3. Algorithms and Why Chosen

Four supervised machine learning algorithms were trained and evaluated:

| Algorithm                    | Description                                     | Reason for Use                                        |
| ---------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| **Logistic Regression (LR)** | Linear baseline model for binary classification | Provides interpretability and fast training           |
| **Random Forest (RF)**       | Ensemble of decision trees                      | Reduces overfitting and captures non-linear relations |
| **Decision Tree (DT)**       | Simple rule-based classifier                    | Easy visualization, good for feature importance       |
| **XGBoost (XGB)**            | Gradient-boosted decision trees                 | High accuracy and efficient computation               |

These models were selected to cover both simple interpretable and high-performance ensemble approaches.

---

## 4. Results & Discussion

### 4.1 Model Performance Summary

| Model               | Accuracy | Precision | Recall | F1-Score |
| ------------------- | -------- | --------- | ------ | -------- |
| Logistic Regression | 0.992    | 0.992     | 0.993  | 0.992    |
| Random Forest       | 0.992    | 0.991     | 0.993  | 0.992    |
| Decision Tree       | 0.957    | 0.959     | 0.956  | 0.957    |
| **XGBoost**             | **0.993**    | **0.993**     | **0.994**  | **0.994**    |



---



### **4.2 Confusion Matrices**

####  Logistic Regression

|                         | Pred Positive (1) | Pred Negative (0) |
| :---------------------- | :---------------: | :---------------: |
| **Actual Positive (1)** |        6272       |         50        |
| **Actual Negative (0)** |         48        |        6381       |

**Accuracy = 0.992**, Precision = 0.992, Recall = 0.993, F1 = 0.992

---

####  Random Forest

|                         | Pred Positive (1) | Pred Negative (0) |
| :---------------------- | :---------------: | :---------------: |
| **Actual Positive (1)** |        6266       |         56        |
| **Actual Negative (0)** |         42        |        6387       |

**Accuracy = 0.992**, Precision = 0.991, Recall = 0.993, F1 = 0.992

---

####  Decision Tree

|                         | Pred Positive (1) | Pred Negative (0) |
| :---------------------- | :---------------: | :---------------: |
| **Actual Positive (1)** |        6057       |        265        |
| **Actual Negative (0)** |        281        |        6148       |

**Accuracy = 0.957**, Precision = 0.959, Recall = 0.956, F1 = 0.957

---

####  XGBoost

|                         | Pred Positive (1) | Pred Negative (0) |
| :---------------------- | :---------------: | :---------------: |
| **Actual Positive (1)** |        6275       |         47        |
| **Actual Negative (0)** |         36        |        6393       |

**Accuracy = 0.993**, Precision = 0.993, Recall = 0.994, F1 = 0.994

---

All models performed well, but **XGBoost achieved the highest accuracy (99.3%)** and **best F1-score (0.994)** — making it the **best overall model**.

---

### **4.3 Why XGBoost Was Chosen (Simple Explanation)**

XGBoost was selected as the **best model** because:

* It had **the highest accuracy and F1-score** among all models.
* It combines the strengths of multiple trees to reduce errors.
* It generalizes better and avoids overfitting compared to a single decision tree.
* It runs efficiently and handles both linear and non-linear relationships well.

In short: **XGBoost gave the most accurate, stable, and reliable predictions.**

---
### 4.4 Sanity Check Predictions

| **Sample** | **Actual Risk** | **LogReg** | **RandForest** | **DecTree** | **XGBoost** |
| ------------- | --------------- | ---------- | -------------- | ----------- | ----------- |
| 13            | ❤️ High (1)     | ❤️ High    | ❤️ High        | ❤️ High     | ❤️ High     |
| 4             | ❤️ High (1)     | ❤️ High    | ❤️ High        | ❤️ High     | ❤️ High     |
| 6             | 💚 Low (0)      | 💚 Low     | 💚 Low         | 💚 Low      | 💚 Low      |
| 7000          | ❤️ High (1)     | ❤️ High    | ❤️ High        | ❤️ High     | ❤️ High     |
| 9354          | 💚 Low (0)      | 💚 Low     | 💚 Low         | 💚 Low      | 💚 Low      |
| 12345         | 💚 Low (0)      | 💚 Low     | 💚 Low         | ❤️ High     | 💚 Low      |

**Observation:**
All models consistently predicted correctly except the Decision Tree, which made one false positive (sample 12345). This confirms that XGBoost and Logistic Regression are the most reliable.

---

### 4.5 Custom Input Prediction

| **Model**           | **Predicted Risk (1=High)** |
| ------------------- | --------------------------- |
| Logistic Regression | 1.0                         |
| Random Forest       | 1.0                         |
| Decision Tree       | 1.0                         |
| XGBoost             | 1.0                         |

All models consistently predicted **High Risk (1)** for the custom test input — validating model stability and agreement.


---

## 5. Deployment Notes

**API Deployment:**

* **Framework:** Flask
* **Endpoints:**

  1. `/predict` – Accepts JSON input and returns prediction and probability.
  2. `/register` – Registers users with email and password.
  3. `/login` – Authenticates users and provides session tokens.
  4. `/logout` – Ends the session token.
  5. `/` – Health check endpoint

**API Usage Example:**

```bash
curl -X POST http://127.0.0.1:8000/predict?model=xgb \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{"Chest_Pain":1,"Shortness_of_Breath":1,"Fatigue":0,"Palpitations":1,
"Dizziness":0,"Swelling":1,"Pain_Arms_Jaw_Back":1,"Cold_Sweats_Nausea":1,
"High_BP":1,"High_Cholesterol":1,"Diabetes":1,"Smoking":1,"Obesity":1,
"Sedentary_Lifestyle":1,"Family_History":1,"Chronic_Stress":1,"Age":65}'
```

**Response Example:**

```json
{
  "model": "xgboost",
  "input": { ... },
  "prediction": 1,
  "probability": 0.98
}
```

---

## 6. Lessons Learned

* Proper **preprocessing and feature scaling** are critical for model performance.
* Ensemble models like Random Forest and XGBoost outperform single Decision Trees for complex datasets.
* Testing with **sanity check samples** helps verify model correctness before deployment.
* API deployment requires careful **session management** for security.
* Documenting and saving feature column order and scalers ensures **consistent predictions** across environments.

---

 **Conclusion:**
The project successfully built a heart disease risk prediction system with high accuracy. XGBoost was selected as the best model and deployed via a Flask API. This system demonstrates the end-to-end pipeline from dataset collection, preprocessing, model training, evaluation, to deployment — suitable for real-world application.

---


