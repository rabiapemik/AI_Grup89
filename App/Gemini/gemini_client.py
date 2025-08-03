import google.generativeai as genai
from config import GEMINI_API_KEY

# API anahtarını tanımla
genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str, model_name: str = "gemini-1.5-flash", temperature: float = 0.7, max_tokens: int = 800) -> dict:
    #Verilen prompt'u Gemini'ye sorar, JSON cevabı döner.
    model = genai.GenerativeModel(model_name)
    chat = model.start_chat()
    response = chat.send_message(
        prompt
    )
    
    return response.to_dict()
