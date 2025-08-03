from flask import Flask, request, jsonify
from .health_integration import get_health_analysis, get_health_summary, get_exercise_recommendations

app = Flask(__name__)

@app.route('/health/analysis', methods=['POST'])
def health_analysis():
    """
    Get comprehensive health analysis including risk prediction and exercise recommendations.
    
    Expected JSON input:
    {
        "age": 45,
        "gender": 1,
        "chest_pain": 0,
        "resting_bp": 140,
        "cholesterol": 200,
        "fasting_bs": 0,
        "resting_ecg": 0,
        "max_hr": 150,
        "exercise_angina": 0,
        "oldpeak": 0.0,
        "st_slope": 0
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'chest_pain', 'resting_bp', 'cholesterol', 
                         'fasting_bs', 'resting_ecg', 'max_hr', 'exercise_angina', 
                         'oldpeak', 'st_slope']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Get comprehensive health analysis
        result = get_health_analysis(data)
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health/summary', methods=['POST'])
def health_summary():
    """
    Get a quick health summary with risk assessment and basic recommendations.
    
    Expected JSON input:
    {
        "age": 45,
        "gender": 1,
        "chest_pain": 0,
        "resting_bp": 140,
        "cholesterol": 200,
        "fasting_bs": 0,
        "resting_ecg": 0,
        "max_hr": 150,
        "exercise_angina": 0,
        "oldpeak": 0.0,
        "st_slope": 0
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'chest_pain', 'resting_bp', 'cholesterol', 
                         'fasting_bs', 'resting_ecg', 'max_hr', 'exercise_angina', 
                         'oldpeak', 'st_slope']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Get health summary
        result = get_health_summary(data)
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health/exercise-recommendations', methods=['POST'])
def exercise_recommendations():
    """
    Get exercise recommendations based on risk assessment.
    
    Expected JSON input:
    {
        "age": 45,
        "gender": 1,
        "chest_pain": 0,
        "resting_bp": 140,
        "cholesterol": 200,
        "fasting_bs": 0,
        "resting_ecg": 0,
        "max_hr": 150,
        "exercise_angina": 0,
        "oldpeak": 0.0,
        "st_slope": 0
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'chest_pain', 'resting_bp', 'cholesterol', 
                         'fasting_bs', 'resting_ecg', 'max_hr', 'exercise_angina', 
                         'oldpeak', 'st_slope']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {missing_fields}"}), 400
        
        # Get exercise recommendations
        result = get_exercise_recommendations(data)
        
        if "error" in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health/status', methods=['GET'])
def health_status():
    """
    Health check endpoint to verify the service is running.
    """
    return jsonify({
        "status": "healthy",
        "service": "Health Advisor API",
        "version": "1.0.0",
        "endpoints": [
            "/health/analysis",
            "/health/summary", 
            "/health/exercise-recommendations",
            "/health/status"
        ]
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 