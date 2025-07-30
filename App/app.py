from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
import db_creator
from db_creator import Session, User, Patient, Doktor, Health_data, suggestions
import os
from ml_model_integration import initialize_ml_model, get_risk_prediction

app = Flask(__name__, static_folder='templates', static_url_path='')
app.secret_key = 'supersecretkey'  # Change this in production

db_creator.ignition()

# Initialize ML model on startup
print("Initializing ML model...")
initialize_ml_model()

@app.route('/')
def home():
    return render_template('VitaChech-homepage.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login_page():
    return render_template('giriş-index.html')

@app.route('/giriş-index.html')
def login_page_alt():
    return render_template('giriş-index.html')

@app.route('/doctor-login')
def doctor_login_page():
    return render_template('doktor-index.html')

@app.route('/patient-login')
def patient_login_page():
    return render_template('hasta-index.html')

@app.route('/patient-register')
def patient_register_page():
    return render_template('hasta-register.html')

@app.route('/doctor-homepage')
def doctor_homepage():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect('/doctor-login')
    return render_template('doctor-homepage.html')

@app.route('/patient-homepage')
def patient_homepage():
    if 'user_id' not in session or session.get('is_admin') != 0:
        return redirect('/patient-login')
    return render_template('hasta-homepage.html')

@app.route('/patient-profile')
def patient_profile():
    if 'user_id' not in session or session.get('is_admin') != 0:
        return redirect('/patient-login')
    return render_template('hasta_profile.html')

@app.route('/patient-risk-assessment')
def patient_risk_assessment():
    if 'user_id' not in session or session.get('is_admin') != 0:
        return redirect('/patient-login')
    return render_template('hasta-riskibelirle.html')

@app.route('/patient-risk-results')
def patient_risk_results():
    if 'user_id' not in session or session.get('is_admin') != 0:
        return redirect('/patient-login')
    return render_template('hasta-risksonuçları.html')

@app.route('/patient-reports')
def patient_reports():
    if 'user_id' not in session or session.get('is_admin') != 0:
        return redirect('/patient-login')
    return render_template('hasta-raporlarim.html')

@app.route('/doctor-patients')
def doctor_patients():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect('/doctor-login')
    return render_template('doctor-patients.html')

@app.route('/doctor-profile')
def doctor_profile():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect('/doctor-login')
    return render_template('doktor-profile.html')

@app.route('/doctor-about')
def doctor_about():
    return render_template('doktor-about.html')

@app.route('/doctor-contact')
def doctor_contact():
    return render_template('doktor-contact.html')

@app.route('/doctor-institution')
def doctor_institution():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect('/doctor-login')
    return render_template('doktor-kurumum.html')

@app.route('/doctor-new-patient')
def doctor_new_patient():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return redirect('/doctor-login')
    return render_template('doktor-yeni-hasta.html')

@app.route('/patient-about')
def patient_about():
    return render_template('hasta-about.html')

@app.route('/patient-contact')
def patient_contact():
    return render_template('hasta-contact.html')

@app.route('/patient-doctor')
def patient_doctor():
    if 'user_id' not in session or session.get('is_admin') != 0:
        return redirect('/patient-login')
    return render_template('hastanın-doctor.html')

# Serve static files from templates directory
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)

# User Registration Endpoint (adjusted for form fields)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or request.form
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', 0)
    if not email or not password or not firstname or not lastname:
        return jsonify({'success': False, 'message': 'All fields required.'}), 400
    session_db = Session()
    existing_user = session_db.query(User).filter_by(username=email).first()
    if existing_user:
        session_db.close()
        return jsonify({'success': False, 'message': 'User already exists.'}), 409
    new_user = User(username=email, password=password, is_admin=is_admin)
    session_db.add(new_user)
    session_db.commit()
    # Optionally create Patient record for user
    if is_admin == 0:
        patient = Patient(name=firstname, surname=lastname, user_id=new_user.id)
        session_db.add(patient)
        session_db.commit()
    session_db.close()
    return jsonify({'success': True, 'message': 'User registered successfully.'}), 201

# User Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required.'}), 400
    session_db = Session()
    user = session_db.query(User).filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        session_db.close()
        return jsonify({'success': True, 'message': 'Login successful.'}), 200
    else:
        session_db.close()
        return jsonify({'success': False, 'message': 'Invalid credentials.'}), 401

# User Logout Endpoint
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully.'}), 200

# Patient Profile Update
@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    session_db = Session()
    user = session_db.query(User).filter_by(id=session['user_id']).first()
    if not user:
        session_db.close()
        return jsonify({'success': False, 'message': 'User not found'}), 404
    if name:
        patient = session_db.query(Patient).filter_by(user_id=user.id).first()
        if patient:
            patient.name = name
    if email:
        user.username = email
    if password:
        user.password = password
    session_db.commit()
    session_db.close()
    return jsonify({'success': True, 'message': 'Profile updated'}), 200

