#!/usr/bin/env python3
"""
Fresh Database seeding script for VitaCheck
Adds comprehensive sample data for patients, doctors, and health records
Can optionally clear existing data and re-seed
"""

import os
import sys
from db_creator import Session, User, Patient, Doktor, Health_data, suggestions

def clear_database(session):
    """Clear all existing data from database"""
    print("Clearing existing data...")
    session.query(suggestions).delete()
    session.query(Health_data).delete()
    session.query(Patient).delete()
    session.query(Doktor).delete()
    session.query(User).delete()
    session.commit()
    print("Database cleared successfully!")

def seed_database(clear_existing=False):
    """Seed database with comprehensive sample data"""
    
    # Check if database exists
    if not os.path.exists("Database.db"):
        print("Database not found. Please run the main application first to create it.")
        return
    
    session = Session()
    
    try:
        # Check if data already exists
        existing_users = session.query(User).count()
        if existing_users > 0:
            if clear_existing:
                clear_database(session)
            else:
                print("Database already contains data. Use --clear flag to clear and re-seed.")
                print("Or use: python db_seed_fresh.py --clear")
                return
        
        print("Starting database seeding with comprehensive sample data...")
        
        # Create sample users
        users_data = [
            # Patients
            {"username": "hasta1@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta2@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta3@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta4@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta5@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta6@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta7@test.com", "password": "123456", "is_admin": 0},
            {"username": "hasta8@test.com", "password": "123456", "is_admin": 0},
            
            # Doctors
            {"username": "doktor1@test.com", "password": "123456", "is_admin": 1},
            {"username": "doktor2@test.com", "password": "123456", "is_admin": 1},
            {"username": "doktor3@test.com", "password": "123456", "is_admin": 1},
            {"username": "doktor4@test.com", "password": "123456", "is_admin": 1},
            
            # Admin
            {"username": "admin@test.com", "password": "123456", "is_admin": 2},
        ]
        
        created_users = []
        for user_data in users_data:
            user = User(**user_data)
            session.add(user)
            created_users.append(user)
        
        session.commit()
        print(f"Created {len(created_users)} users")
        
        # Create sample patients
        patients_data = [
            {"name": "Ahmet", "surname": "Yılmaz", "user_id": created_users[0].id, "doktor_id": 1},
            {"name": "Fatma", "surname": "Kaya", "user_id": created_users[1].id, "doktor_id": 1},
            {"name": "Mehmet", "surname": "Demir", "user_id": created_users[2].id, "doktor_id": 2},
            {"name": "Ayşe", "surname": "Özkan", "user_id": created_users[3].id, "doktor_id": 2},
            {"name": "Ali", "surname": "Çelik", "user_id": created_users[4].id, "doktor_id": 3},
            {"name": "Zeynep", "surname": "Arslan", "user_id": created_users[5].id, "doktor_id": 3},
            {"name": "Mustafa", "surname": "Koç", "user_id": created_users[6].id, "doktor_id": 4},
            {"name": "Elif", "surname": "Şahin", "user_id": created_users[7].id, "doktor_id": 4},
        ]
        
        created_patients = []
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            session.add(patient)
            created_patients.append(patient)
        
        # Create sample doctors
        doctors_data = [
            {"name": "Elif", "surname": "Yılmaz", "user_id": created_users[8].id},
            {"name": "Ali", "surname": "Özkan", "user_id": created_users[9].id},
            {"name": "Zeynep", "surname": "Demir", "user_id": created_users[10].id},
            {"name": "Mehmet", "surname": "Koç", "user_id": created_users[11].id},
        ]
        
        created_doctors = []
        for doctor_data in doctors_data:
            doctor = Doktor(**doctor_data)
            session.add(doctor)
            created_doctors.append(doctor)
        
        session.commit()
        print(f"Created {len(created_patients)} patients and {len(created_doctors)} doctors")
        
        # Create comprehensive health data
        health_data_samples = [
            # High risk patient
            {
                "user_id": created_users[0].id,
                "weight": 85,
                "height": 175,
                "age": 58,
                "gender": "Erkek",
                "chest_pain": 1,
                "shortness_of_breath": 1,
                "fatigue": 1,
                "palpitations": 1,
                "smoker": 1,
                "diabetes": 1,
                "dizziness": 1,
                "swelling": 1,
                "radiating_pain": 1,
                "cold_sweats": 1,
                "hypertension": 1,
                "colestrol_high": 1,
                "obesity": 1,
                "family_history": 1,
                "risk_label": 5
            },
            # Medium risk patient
            {
                "user_id": created_users[1].id,
                "weight": 75,
                "height": 165,
                "age": 45,
                "gender": "Kadın",
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
            # Low risk patient
            {
                "user_id": created_users[2].id,
                "weight": 70,
                "height": 180,
                "age": 35,
                "gender": "Erkek",
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
            },
            # Very low risk patient
            {
                "user_id": created_users[3].id,
                "weight": 55,
                "height": 160,
                "age": 28,
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
            },
            # Medium-high risk patient
            {
                "user_id": created_users[4].id,
                "weight": 90,
                "height": 175,
                "age": 62,
                "gender": "Erkek",
                "chest_pain": 1,
                "shortness_of_breath": 1,
                "fatigue": 1,
                "palpitations": 0,
                "smoker": 1,
                "diabetes": 0,
                "dizziness": 0,
                "swelling": 1,
                "radiating_pain": 1,
                "cold_sweats": 0,
                "hypertension": 1,
                "colestrol_high": 1,
                "obesity": 1,
                "family_history": 1,
                "risk_label": 4
            },
            # Medium risk patient
            {
                "user_id": created_users[5].id,
                "weight": 68,
                "height": 170,
                "age": 42,
                "gender": "Kadın",
                "chest_pain": 0,
                "shortness_of_breath": 0,
                "fatigue": 1,
                "palpitations": 1,
                "smoker": 0,
                "diabetes": 0,
                "dizziness": 0,
                "swelling": 0,
                "radiating_pain": 0,
                "cold_sweats": 0,
                "hypertension": 1,
                "colestrol_high": 0,
                "obesity": 0,
                "family_history": 1,
                "risk_label": 2
            },
            # High risk patient
            {
                "user_id": created_users[6].id,
                "weight": 95,
                "height": 170,
                "age": 55,
                "gender": "Erkek",
                "chest_pain": 1,
                "shortness_of_breath": 1,
                "fatigue": 1,
                "palpitations": 1,
                "smoker": 1,
                "diabetes": 1,
                "dizziness": 1,
                "swelling": 1,
                "radiating_pain": 1,
                "cold_sweats": 1,
                "hypertension": 1,
                "colestrol_high": 1,
                "obesity": 1,
                "family_history": 1,
                "risk_label": 5
            },
            # Low risk patient
            {
                "user_id": created_users[7].id,
                "weight": 60,
                "height": 165,
                "age": 32,
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
        
        print(f"Created {len(health_data_samples)} health data records")
        
        # Create comprehensive suggestions
        suggestions_data = [
            # High risk patient suggestions
            {"suggestion": "ACİL: Yüksek risk grubundasınız. Hemen doktor kontrolüne gitmeniz gerekiyor.", "user_id": created_users[0].id},
            {"suggestion": "Sigara kullanımını tamamen bırakmanız hayati önem taşıyor.", "user_id": created_users[0].id},
            {"suggestion": "Diyabet kontrolünüzü sıkılaştırın ve düzenli ilaç kullanın.", "user_id": created_users[0].id},
            {"suggestion": "Günde en az 30 dakika hafif egzersiz yapın.", "user_id": created_users[0].id},
            
            # Medium risk patient suggestions
            {"suggestion": "Düzenli egzersiz yapmanızı öneriyorum. Günde 30 dakika yürüyüş yapabilirsiniz.", "user_id": created_users[1].id},
            {"suggestion": "Sigara kullanımını bırakmanız kalp sağlığınız için çok önemli.", "user_id": created_users[1].id},
            {"suggestion": "Tansiyonunuzu düzenli kontrol ettirin.", "user_id": created_users[1].id},
            
            # Low risk patient suggestions
            {"suggestion": "Sağlıklı beslenme alışkanlıklarınızı sürdürün.", "user_id": created_users[2].id},
            {"suggestion": "Düzenli kontrollerinizi aksatmayın.", "user_id": created_users[2].id},
            
            # Very low risk patient suggestions
            {"suggestion": "Mevcut sağlıklı yaşam tarzınızı sürdürün.", "user_id": created_users[3].id},
            {"suggestion": "Günlük aktivite seviyenizi artırabilirsiniz.", "user_id": created_users[3].id},
            
            # Medium-high risk patient suggestions
            {"suggestion": "Kilo vermeniz kalp sağlığınız için faydalı olacaktır.", "user_id": created_users[4].id},
            {"suggestion": "Stres yönetimi teknikleri öğrenmenizi öneriyorum.", "user_id": created_users[4].id},
            {"suggestion": "Düzenli doktor kontrolüne gitmeniz önemli.", "user_id": created_users[4].id},
            
            # Medium risk patient suggestions
            {"suggestion": "Tansiyon kontrolünüzü sıkılaştırın.", "user_id": created_users[5].id},
            {"suggestion": "Düzenli egzersiz programına başlayın.", "user_id": created_users[5].id},
            
            # High risk patient suggestions
            {"suggestion": "ACİL: Yüksek risk grubundasınız. Hemen doktor kontrolüne gitmeniz gerekiyor.", "user_id": created_users[6].id},
            {"suggestion": "Tüm ilaçlarınızı düzenli kullanın ve diyetinize dikkat edin.", "user_id": created_users[6].id},
            {"suggestion": "Sigara kullanımını tamamen bırakın.", "user_id": created_users[6].id},
            
            # Low risk patient suggestions
            {"suggestion": "Sağlıklı yaşam tarzınızı sürdürün.", "user_id": created_users[7].id},
            {"suggestion": "Düzenli kontrollerinizi aksatmayın.", "user_id": created_users[7].id}
        ]
        
        for suggestion_data in suggestions_data:
            sugg = suggestions(**suggestion_data)
            session.add(sugg)
        
        session.commit()
        print(f"Created {len(suggestions_data)} suggestions")
        
        print("\n" + "="*50)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("="*50)
        print("\nSample login credentials:")
        print("\nPatients:")
        print("  hasta1@test.com / 123456 (High Risk)")
        print("  hasta2@test.com / 123456 (Medium Risk)")
        print("  hasta3@test.com / 123456 (Low Risk)")
        print("  hasta4@test.com / 123456 (Very Low Risk)")
        print("  hasta5@test.com / 123456 (Medium-High Risk)")
        print("  hasta6@test.com / 123456 (Medium Risk)")
        print("  hasta7@test.com / 123456 (High Risk)")
        print("  hasta8@test.com / 123456 (Low Risk)")
        print("\nDoctors:")
        print("  doktor1@test.com / 123456")
        print("  doktor2@test.com / 123456")
        print("  doktor3@test.com / 123456")
        print("  doktor4@test.com / 123456")
        print("\nAdmin:")
        print("  admin@test.com / 123456")
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        session.rollback()
        raise
    finally:
        session.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed database with sample data')
    parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')
    
    args = parser.parse_args()
    
    seed_database(clear_existing=args.clear) 