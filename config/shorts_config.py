"""
Configuración específica para YouTube Shorts.
Optimizada para contenido viral vertical de 15-60 segundos.
"""

# Configuración de Shorts
SHORTS_CONFIG = {
    # Dimensiones y formato
    "resolution": (1080, 1920),  # 9:16 vertical
    "fps": 30,
    "max_duration": 60,  # YouTube Shorts máximo
    "min_duration": 15,  # Mínimo recomendado
    "optimal_duration": 45,  # Duración óptima para engagement
    
    # Configuración de texto para móvil
    "font_size_title": 120,  # Título principal
    "font_size_content": 80,  # Contenido
    "font_size_number": 150,  # Números (TOP 5)
    "text_margin": 100,  # Margen del texto
    "line_height": 1.2,  # Espacio entre líneas
    
    # Colores optimizados para Shorts
    "background_colors": [
        "#000000",  # Negro clásico
        "#1a1a2e",  # Azul oscuro
        "#16213e",  # Azul marino
        "#0f3460",  # Azul profundo
        "#533483",  # Púrpura
    ],
    "text_color": "#ffffff",  # Blanco para contraste
    "accent_colors": [
        "#ff6b6b",  # Rojo vibrante
        "#4ecdc4",  # Turquesa
        "#45b7d1",  # Azul cielo
        "#f9ca24",  # Amarillo
        "#6c5ce7",  # Púrpura vibrante
    ],
    
    # Configuración de audio para Shorts
    "audio_format": "mp3",
    "audio_bitrate": "192k",
    "volume_level": 0.8,  # Volumen óptimo
    
    # Templates específicos para Shorts
    "content_templates": {
        "hook_phrases": [
            "¿Sabías que...?",
            "Esto te va a sorprender",
            "No vas a creer esto",
            "Dato perturbador:",
            "Increíble pero cierto:",
            "Te va a volar la mente:",
        ],
        
        "transition_phrases": [
            "Pero eso no es todo...",
            "Espera, hay más...",
            "Y el número {} te va a impactar",
            "Ahora viene lo bueno...",
            "Prepárate para esto...",
        ],
        
        "cta_phrases": [
            "¡Sígueme para más datos locos!",
            "¿Conocías alguno? ¡Comenta!",
            "Dale like si te sorprendió",
            "¡Sigue para más curiosidades!",
            "¿Cuál te impactó más?",
        ]
    },
    
    # Hashtags optimizados para Shorts
    "hashtags": {
        "general": ["#Shorts", "#Viral", "#Curiosidades", "#DatosCuriosos", "#NoLoSabias"],
        "top5": ["#Top5", "#Ranking", "#LoMejor", "#Increible"],
        "datos": ["#DatosLocos", "#Perturbador", "#Sorprendente", "#Impactante"],
        "ciencia": ["#Ciencia", "#Descubrir", "#Aprender", "#Conocimiento"],
    },
    
    # Configuración de thumbnails para Shorts
    "thumbnail_config": {
        "size": (1080, 1920),  # Mismo formato que el video
        "title_font_size": 100,
        "show_numbers": True,
        "use_emoji": True,
        "contrast_overlay": True,
    },
    
    # Timing optimizado para Shorts
    "timing": {
        "hook_duration": 3,  # Primeros 3 segundos críticos
        "content_per_item": 8,  # 8 segundos por dato
        "transition_time": 0.5,  # Transición entre elementos
        "outro_duration": 5,  # CTA final
    },
    
    # Optimización para algoritmo de Shorts
    "seo_optimization": {
        "title_max_length": 60,  # Caracteres máximos en título
        "description_max_length": 200,  # Descripción corta
        "tags_count": 8,  # Número óptimo de tags
        "include_trending": True,  # Incluir hashtags trending
    }
}

