"""
Configuración principal del sistema de automatización de YouTube.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, List

# Cargar variables de entorno
load_dotenv()

# Configuración de localización
try:
    from .localization import (
        DEFAULT_LANGUAGE, DEFAULT_THEME, 
        get_current_config, get_language_config, 
        get_theme_config, get_localized_texts
    )
except ImportError:
    # Fallback si localization no está disponible
    DEFAULT_LANGUAGE = "es"
    DEFAULT_THEME = "curiosidades"
    def get_language_config(lang=None):
        return {"voice": "es-ES-AlvaroNeural", "voice_female": "es-ES-ElviraNeural"}

class Settings:
    """Configuración de la aplicación."""
    
    def __init__(self):
        # Configuración de localización
        self.LANGUAGE = os.getenv("CONTENT_LANGUAGE", DEFAULT_LANGUAGE)
        self.THEME = os.getenv("CONTENT_THEME", DEFAULT_THEME)
        
        # Rutas del proyecto
        self.PROJECT_ROOT = Path(__file__).parent.parent
        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.ASSETS_DIR = self.PROJECT_ROOT / "assets"
        self.TEMPLATES_DIR = self.PROJECT_ROOT / "templates"
        self.OUTPUT_DIR = self.PROJECT_ROOT / "output"
        
        # APIs de IA
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
        self.OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        
        self.ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
        self.ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
        
        # Configuración TTS localizada
        try:
            lang_config = get_language_config(self.LANGUAGE)
            self.TTS_VOICE = os.getenv("TTS_VOICE", lang_config.get("voice", "es-ES-AlvaroNeural"))
            self.TTS_VOICE_FEMALE = lang_config.get("voice_female", "es-ES-ElviraNeural")
        except:
            self.TTS_VOICE = "es-ES-AlvaroNeural"
            self.TTS_VOICE_FEMALE = "es-ES-ElviraNeural"
        
        # YouTube API
        self.YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
        self.YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
        self.YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
        self.YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")
        
        # APIs de multimedia
        self.UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
        self.UNSPLASH_SECRET_KEY = os.getenv("UNSPLASH_SECRET_KEY", "")
        self.PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
        
        # Base de datos
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/youtube_automation.db")
        
        # Configuración de contenido
        self.CONTENT_LANGUAGE = os.getenv("CONTENT_LANGUAGE", "es")
        self.CONTENT_COUNTRY = os.getenv("CONTENT_COUNTRY", "ES")
        
        # Configuración de video para YouTube Shorts
        self.VIDEO_RESOLUTION = os.getenv("VIDEO_RESOLUTION", "1080x1920")  # Formato vertical 9:16
        self.VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))
        self.VIDEO_DURATION_MIN = int(os.getenv("VIDEO_DURATION_MIN", "15"))   # 15 segundos mínimo
        self.VIDEO_DURATION_MAX = int(os.getenv("VIDEO_DURATION_MAX", "60"))   # 60 segundos máximo
        
        # Programación
        self.PUBLISH_SCHEDULE = os.getenv("PUBLISH_SCHEDULE", "0 10,18 * * *")
        
        # N8N (opcional)
        self.N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")
        self.N8N_API_KEY = os.getenv("N8N_API_KEY", "")
        
        # Debug
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.SAVE_INTERMEDIATE_FILES = os.getenv("SAVE_INTERMEDIATE_FILES", "True").lower() == "true"
        
        # Rate limiting
        self.RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
        self.RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

# Instancia global de configuración
settings = Settings()

# Crear directorios necesarios
for directory in [
    settings.DATA_DIR,
    settings.ASSETS_DIR, 
    settings.OUTPUT_DIR
]:
    directory.mkdir(exist_ok=True)

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': settings.LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': settings.DATA_DIR / 'app.log',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# Plantillas de prompts para diferentes tipos de contenido
CONTENT_TEMPLATES = {
    "TOP_5": {
        "system_prompt": """Eres un experto creador de contenido para YouTube especializado en listas TOP 5 en español. 
        Crea contenido viral, interesante y bien estructurado que enganche a la audiencia hispana.""",
        
        "user_prompt": """Crea un guión para un YouTube SHORT sobre "TOP 5 {topic}" (máximo 60 segundos).

        REQUISITOS PARA SHORTS:
        1. Título llamativo con números (#Shorts #Top5)
        2. Hook inicial de 3 segundos que enganche
        3. 5 elementos rápidos (10-12 segundos cada uno)
        4. Datos impactantes y sorprendentes
        5. Texto grande y legible para móvil
        6. Duración total: 45-60 segundos
        7. Lenguaje: español dinámico, directo
        8. Call-to-action final (sigue para más)

        ESTRUCTURA SHORTS:
        - Hook (3s): "¿Sabías que...?"
        - Top 5 elementos (40-50s)
        - CTA final (5-7s): "¡Sígueme para más!"
        - Hashtags: #Shorts #Top5 #Curiosidades

        TEMA: {topic}
        FORMATO: Vertical, móvil-first
        TONO: Rápido, impactante, viral
        """
    },
    
    "CURIOSIDADES": {
        "system_prompt": """Eres un divulgador científico y cultural experto en crear contenido de curiosidades 
        fascinantes para YouTube en español.""",
        
        "user_prompt": """Crea un guión para un SHORT de curiosidades sobre "{topic}" (máximo 60 segundos).

        REQUISITOS PARA SHORTS:
        1. 3-5 curiosidades ultra impactantes
        2. Datos verificables pero sorprendentes
        3. Frases cortas, fáciles de leer
        4. Elementos visuales llamativos
        5. Ritmo muy rápido y adictivo
        6. Duración: 30-60 segundos
        7. Texto overlay para cada dato

        ESTRUCTURA SHORTS:
        - Hook viral (3-5s): "Esto te va a volar la mente"
        - 3-4 curiosidades rápidas (40-50s)
        - Cierre impactante (5-7s)
        - Hashtags virales

        FORMATO: Vertical, texto grande
        TEMA: {topic}
        TONO: Impactante, adictivo, compartible
        """
    }
}

# Configuración de APIs externas
API_ENDPOINTS = {
    "TRENDING": {
        "google_trends": "https://trends.google.com/trends/api",
        "youtube_trending": "https://www.googleapis.com/youtube/v3/videos"
    },
    "IMAGES": {
        "unsplash": "https://api.unsplash.com",
        "pexels": "https://api.pexels.com/v1"
    },
    "TTS": {
        "elevenlabs": "https://api.elevenlabs.io/v1",
        "edge_tts": "edge-tts"  # Servicio local
    }
}