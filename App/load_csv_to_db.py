import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_creator import Base, Health_data, User, Patient
import os

def load_csv_to_database():
    """Load heart.csv data into the database"""
    
    # Read the CSV file
    try:
        df = pd.read_csv('heart.csv')
        print(f"CSV loaded successfully. Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
    
    # Create database engine
    engine = create_engine("sqlite:///Database.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    # Create a test user for the CSV data
    test_user = User(
        username="csv_data_user",
        password="csv_data_password",
        is_admin=0
    )
    session.add(test_user)
    session.commit()
    
    # Create a test patient
    test_patient = Patient(
        name="CSV",
        surname="Data",
        user_id=test_user.id
    )
    session.add(test_patient)
    session.commit()
    
    print(f"Created test user with ID: {test_user.id}")
    
    # Map CSV columns to database columns
    column_mapping = {
        'Chest_Pain': 'chest_pain',
        'Shortness_of_Breath': 'shortness_of_breath',
        'Fatigue': 'fatigue',
        'Palpitations': 'palpitations',
        'Dizziness': 'dizziness',
        'Swelling': 'swelling',
        'Pain_Arms_Jaw_Back': 'radiating_pain',
        'Cold_Sweats_Nausea': 'cold_sweats',
        'High_BP': 'hypertension',
        'High_Cholesterol': 'colestrol_high',
        'Diabetes': 'diabetes',
        'Smoking': 'smoker',
        'Obesity': 'obesity',
        'Sedentary_Lifestyle': 'sedentary_lifestyle',  # This will be mapped to obesity
        'Family_History': 'family_history',
        'Chronic_Stress': 'chronic_stress',  # This will be mapped to hypertension
        'Gender': 'gender',
        'Age': 'age'
    }
    
    # Process each row in the CSV
    records_added = 0
    for index, row in df.iterrows():
        try:
            # Create health data record
            health_data = Health_data(
                user_id=test_user.id,
                weight=70,  # Default weight since not in CSV
                height=170,  # Default height since not in CSV
                age=int(row['Age']) if pd.notna(row['Age']) else 50,
                gender=str(row['Gender']) if pd.notna(row['Gender']) else 'Unknown',
                chest_pain=int(row['Chest_Pain']) if pd.notna(row['Chest_Pain']) else 0,
                shortness_of_breath=int(row['Shortness_of_Breath']) if pd.notna(row['Shortness_of_Breath']) else 0,
                fatigue=int(row['Fatigue']) if pd.notna(row['Fatigue']) else 0,
                palpitations=int(row['Palpitations']) if pd.notna(row['Palpitations']) else 0,
                smoker=int(row['Smoking']) if pd.notna(row['Smoking']) else 0,
                diabetes=int(row['Diabetes']) if pd.notna(row['Diabetes']) else 0,
                dizziness=int(row['Dizziness']) if pd.notna(row['Dizziness']) else 0,
                swelling=int(row['Swelling']) if pd.notna(row['Swelling']) else 0,
                radiating_pain=int(row['Pain_Arms_Jaw_Back']) if pd.notna(row['Pain_Arms_Jaw_Back']) else 0,
                cold_sweats=int(row['Cold_Sweats_Nausea']) if pd.notna(row['Cold_Sweats_Nausea']) else 0,
                hypertension=int(row['High_BP']) if pd.notna(row['High_BP']) else 0,
                colestrol_high=int(row['High_Cholesterol']) if pd.notna(row['High_Cholesterol']) else 0,
                obesity=int(row['Obesity']) if pd.notna(row['Obesity']) else 0,
                family_history=int(row['Family_History']) if pd.notna(row['Family_History']) else 0,
                risk_label=int(row['Heart_Risk']) if 'Heart_Risk' in row and pd.notna(row['Heart_Risk']) else 1
            )
            
            session.add(health_data)
            records_added += 1
            
            # Commit every 100 records to avoid memory issues
            if records_added % 100 == 0:
                session.commit()
                print(f"Processed {records_added} records...")
                
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue
    
    # Final commit
    session.commit()
    session.close()
    
    print(f"Successfully added {records_added} records to the database.")
    print("CSV data has been loaded into the database.")

if __name__ == "__main__":
    load_csv_to_database() 