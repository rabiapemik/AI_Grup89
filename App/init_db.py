#!/usr/bin/env python3
"""
Database initialization script for VitaCheck
Creates sample users, doctors, and patients for testing
"""

import os
import sys
from db_creator import Session, User, Patient, Doktor, Health_data, suggestions

def init_database():
    """Initialize database with sample data"""
    
    # Check if database exists
    if not os.path.exists("Database.db"):
        print("Database not found. Please run the main application first to create it.")
        return
    
    session = Session()
    
    try:
        # Check if data already exists
        existing_users = session.query(User).count()
        if existing_users > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Initializing database with sample data...")
        
        # Create sample users
        users_data = [
            # Patients
            {"username": "hasta1@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta2@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta3@test.com", "password": "123456", "is_admin": 0},
            
            # Doctors
            {"username": "doktor1@test.com", "password": "123456", "is_admin": 1},
            {"username": "doktor2@test.com", "password": "123456", "is_admin": 1},
            
            # Admin
            {"username": "admin@test.com", "password": "123456", "is_admin": 2},
        ]
        
        created_users = []
        for user_data in users_data:
            user = User(**user_data)
            session.add(user)
            created_users.append(user)
        
        session.commit()
        
        # Create sample patients
        patients_data = [
            {"name": "Ahmet", "surname": "Yılmaz", "user_id": created_users[0].id},
            {"name": "Fatma", "surname": "Kaya", "user_id": created_users[1].id},
            {"name": "Mehmet", "surname": "Demir", "user_id": created_users[2].id},
        ]
        
        created_patients = []
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            session.add(patient)
            created_patients.append(patient)
        
        # Create sample doctors
        doctors_data = [
            {"name": "Elif", "surname": "Yılmaz", "user_id": created_users[3].id},
            {"name": "Ali", "surname": "Özkan", "user_id": created_users[4].id},
        ]
        
        created_doctors = []
        for doctor_data in doctors_data:
            doctor = Doktor(**doctor_data)
            session.add(doctor)
            created_doctors.append(doctor)
        
        session.commit()
        
        # Assign patients to doctors
        if created_patients and created_doctors:
            created_patients[0].doktor_id = created_doctors[0].id
            created_patients[1].doktor_id = created_doctors[0].id
            created_patients[2].doktor_id = created_doctors[1].id
        
        # Create sample health data
        health_data_samples = [
            {
                "user_id": created_users[0].id,
                "weight": 75,
                "height": 175,
                "age": 45,
                "gender": "Erkek",
                "chest_pain": 1,
                "shortness_of_breath": 0,
                "fatigue": 1,
                "palpitations": 0,
                "smoker": 1,
                "diabetes": 0,
                "dizziness": 0,
                "swelling": 0,
                "radiating_pain": 0,
                "cold_sweats": 0,
                "hypertension": 1,
                "colestrol_high": 0,
                "obesity": 0,
                "family_history": 1,
                "risk_label": 3
            },
            {
                "user_id": created_users[1].id,
                "weight": 60,
                "height": 165,
                "age": 35,
                "gender": "Kadın",
                "chest_pain": 0,
                "shortness_of_breath": 0,
                "fatigue": 0,
                "palpitations": 0,
                "smoker": 0,
                "diabetes": 0,
                "dizziness": 0,
                "swelling": 0,
                "radiating_pain": 0,
                "cold_sweats": 0,
                "hypertension": 0,
                "colestrol_high": 0,
                "obesity": 0,
                "family_history": 0,
                "risk_label": 1
            }
        ]
        
        for health_data in health_data_samples:
            hd = Health_data(**health_data)
            session.add(hd)
        
        # Create sample suggestions
        suggestions_data = [
            {"suggestion": "Düzenli egzersiz yapmanızı öneriyorum. Günde 30 dakika yürüyüş yapabilirsiniz.", "user_id": created_users[0].id},
            {"suggestion": "Sigara kullanımını bırakmanız kalp sağlığınız için çok önemli.", "user_id": created_users[0].id},
            {"suggestion": "Sağlıklı beslenme alışkanlıkları edinmenizi öneriyorum.", "user_id": created_users[1].id},
        ]
        
        for suggestion_data in suggestions_data:
            sugg = suggestions(**suggestion_data)
            session.add(sugg)
        
        session.commit()
        
        print("Database initialized successfully!")
        print("\nSample login credentials:")
        print("Patients:")
        print("  hasta1@test.com / 123456")
        print("  hasta2@test.com / 123456")
        print("  hasta3@test.com / 123456")
        print("\nDoctors:")
        print("  doktor1@test.com / 123456")
        print("  doktor2@test.com / 123456")
        print("\nAdmin:")
        print("  admin@test.com / 123456")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_database() 