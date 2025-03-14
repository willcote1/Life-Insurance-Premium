import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib

# Connect to the SQLite database
engine = create_engine("sqlite:///life_insurance.db")
df = pd.read_sql_table("insurance_data", engine)

# List of categorical columns to encode. Adjust based on your JSON fields.
categorical_cols = [
    "sex", "smoker", "nic_other", "cannabis", "opioids", 
    "other_drugs", "addiction", "diabetes", "hds", 
    "asthma", "immune_defic", "family_cancer", 
    "family_heart_disease", "family_cholesterol"
]

# Encode categorical features: for "sex", map 'm'->1, 'f'->0; for the others, map 'y'->1, 'n'->0.
for col in categorical_cols:
    if col in df.columns:
        if col == "sex":
            df[col] = df[col].map({"m": 1, "f": 0})
        else:
            df[col] = df[col].map({"y": 1, "n": 0})

# Define features and target. We treat "age" (from the JSON) as the age of death.
# Choose a set of features that appear in your JSON.
features = [
    "weight", "height", "sys_bp", "cholesterol", "num_meds", 
    "occup_danger", "ls_danger", "drinks_aweek"
] + categorical_cols

target = "age"

# Drop rows with missing values for features or target
df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Gradient Boosting Regressor
model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("Test RMSE: ", rmse)
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="neg_mean_squared_error")
cv_rmse = np.sqrt(-cv_scores.mean())
print("CV RMSE: ", cv_rmse)

# Save the trained model
joblib.dump(model, "age_of_death_model.pkl")
print("Model saved to age_of_death_model.pkl")
