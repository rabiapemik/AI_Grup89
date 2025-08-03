import os
from dotenv import load_dotenv

# .env klasörünü yükle
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env', 'gemini_keys.env')
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    raise RuntimeError("GEMINI_API_KEY bulunamadı. .env dosyasını kontrol edin.")
