#!/usr/bin/env python3
"""
Test script for ML integration
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_csv_loading():
    """Test CSV data loading"""
    print("Testing CSV data loading...")
    try:
        from load_csv_to_db import load_csv_to_database
        load_csv_to_database()
        print("✓ CSV loading test passed")
        return True
    except Exception as e:
        print(f"✗ CSV loading test failed: {e}")
        return False

def test_ml_model():
    """Test ML model initialization and prediction"""
    print("Testing ML model...")
    try:
        from ml_model_integration import initialize_ml_model, get_risk_prediction
        
        # Initialize model
        success = initialize_ml_model()
        if not success:
            print("✗ ML model initialization failed")
            return False
        
        # Test prediction
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
            print(f"✓ ML model test passed")
            print(f"  Risk: {prediction['risk_percentage']:.2f}%")
            print(f"  Confidence: {prediction['confidence']:.3f}")
            return True
        else:
            print("✗ ML model prediction failed")
            return False
            
    except Exception as e:
        print(f"✗ ML model test failed: {e}")
        return False

def test_flask_integration():
    """Test Flask app integration"""
    print("Testing Flask integration...")
    try:
        from app import app
        print("✓ Flask app import successful")
        return True
    except Exception as e:
        print(f"✗ Flask integration test failed: {e}")
        return False

def main():
    print("=== ML Integration Test ===")
    print()
    
    tests = [
        ("CSV Loading", test_csv_loading),
        ("ML Model", test_ml_model),
        ("Flask Integration", test_flask_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print(f"=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! ML integration is ready.")
        return True
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 