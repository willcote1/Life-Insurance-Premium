import pandas as pd
from sqlalchemy import create_engine
from lifelines import WeibullAFTFitter
import joblib

# Connect to the SQLite database and load the data
engine = create_engine("sqlite:///life_insurance.db")
df = pd.read_sql_table("insurance_data", engine)

# Define the list of features to use (numeric and encoded categorical)
features = [
    "weight", "height", "sys_bp", "cholesterol", "num_meds", 
    "occup_danger", "ls_danger", "drinks_aweek"
]
categorical_cols = [
    "sex", "smoker", "nic_other", "cannabis", "opioids", 
    "other_drugs", "addiction", "diabetes", "hds", 
    "asthma", "immune_defic", "family_cancer", 
    "family_heart_disease", "family_cholesterol"
]

# Encode categorical variables: for sex, map 'm'->1, 'f'->0; for others, map 'y'->1, 'n'->0.
for col in categorical_cols:
    if col in df.columns:
        if col == "sex":
            df[col] = df[col].map({"m": 1, "f": 0})
        else:
            df[col] = df[col].map({"y": 1, "n": 0})
            
# Add the categorical columns to features list
features += categorical_cols

# Drop rows with missing values in features or target
df = df.dropna(subset=features + ["age"])

# For survival analysis, treat "age" as the event time.
df["duration"] = df["age"]
df["event"] = 1  # assume all records are uncensored (death observed)

# Select the columns for modeling
data = df[features + ["duration", "event"]]

# Train a Weibull AFT model
aft = WeibullAFTFitter()
aft.fit(data, duration_col="duration", event_col="event")
print(aft.summary)

# Save the trained model to disk
joblib.dump(aft, "age_of_death_model.pkl")
print("Model saved to age_of_death_model.pkl")
