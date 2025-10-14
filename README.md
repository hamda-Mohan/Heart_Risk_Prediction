# Heart Disease Risk Prediction

Predict the risk of heart disease (low/high) using 17 binary health indicators + age.

## Dataset
[Kaggle – Heart Disease Risk Prediction Dataset](https://www.kaggle.com/datasets/mahatiratusher/heart-disease-risk-prediction-dataset)  
70,000 samples, balanced dataset.

## Models Used
- Logistic Regression
- Random Forest
- Decision Tree
- XGBoost

## Setup
```bash
pip install -r requirements.txt

```
## Preprocess Data
```python
python preprocessing.py
```


## Train Models
```python
python model.py
```
## Run API
```python
python app.py
```
## API Usage Example
```json
curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d '{"Chest_Pain":1,"Shortness_of_Breath":0,
"Fatigue":1,
"Palpitations":0,
"Dizziness":0,
"Swelling":1,
"Pain_Arms_Jaw_Back":0,"Cold_Sweats_Nausea":0,
"High_BP":1,
"High_Cholesterol":1,
"Diabetes":0,"Smoking":0,
"Obesity":0,
"Sedentary_Lifestyle":1,"Family_History":1,
"Chronic_Stress":0,"Age":55
}'
```
## Resbonse
```json
{"input":{"Age":55,"Chest_Pain":1,"Chronic_Stress":0,"Cold_Sweats_Nausea":0,"Diabetes":0,"Dizziness":0,"Family_History":1,"Fatigue":1,"High_BP":1,"High_Cholesterol":1,"Obesity":0,"Pain_Arms_Jaw_Back":0,"Palpitations":0,"Sedentary_Lifestyle":1,"Shortness_of_Breath":0,"Smoking":0,"Swelling":1},"model":"logistic_regression","prediction":0,"probability":0.08}
 ```





