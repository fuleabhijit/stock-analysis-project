import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROK_API_KEY = os.getenv("GROK_API_KEY", "")
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True