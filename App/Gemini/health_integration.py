import sys
import os
from typing import Dict, Any
from pathlib import Path

# Add the parent directory to the path to import ml_model_integration
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model_integration import predictor
from .health_advisor import get_health_advice, create_health_report

class HealthAdvisorIntegration:
    """
    Integration class that combines ML risk prediction with AI-powered health advice.
    Focuses on exercise recommendations and general health advice.
    """
    
    def __init__(self):
        self.predictor = predictor
        self.is_initialized = False
    
    def initialize(self):
        """Initialize the ML model"""
        try:
            if not self.predictor.is_trained:
                self.predictor.train_model()
            self.is_initialized = True
            print("Health Advisor Integration initialized successfully")
        except Exception as e:
            print(f"Error initializing Health Advisor Integration: {e}")
            self.is_initialized = False
    
    def get_comprehensive_health_analysis(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive health analysis including risk prediction and exercise recommendations.
        
        Args:
            user_data: Dictionary containing user health parameters
            
        Returns:
            Dictionary containing risk assessment and health advice
        """
        if not self.is_initialized:
            self.initialize()
        
        try:
            # Get risk prediction
            risk_data = self.predictor.predict_risk(user_data)
            
            # Get health advice based on risk
            health_advice = get_health_advice(risk_data, user_data)
            
            return {
                "risk_assessment": risk_data,
                "health_advice": health_advice,
                "timestamp": "2024-01-01T00:00:00Z"
            }
            
        except Exception as e:
            return {
                "error": f"Error in comprehensive health analysis: {str(e)}",
                "user_data": user_data
            }
    
    def get_quick_health_summary(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a quick health summary with risk assessment and basic recommendations.
        
        Args:
            user_data: Dictionary containing user health parameters
            
        Returns:
            Dictionary containing risk summary and basic health advice
        """
        if not self.is_initialized:
            self.initialize()
        
        try:
            # Get risk prediction
            risk_data = self.predictor.predict_risk(user_data)
            
            # Get basic health advice
            health_advice = get_health_advice(risk_data, user_data)
            
            return {
                "risk_summary": {
                    "risk_level": risk_data.get('risk_label', 0),
                    "risk_percentage": risk_data.get('risk_percentage', 0),
                    "confidence": risk_data.get('confidence', 0)
                },
                "main_recommendations": [
                    "Düzenli kardiyovasküler egzersiz",
                    "Güçlendirme egzersizleri", 
                    "Esneklik ve denge egzersizleri",
                    "Sağlıklı yaşam tarzı değişiklikleri"
                ],
                "health_advice": health_advice
            }
            
        except Exception as e:
            return {
                "error": f"Error in quick health summary: {str(e)}",
                "user_data": user_data
            }

# Create a global instance
health_integration = HealthAdvisorIntegration()

# Convenience functions for easy integration
def get_health_analysis(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get comprehensive health analysis including risk prediction and exercise recommendations.
    
    Args:
        user_data: Dictionary containing user health parameters
        
    Returns:
        Dictionary containing risk assessment and health advice
    """
    return health_integration.get_comprehensive_health_analysis(user_data)

def get_health_summary(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a quick health summary with risk assessment and basic recommendations.
    
    Args:
        user_data: Dictionary containing user health parameters
        
    Returns:
        Dictionary containing risk summary and basic health advice
    """
    return health_integration.get_quick_health_summary(user_data)

def get_exercise_recommendations(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get exercise recommendations based on risk assessment.
    
    Args:
        user_data: Dictionary containing user health parameters
        
    Returns:
        Dictionary containing exercise recommendations
    """
    analysis = get_health_analysis(user_data)
    
    if "error" in analysis:
        return analysis
    
    # Extract exercise recommendations from health advice
    health_advice = analysis.get("health_advice", {})
    exercise_recommendations = health_advice.get("exercise_recommendations", {})
    
    return {
        "risk_assessment": analysis.get("risk_assessment", {}),
        "exercise_recommendations": exercise_recommendations,
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Example usage
if __name__ == "__main__":
    # Example user data
    example_user_data = {
        'age': 45,
        'gender': 1,  # Male
        'chest_pain': 0,
        'shortness_of_breath': 0,
        'fatigue': 1,
        'palpitations': 0,
        'dizziness': 0,
        'swelling': 0,
        'radiating_pain': 0,
        'cold_sweats': 0,
        'hypertension': 1,
        'colestrol_high': 1,
        'diabetes': 0,
        'smoker': 0,
        'obesity': 1,
        'sedentary_lifestyle': 1,
        'family_history': 1,
        'chronic_stress': 1
    }
    
    # Initialize the integration
    if health_integration.initialize():
        print("Testing health analysis...")
        
        # Get comprehensive analysis
        analysis = get_health_analysis(example_user_data)
        print("Comprehensive Analysis:", analysis)
        
        # Get quick summary
        summary = get_health_summary(example_user_data)
        print("Quick Summary:", summary)
        
        # Get exercise recommendations
        exercise_recommendations = get_exercise_recommendations(example_user_data)
        print("Exercise Recommendations:", exercise_recommendations)
    else:
        print("Failed to initialize health integration") 