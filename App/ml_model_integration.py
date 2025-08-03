import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

class HeartDiseasePredictor:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.is_trained = False

    def train_model(self, csv_path='heart.csv'):
        """Train the machine learning model using Gradient Boosting only"""
        try:
            # Load the data
            df = pd.read_csv(csv_path)
            print(f"Data loaded successfully. Shape: {df.shape}")

            # Separate features and target
            X = df.drop('Heart_Risk', axis=1)
            y = df['Heart_Risk']

            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Define numerical features (only Age in this case)
            numerical_features = ['Age']

            # Create preprocessor
            self.preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(), numerical_features),
                ],
                remainder='passthrough'
            )

            # Use only Gradient Boosting
            self.model = Pipeline([
                ('preprocessor', self.preprocessor),
                ('classifier', GradientBoostingClassifier(random_state=42))
            ])

            # Train the model
            print("Training Gradient Boosting model...")
            self.model.fit(X_train, y_train)

            # Evaluate the model
            y_pred = self.model.predict(X_test)
            y_pred_proba = self.model.predict_proba(X_test)[:, 1]

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred_proba)

            print(f"Model Performance:")
            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  Precision: {precision:.4f}")
            print(f"  Recall: {recall:.4f}")
            print(f"  F1-Score: {f1:.4f}")
            print(f"  ROC AUC: {roc_auc:.4f}")

            # Save the model
            joblib.dump(self.model, 'heart_disease_model.pkl')
            print("Model saved as 'heart_disease_model.pkl'")

            # --- TEST: Predict with all-1s input (high-risk scenario) ---
            test_input = pd.DataFrame({
                'Chest_Pain': [1],
                'Shortness_of_Breath': [1],
                'Fatigue': [1],
                'Palpitations': [1],
                'Dizziness': [1],
                'Swelling': [1],
                'Pain_Arms_Jaw_Back': [1],
                'Cold_Sweats_Nausea': [1],
                'High_BP': [1],
                'High_Cholesterol': [1],
                'Diabetes': [1],
                'Smoking': [1],
                'Obesity': [1],
                'Sedentary_Lifestyle': [1],
                'Family_History': [1],
                'Chronic_Stress': [1],
                'Gender': [1],
                'Age': [60]
            })
            test_proba = self.model.predict_proba(test_input)[0]
            print(f"\n[TEST] All-1s input prediction: Probabilities={test_proba}, Risk%={test_proba[1]*100:.2f}%\n")

            self.is_trained = True
            return True

        except Exception as e:
            print(f"Error training model: {e}")
            return False

    def load_model(self, model_path='heart_disease_model.pkl'):
        """Load a trained model"""
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                self.is_trained = True
                print("Model loaded successfully")
                return True
            else:
                print(f"Model file {model_path} not found")
                return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def predict_risk(self, user_data):
        """Predict heart disease risk for a user"""
        if not self.is_trained or self.model is None:
            print("Model not trained or loaded")
            return None

        try:
            # Convert user data to the expected format
            model_input = pd.DataFrame({
                'Chest_Pain': [user_data.get('chest_pain', 0)],
                'Shortness_of_Breath': [user_data.get('shortness_of_breath', 0)],
                'Fatigue': [user_data.get('fatigue', 0)],
                'Palpitations': [user_data.get('palpitations', 0)],
                'Dizziness': [user_data.get('dizziness', 0)],
                'Swelling': [user_data.get('swelling', 0)],
                'Pain_Arms_Jaw_Back': [user_data.get('radiating_pain', 0)],
                'Cold_Sweats_Nausea': [user_data.get('cold_sweats', 0)],
                'High_BP': [user_data.get('hypertension', 0)],
                'High_Cholesterol': [user_data.get('colestrol_high', 0)],
                'Diabetes': [user_data.get('diabetes', 0)],
                'Smoking': [user_data.get('smoker', 0)],
                'Obesity': [user_data.get('obesity', 0)],
                'Sedentary_Lifestyle': [user_data.get('sedentary_lifestyle', 0)],
                'Family_History': [user_data.get('family_history', 0)],
                'Chronic_Stress': [user_data.get('chronic_stress', 0)],
                'Gender': [user_data.get('gender', 0)],
                'Age': [user_data.get('age', 50)]
            })

            # Make prediction
            prediction_proba = self.model.predict_proba(model_input)[0]
            prediction_label = self.model.predict(model_input)[0]

            # Calculate risk percentage - this is the probability of high risk (class 1)
            risk_percentage = prediction_proba[1] * 100

            # Debug information
            print(f"Debug - Input data: {user_data}")
            print(f"Debug - Model input shape: {model_input.shape}")
            print(f"Debug - Prediction probabilities: {prediction_proba}")
            print(f"Debug - Prediction label: {prediction_label}")
            print(f"Debug - Risk percentage: {risk_percentage:.2f}%")

            return {
                'risk_percentage': risk_percentage,
                'risk_label': int(prediction_label),
                'confidence': max(prediction_proba),
                'low_risk_prob': prediction_proba[0],
                'high_risk_prob': prediction_proba[1]
            }

        except Exception as e:
            print(f"Error making prediction: {e}")
            return None

# Global predictor instance
predictor = HeartDiseasePredictor()

def initialize_ml_model():
    """Initialize the ML model - train if needed, otherwise load"""
    if os.path.exists('heart_disease_model.pkl'):
        print("Loading existing model...")
        return predictor.load_model()
    else:
        print("Training new model...")
        return predictor.train_model()

def get_risk_prediction(user_data):
    """Get risk prediction for user data"""
    return predictor.predict_risk(user_data) 