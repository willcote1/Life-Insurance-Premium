from sqlalchemy import create_engine
import pandas as pd

# Create a SQLAlchemy engine for an SQLite database named 'insurance_rates.db'
engine = create_engine("sqlite:///insurance_rates.db")

# Load the processed CSV file
df_processed = pd.read_csv("processed_insurance_data.csv")

# Insert data into a table named 'insurance_rates'
df_processed.to_sql("insurance_rates", engine, if_exists="replace", index=False)

print("Data inserted into the SQL database!")

