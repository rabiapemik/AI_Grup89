#!/usr/bin/env python3
"""
Setup script for ML integration with VitaCheck
This script will:
1. Load CSV data into the database
2. Train/initialize the ML model
3. Test the integration
"""

import os
import sys
from load_csv_to_db import load_csv_to_database
from ml_model_integration import initialize_ml_model, get_risk_prediction

def main():
    print("=== VitaCheck ML Integration Setup ===")
    print()
    
    # Step 1: Load CSV data into database
    print("Step 1: Loading CSV data into database...")
    try:
        load_csv_to_database()
        print("✓ CSV data loaded successfully")
    except Exception as e:
        print(f"✗ Error loading CSV data: {e}")
        return False
    
    print()
    
    # Step 2: Initialize ML model
    print("Step 2: Initializing ML model...")
    try:
        success = initialize_ml_model()
        if success:
            print("✓ ML model initialized successfully")
        else:
            print("✗ Failed to initialize ML model")
            return False
    except Exception as e:
        print(f"✗ Error initializing ML model: {e}")
        return False
    
    print()
    
    # Step 3: Test the integration
    print("Step 3: Testing ML model integration...")
    try:
        # Test data
        test_data = {
            'chest_pain': 1,
            'shortness_of_breath': 0,
            'fatigue': 1,
            'palpitations': 0,
            'dizziness': 0,
            'swelling': 0,
            'radiating_pain': 1,
            'cold_sweats': 0,
            'hypertension': 1,
            'colestrol_high': 1,
            'diabetes': 0,
            'smoker': 1,
            'obesity': 1,
            'family_history': 1,
            'sedentary_lifestyle': 1,
            'chronic_stress': 1,
            'gender': 1,
            'age': 58
        }
        
        prediction = get_risk_prediction(test_data)
        if prediction:
            print(f"✓ Test prediction successful:")
            print(f"  Risk Percentage: {prediction['risk_percentage']:.2f}%")
            print(f"  Risk Label: {prediction['risk_label']}")
            print(f"  Confidence: {prediction['confidence']:.3f}")
        else:
            print("✗ Test prediction failed")
            return False
    except Exception as e:
        print(f"✗ Error testing ML model: {e}")
        return False
    
    print()
    print("=== Setup Complete ===")
    print("The ML integration is now ready to use!")
    print("You can run the Flask application with: python app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 