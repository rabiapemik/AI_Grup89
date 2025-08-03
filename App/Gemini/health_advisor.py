import json
import re
from typing import Dict, Any, List
from gemini_client import ask_gemini

def health_advice_prompt(risk_data: Dict[str, Any], user_profile: Dict[str, Any] = None) -> str:
    """
    Generate a prompt for comprehensive health advice based on risk data.
    Focuses on exercise recommendations and general health advice.
    """
    risk_level = "Yüksek" if risk_data.get('risk_label', 0) == 1 else "Düşük"
    risk_percentage = risk_data.get('risk_percentage', 0)
    confidence = risk_data.get('confidence', 0)
    
    user_info = ""
    if user_profile:
        age = user_profile.get('age', 'Bilinmiyor')
        gender = user_profile.get('gender', 'Bilinmiyor')
        weight = user_profile.get('weight', 'Bilinmiyor')
        height = user_profile.get('height', 'Bilinmiyor')
        user_info = f"""
Kullanıcı Profili:
- Yaş: {age}
- Cinsiyet: {gender}
- Kilo: {weight} kg
- Boy: {height} cm
"""

    prompt = f"""
Sen bir sağlık danışmanısın. Kullanıcının kalp hastalığı risk analizi sonuçlarına göre kişiselleştirilmiş sağlık önerileri ver.

Risk Analizi Sonuçları:
- Risk Seviyesi: {risk_level}
- Risk Yüzdesi: %{risk_percentage:.1f}
- Güvenilirlik: %{confidence:.1f}
{user_info}

Lütfen aşağıdaki JSON formatında kapsamlı sağlık önerileri ver:

{{
    "risk_assessment": {{
        "risk_level": "{risk_level}",
        "risk_percentage": {risk_percentage},
        "confidence": {confidence},
        "interpretation": "Risk seviyesinin açıklaması"
    }},
    "exercise_recommendations": {{
        "cardio_exercises": [
            {{
                "name": "Egzersiz adı",
                "duration": "Süre (dakika)",
                "frequency": "Haftada kaç kez",
                "intensity": "Yoğunluk seviyesi",
                "benefits": "Faydaları",
                "precautions": "Dikkat edilmesi gerekenler"
            }}
        ],
        "strength_training": [
            {{
                "name": "Egzersiz adı",
                "sets": "Set sayısı",
                "reps": "Tekrar sayısı",
                "frequency": "Haftada kaç kez",
                "benefits": "Faydaları",
                "precautions": "Dikkat edilmesi gerekenler"
            }}
        ],
        "flexibility_exercises": [
            {{
                "name": "Egzersiz adı",
                "duration": "Süre",
                "frequency": "Haftada kaç kez",
                "benefits": "Faydaları"
            }}
        ],
        "weekly_plan": {{
            "monday": ["Egzersiz listesi"],
            "tuesday": ["Egzersiz listesi"],
            "wednesday": ["Egzersiz listesi"],
            "thursday": ["Egzersiz listesi"],
            "friday": ["Egzersiz listesi"],
            "saturday": ["Egzersiz listesi"],
            "sunday": ["Dinlenme veya hafif aktivite"]
        }}
    }},
    "lifestyle_recommendations": {{
        "daily_activities": [
            "Günlük aktivite önerileri"
        ],
        "stress_management": [
            "Stres yönetimi teknikleri"
        ],
        "sleep_hygiene": [
            "Uyku düzeni önerileri"
        ],
        "smoking_alcohol": [
            "Sigara ve alkol konusunda öneriler"
        ]
    }},
    "health_monitoring": {{
        "vital_signs": [
            "Takip edilmesi gereken vital bulgular"
        ],
        "warning_signs": [
            "Dikkat edilmesi gereken uyarı işaretleri"
        ],
        "follow_up": [
            "Düzenli kontrol önerileri"
        ]
    }},
    "emergency_guidance": {{
        "when_to_seek_help": [
            "Acil durum belirtileri"
        ],
        "emergency_contacts": [
            "Acil durum iletişim bilgileri"
        ]
    }}
}}

Önemli Notlar:
1. Risk seviyesine göre egzersiz yoğunluğunu ayarla
2. Güvenli ve etkili egzersizler öner
3. Kullanıcının yaş ve sağlık durumuna uygun öneriler ver
4. Türkçe olarak yanıt ver
5. Sadece JSON formatında yanıt ver, ek açıklama ekleme
"""

    return prompt

def parse_health_advice_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the Gemini response and extract structured health advice
    """
    try:
        # Extract text content from Gemini response
        candidate = response["candidates"][0]
        content = candidate["content"]
        
        if isinstance(content, dict) and "parts" in content:
            raw_text = "".join(part.get("text", "") for part in content["parts"])
        else:
            raw_text = str(content)
        
        # Extract JSON from the response
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            raise ValueError("Could not parse JSON from Gemini response")
        
        data = json.loads(match.group(0))
        return data
        
    except Exception as e:
        print(f"Error parsing health advice response: {e}")
        return {
            "error": "Failed to parse health advice",
            "raw_response": raw_text if 'raw_text' in locals() else str(response)
        }

def get_health_advice(risk_data: Dict[str, Any], user_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get comprehensive health advice based on risk data.
    Focuses on exercise recommendations and general health advice.
    """
    try:
        prompt = health_advice_prompt(risk_data, user_profile)
        response = ask_gemini(prompt)
        
        # Extract the text content from the response
        if 'candidates' in response and len(response['candidates']) > 0:
            content = response['candidates'][0]['content']['parts'][0]['text']
            
            # Try to parse as JSON
            import json
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, return a structured error response
                return {
                    "error": "AI response could not be parsed as JSON",
                    "raw_response": content,
                    "risk_data": risk_data
                }
        else:
            return {
                "error": "No response from AI",
                "risk_data": risk_data
            }
            
    except Exception as e:
        return {
            "error": f"Error getting health advice: {str(e)}",
            "risk_data": risk_data
        }

def create_health_report(risk_data: Dict[str, Any], user_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Create a comprehensive health report focusing on exercise recommendations.
    """
    health_advice = get_health_advice(risk_data, user_profile)
    
    return {
        "timestamp": "2024-01-01T00:00:00Z",
        "risk_data": risk_data,
        "user_profile": user_profile,
        "health_advice": health_advice,
        "summary": {
            "risk_level": risk_data.get('risk_label', 0),
            "risk_percentage": risk_data.get('risk_percentage', 0),
            "main_recommendations": [
                "Düzenli kardiyovasküler egzersiz",
                "Güçlendirme egzersizleri",
                "Esneklik ve denge egzersizleri",
                "Sağlıklı yaşam tarzı değişiklikleri"
            ]
        }
    } 