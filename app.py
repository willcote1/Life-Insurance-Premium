from flask import Flask, render_template, request
import pandas as pd
import joblib
import math

app = Flask(__name__)

# Load the pre-trained age-of-death survival model
aft = joblib.load("age_of_death_model.pkl")

# The features used by the survival model; must match the training order.
model_features = [
    "weight", "height", "sys_bp", "cholesterol", "num_meds", 
    "occup_danger", "ls_danger", "drinks_aweek",
    "sex", "smoker", "nic_other", "cannabis", "opioids", 
    "other_drugs", "addiction", "diabetes", "hds", 
    "asthma", "immune_defic", "family_cancer", 
    "family_heart_disease", "family_cholesterol"
]

def predict_age_of_death(input_data):
    """
    Given a dictionary of input data (keys matching model_features),
    returns the predicted median duration (which here represents the predicted age of death).
    """
    df_input = pd.DataFrame([input_data])
    # lifelines' predict_median returns a Series.
    median = aft.predict_median(df_input)
    return float(median.iloc[0])

def calculate_premium_advanced(current_age, predicted_age, policy_amount, insurance_type, term_length=None):
    """
    Calculates the monthly premium using a survival approach.
    
    1. Calculate remaining years = predicted_age - current_age. If <=0, set to 1.
    2. Derive an effective annual mortality rate r = 1 / remaining_years.
    3. Set T = term_length if term life; for whole life, T = remaining years.
    4. Use an annual discount rate i (5%).
    5. Compute survival probability over T years: S(T) = exp(-rT), death probability q(T) = 1 - S(T).
    6. Present Value (PV) = (policy_amount * q(T)) / ((1 + i)^T).
    7. Base monthly premium = PV / (T * 12).
    8. For whole life, multiply the base monthly premium by a factor (e.g., 1.5).
    """
    whole_life_factor = 1.5
    remaining_years = predicted_age - current_age
    if remaining_years <= 0:
        remaining_years = 1
    r = 1 / remaining_years
    if insurance_type == "term":
        if term_length is None or term_length <= 0:
            raise ValueError("A positive term length is required for term life policies.")
        T = term_length
    else:
        T = remaining_years
    i = 0.05
    S_T = math.exp(-r * T)
    q_T = 1 - S_T
    PV = (policy_amount * q_T) / ((1 + i) ** T)
    base_monthly = PV / (T * 12)
    if insurance_type == "whole":
        base_monthly *= whole_life_factor
    return round(base_monthly, 2)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    premium = None
    if request.method == "POST":
        try:
            # Collect policy details
            current_age = float(request.form["current_age"])
            policy_amount = float(request.form["policy_amount"])
            insurance_type = request.form["insurance_type"]
            term_length = None
            if insurance_type == "term":
                term_length = float(request.form["term_length"])
            
            # Collect health & demographic inputs for the survival model
            input_data = {
                "weight": float(request.form["weight"]),
                "height": float(request.form["height"]),
                "sys_bp": float(request.form["sys_bp"]),
                "cholesterol": float(request.form["cholesterol"]),
                "num_meds": float(request.form["num_meds"]),
                "occup_danger": float(request.form["occup_danger"]),
                "ls_danger": float(request.form["ls_danger"]),
                "drinks_aweek": float(request.form["drinks_aweek"]),
                "sex": 1 if request.form["sex"].lower() == "m" else 0,
                "smoker": 1 if request.form["smoker"].lower() == "y" else 0,
                "nic_other": 1 if request.form["nic_other"].lower() == "y" else 0,
                "cannabis": 1 if request.form["cannabis"].lower() == "y" else 0,
                "opioids": 1 if request.form["opioids"].lower() == "y" else 0,
                "other_drugs": 1 if request.form["other_drugs"].lower() == "y" else 0,
                "addiction": 1 if request.form["addiction"].lower() == "y" else 0,
                "diabetes": 1 if request.form["diabetes"].lower() == "y" else 0,
                "hds": 1 if request.form["hds"].lower() == "y" else 0,
                "asthma": 1 if request.form["asthma"].lower() == "y" else 0,
                "immune_defic": 1 if request.form["immune_defic"].lower() == "y" else 0,
                "family_cancer": 1 if request.form["family_cancer"].lower() == "y" else 0,
                "family_heart_disease": 1 if request.form["family_heart_disease"].lower() == "y" else 0,
                "family_cholesterol": 1 if request.form["family_cholesterol"].lower() == "y" else 0,
            }
            
            predicted_age = predict_age_of_death(input_data)
            premium = calculate_premium_advanced(current_age, predicted_age, policy_amount, insurance_type, term_length)
        except Exception as e:
            prediction = f"Error: {str(e)}"
    return render_template("index.html", prediction=prediction, premium=premium)

if __name__ == "__main__":
    app.run(debug=True)