# Doctor Profile Update (password only)
@app.route('/doctor/profile/update', methods=['POST'])
def update_doctor_profile():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json() or request.form
    password = data.get('password')
    session_db = Session()
    user = session_db.query(User).filter_by(id=session['user_id']).first()
    if not user:
        session_db.close()
        return jsonify({'success': False, 'message': 'User not found'}), 404
    if password:
        user.password = password
        session_db.commit()
    session_db.close()
    return jsonify({'success': True, 'message': 'Password updated'}), 200

# Feedback/Contact Endpoint
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json() or request.form
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    # For now, just print or log the feedback. In production, store or email it.
    print(f"Feedback from {name} <{email}>: {message}")
    return jsonify({'success': True, 'message': 'Feedback received. Thank you!'}), 200

# 2. Doctor creation (by admin)
@app.route('/doctors', methods=['POST'])
def create_doctor():
    if 'user_id' not in session or session.get('is_admin') != 2:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    user_id = data.get('user_id')
    if not name or not surname or not user_id:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    session_db = Session()
    new_doctor = Doktor(name=name, surname=surname, user_id=user_id)
    session_db.add(new_doctor)
    session_db.commit()
    session_db.close()
    return jsonify({'success': True, 'message': 'Doctor created'}), 201

# 3. Get patient list for doctor
@app.route('/patients', methods=['GET'])
def get_patients():
    if 'user_id' not in session or session.get('is_admin') != 1:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    session_db = Session()
    doctor = session_db.query(Doktor).filter_by(user_id=session['user_id']).first()
    if not doctor:
        session_db.close()
        return jsonify({'success': False, 'message': 'Doctor not found'}), 404
    patients = session_db.query(Patient).filter_by(doktor_id=doctor.id).all()
    result = [{'id': p.id, 'name': p.name, 'surname': p.surname, 'user_id': p.user_id} for p in patients]
    session_db.close()
    return jsonify({'success': True, 'patients': result}), 200