# Plantillas de contenido específicas para Shorts
SHORTS_PROMPTS = {
    "TOP_5_VIRAL": """
    Crea un guión para un SHORT viral de "TOP 5 {topic}" (máximo 45 segundos).
    
    ESTRUCTURA RÍGIDA:
    
    HOOK (3s): "[Frase impactante sobre el tema]"
    
    CONTENIDO (35s):
    5. [Dato sorprendente - 7s]
    4. [Dato más impactante - 7s] 
    3. [Dato increíble - 7s]
    2. [Dato perturbador - 7s]
    1. [Dato que vuela la mente - 7s]
    
    CTA (5s): "[Llamada a la acción viral]"
    
    REQUISITOS:
    - Cada dato debe ser verificable pero sorprendente
    - Usar números exactos cuando sea posible
    - Lenguaje directo, sin florituras
    - Texto grande y fácil de leer
    - Crear suspense hasta el #1
    
    TEMA: {topic}
    """,
    
    "DATOS_LOCOS": """
    Crea un SHORT de "DATOS LOCOS sobre {topic}" (30-45 segundos).
    
    FORMATO:
    
    HOOK (3s): "3 datos sobre {topic} que te van a perturbar"
    
    DATO 1 (12s): [Algo completamente inesperado]
    DATO 2 (15s): [Algo que cambia tu perspectiva] 
    DATO 3 (15s): [Algo que no puedes creer]
    
    CTA (5s): "¿Conocías alguno? ¡Comenta el que más te impactó!"
    
    REQUISITOS:
    - Datos verificables de fuentes confiables
    - Que generen reacciones fuertes
    - Fáciles de compartir y comentar
    - Crear curiosidad para seguir la cuenta
    
    TEMA: {topic}
    """,
    
    "PERTURBADOR": """
    Crea un SHORT "DATOS PERTURBADORES sobre {topic}" (45-60 segundos).
    
    ESTRUCTURA:
    
    HOOK (3s): "Te va a cambiar la forma de ver {topic}"
    
    REVELACIÓN 1 (18s): [Dato que incomoda]
    REVELACIÓN 2 (18s): [Dato más fuerte]
    REVELACIÓN 3 (18s): [Dato que impacta]
    
    CIERRE (3s): "La realidad es más loca de lo que piensas"
    
    REQUISITOS:
    - Datos reales pero inquietantes
    - Que generen debate en comentarios
    - Información poco conocida
    - Balance entre impacto y veracidad
    
    TEMA: {topic}
    """
}

# Configuración de costos optimizada para Shorts
SHORTS_COSTS = {
    "tokens_per_short": 150,  # Menos tokens que videos largos
    "images_per_short": 3,    # Menos imágenes necesarias
    "audio_duration": 45,     # Segundos promedio
    
    "monthly_estimates": {
        "shorts_per_day": 10,
        "days_per_month": 30,
        "total_shorts": 300,
        
        "openai_cost": {
            "gpt4_tokens": 45000,  # 150 tokens × 300 shorts
            "cost_per_1k": 0.03,
            "monthly_total": 1.35
        },
        
        "tts_cost": {
            "edge_tts": 0,  # Gratis
            "elevenlabs_chars": 135000,  # ~450 chars × 300 shorts
            "elevenlabs_cost": 5.40  # $0.00004 por carácter
        },
        
        "total_minimum": 1.35,  # Solo OpenAI
        "total_with_premium": 6.75  # OpenAI + ElevenLabs
    }
}

# Métricas esperadas para Shorts
SHORTS_METRICS = {
    "engagement": {
        "view_rate": "70-85%",  # Shorts tienen mejor retención
        "like_rate": "8-15%",   # Mayor engagement que videos largos
        "comment_rate": "3-8%", # Más comentarios por la naturaleza viral
        "share_rate": "5-12%"   # Más compartibles
    },
    
    "growth": {
        "subscriber_rate": "2-5%",  # % de viewers que se suscriben
        "viral_chance": "15%",      # Probabilidad de volverse viral
        "algorithm_boost": "High"    # Shorts favorecidos por algoritmo
    },
    
    "benchmarks": {
        "month_1": {
            "views_per_short": "100-1K",
            "subscribers": "50-200",
            "total_views": "10K-50K"
        },
        "month_3": {
            "views_per_short": "1K-10K", 
            "subscribers": "500-2K",
            "total_views": "100K-500K"
        },
        "month_6": {
            "views_per_short": "5K-50K",
            "subscribers": "2K-10K", 
            "total_views": "500K-2M"
        }
    }
}