# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
    GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    MODELO_SELECIONADO = os.getenv('MODELO_SELECIONADO', 'gemini').lower()
    TEMPERATURA = float(os.getenv('TEMPERATURA', 0.1))
    MAX_OUTPUT_TOKENS = int(os.getenv('MAX_OUTPUT_TOKENS', 8192))
    TOP_P = float(os.getenv('TOP_P', 1.0))
    TOP_K = int(os.getenv('TOP_K', 1))
