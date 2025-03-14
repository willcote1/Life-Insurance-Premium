import pandas as pd
from sqlalchemy import create_engine

# Load the JSON file into a DataFrame
df = pd.read_json("life_insurance_data.json")

# Create a SQLAlchemy engine for the SQLite database (e.g., life_insurance.db)
engine = create_engine("sqlite:///life_insurance.db")

# Insert the data into a table named "insurance_data"
df.to_sql("insurance_data", engine, if_exists="replace", index=False)

print("JSON data has been inserted into the SQLite database in table 'insurance_data'.")
