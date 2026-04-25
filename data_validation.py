import pandas as pd 
import numpy as np
import re

# Load data
df = pd.read_csv("C:\\Users\\priya\\Downloads\\PAN_DATA.csv")

# ------------------ VALIDATION FUNCTIONS ------------------

def validate_pan(pan):
    if pd.isnull(pan):
        return False
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    return bool(re.match(pattern, pan))

def validate_email(email):
    if pd.isnull(email):
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# ------------------ APPLY VALIDATIONS ------------------

df['PAN_valid'] = df['PAN'].apply(validate_pan)
df['Email_valid'] = df['Email'].apply(validate_email)

df['Age_valid'] = df['Age'].apply(lambda x: 0 < x < 100 if pd.notnull(x) else False)
df['Salary_valid'] = df['Salary'].apply(lambda x: x > 0 if pd.notnull(x) else False)

# ------------------ OVERALL STATUS ------------------

df['Overall_Status'] = df[
    ['PAN_valid', 'Email_valid', 'Age_valid', 'Salary_valid']
].all(axis=1)

# ------------------ ERROR COLUMN ------------------

def get_errors(row):
    errors = []
    
    if not row['PAN_valid']:
        errors.append("Invalid PAN")
    if not row['Email_valid']:
        errors.append("Invalid Email")
    if not row['Age_valid']:
        errors.append("Invalid Age")
    if not row['Salary_valid']:
        errors.append("Invalid Salary")
    
    return ", ".join(errors)

df['Errors'] = df.apply(get_errors, axis=1)

# ------------------ FILTER DATA ------------------

# Valid data
valid_df = df[df['Overall_Status']]

# Invalid data
invalid_df = df[~df['Overall_Status']]

# ------------------ SAVE FILES ------------------

valid_df.to_csv("valid_data.csv", index=False)
invalid_df.to_csv("invalid_data.csv", index=False)

# ------------------ PRINT SUMMARY ------------------

print("Total Records:", len(df))
print("Valid Records:", len(valid_df))
print("Invalid Records:", len(invalid_df))