# 4. Get patient details
@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient_details(patient_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    session_db = Session()
    patient = session_db.query(Patient).filter_by(id=patient_id).first()
    if not patient:
        session_db.close()
        return jsonify({'success': False, 'message': 'Patient not found'}), 404
    result = {'id': patient.id, 'name': patient.name, 'surname': patient.surname, 'user_id': patient.user_id, 'doktor_id': patient.doktor_id}
    session_db.close()
    return jsonify({'success': True, 'patient': result}), 200

# 5. Add health data for patient
@app.route('/health_data', methods=['POST'])
def add_health_data():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Missing user_id'}), 400
    session_db = Session()
    health_data = Health_data(**data)
    session_db.add(health_data)
    session_db.commit()
    session_db.close()
    return jsonify({'success': True, 'message': 'Health data added'}), 201

# 6. Get health data for patient
@app.route('/health_data/<int:user_id>', methods=['GET'])
def get_health_data(user_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    session_db = Session()
    health_data = session_db.query(Health_data).filter_by(user_id=user_id).all()
    result = [
        {col.name: getattr(h, col.name) for col in Health_data.__table__.columns}
        for h in health_data
    ]
    session_db.close()
    return jsonify({'success': True, 'health_data': result}), 200

# 7. Add suggestion for patient
@app.route('/suggestions', methods=['POST'])
def add_suggestion():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    data = request.get_json()
    suggestion = data.get('suggestion')
    user_id = data.get('user_id')
    if not suggestion or not user_id:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    session_db = Session()
    new_suggestion = suggestions(suggestion=suggestion, user_id=user_id)
    session_db.add(new_suggestion)
    session_db.commit()
    session_db.close()
    return jsonify({'success': True, 'message': 'Suggestion added'}), 201

# 8. Get suggestions for patient
@app.route('/suggestions/<int:user_id>', methods=['GET'])
def get_suggestions(user_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    session_db = Session()
    suggs = session_db.query(suggestions).filter_by(user_id=user_id).all()
    result = [
        {col.name: getattr(s, col.name) for col in suggestions.__table__.columns}
        for s in suggs
    ]
    session_db.close()
    return jsonify({'success': True, 'suggestions': result}), 200

# Risk assessment endpoint with ML model integration
@app.route('/risk-assessment', methods=['POST'])
def risk_assessment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    session_db = Session()
    
    # Calculate BMI
    weight = data.get('weight', 0)
    height = data.get('height', 0)
    bmi = (weight / ((height/100) ** 2)) if height > 0 else 0
    
    # Determine obesity (BMI > 30)
    obesity = 1 if bmi > 30 else 0
    
    # Prepare data for ML model
    ml_data = {
        'chest_pain': data.get('chest_pain', 0),
        'shortness_of_breath': data.get('shortness_of_breath', 0),
        'fatigue': data.get('fatigue', 0),
        'palpitations': data.get('palpitations', 0),
        'dizziness': data.get('dizziness', 0),
        'swelling': data.get('swelling', 0),
        'radiating_pain': data.get('radiating_pain', 0),
        'cold_sweats': data.get('cold_sweats', 0),
        'hypertension': data.get('hypertension', 0),
        'colestrol_high': data.get('colestrol_high', 0),
        'diabetes': data.get('diabetes', 0),
        'smoker': data.get('smoker', 0),
        'obesity': obesity,
        'family_history': data.get('family_history', 0),
        'sedentary_lifestyle': data.get('sedentary_lifestyle', 0),
        'chronic_stress': data.get('chronic_stress', 0),
        'gender': data.get('gender', 0),
        'age': data.get('age', 50)
    }
    
    # Get ML prediction
    ml_prediction = get_risk_prediction(ml_data)
    
    if ml_prediction:
        # Use ML model prediction
        risk_percentage = ml_prediction['risk_percentage']
        risk_label = ml_prediction['risk_label']
        confidence = ml_prediction['confidence']
        
        # Map ML risk label to risk level (0=low, 1=high)
        if risk_label == 0:
            risk_level = 1  # Low Risk
        else:
            risk_level = 3  # High Risk (could be adjusted based on percentage)
            
        # Adjust risk level based on percentage
        if risk_percentage >= 80:
            risk_level = 4  # Very High Risk
        elif risk_percentage >= 60:
            risk_level = 3  # High Risk
        elif risk_percentage >= 40:
            risk_level = 2  # Medium Risk
        else:
            risk_level = 1  # Low Risk
            
    else:
        # Fallback to original calculation if ML model fails
        risk_score = 0
        risk_factors = [
            data.get('chest_pain', 0),
            data.get('shortness_of_breath', 0),
            data.get('fatigue', 0),
            data.get('palpitations', 0),
            data.get('smoker', 0),
            data.get('diabetes', 0),
            data.get('dizziness', 0),
            data.get('swelling', 0),
            data.get('radiating_pain', 0),
            data.get('cold_sweats', 0),
            data.get('hypertension', 0),
            data.get('colestrol_high', 0),
            obesity,
            data.get('family_history', 0)
        ]
        
        risk_score = sum(risk_factors)
        age_factor = data.get('age', 0) * 0.1
        risk_score += age_factor
        
        # Determine risk level
        if risk_score >= 12:
            risk_level = 4  # Very High Risk
        elif risk_score >= 7:
            risk_level = 3  # High Risk
        elif risk_score >= 4:
            risk_level = 2  # Medium Risk
        else:
            risk_level = 1  # Low Risk
            
        risk_percentage = min(risk_score * 8, 100)  # Convert to percentage
        confidence = 0.7  # Default confidence
    
    # Create health data record
    health_data = Health_data(
        user_id=session['user_id'],
        weight=weight,
        height=height,
        age=data.get('age', 0),
        gender=data.get('gender', ''),
        chest_pain=data.get('chest_pain', 0),
        shortness_of_breath=data.get('shortness_of_breath', 0),
        fatigue=data.get('fatigue', 0),
        palpitations=data.get('palpitations', 0),
        smoker=data.get('smoker', 0),
        diabetes=data.get('diabetes', 0),
        dizziness=data.get('dizziness', 0),
        swelling=data.get('swelling', 0),
        radiating_pain=data.get('radiating_pain', 0),
        cold_sweats=data.get('cold_sweats', 0),
        hypertension=data.get('hypertension', 0),
        colestrol_high=data.get('colestrol_high', 0),
        obesity=obesity,
        family_history=data.get('family_history', 0),
        risk_label=risk_level
    )
    
    session_db.add(health_data)
    session_db.commit()
    session_db.close()
    
    return jsonify({
        'success': True, 
        'risk_score': risk_percentage,
        'risk_level': risk_level,
        'bmi': round(bmi, 2),
        'confidence': round(confidence, 3),
        'ml_prediction': ml_prediction is not None
    }), 200

# Get current user info
@app.route('/user/info', methods=['GET'])
def get_user_info():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    session_db = Session()
    user = session_db.query(User).filter_by(id=session['user_id']).first()
    if not user:
        session_db.close()
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    user_info = {
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    }
    
    if user.is_admin == 0:  # Patient
        patient = session_db.query(Patient).filter_by(user_id=user.id).first()
        if patient:
            user_info.update({
                'name': patient.name,
                'surname': patient.surname,
                'patient_id': patient.id
            })
    elif user.is_admin == 1:  # Doctor
        doctor = session_db.query(Doktor).filter_by(user_id=user.id).first()
        if doctor:
            user_info.update({
                'name': doctor.name,
                'surname': doctor.surname,
                'doctor_id': doctor.id
            })
    
    session_db.close()
    return jsonify({'success': True, 'user': user_info}), 200

if __name__ == '__main__':
    try:
        print("Starting VitaCheck Healthcare Management System...")
        print("Access the application at: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down VitaCheck...")
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Please check if port 5000 is available and try again.") 