"""
Configuración de Localización y Temas
Sistema configurable para diferentes idiomas y temáticas de contenido.
"""

# ===== CONFIGURACIÓN PRINCIPAL =====

# Idioma principal del contenido
DEFAULT_LANGUAGE = "es"  # Español
# Opciones: "es", "en", "fr", "pt", "it", "de"

# Temática principal del canal
DEFAULT_THEME = "curiosidades"
# Opciones: "curiosidades", "tecnologia", "historia", "ciencia", "deportes", "entretenimiento"

# ===== CONFIGURACIÓN POR IDIOMAS =====

LANGUAGES_CONFIG = {
    "es": {
        "name": "Español",
        "voice": "es-ES-AlvaroNeural",  # Voz masculina española
        "voice_female": "es-ES-ElviraNeural",  # Voz femenina española
        "country": "España",
        "currency": "EUR",
        "date_format": "%d/%m/%Y"
    },
    "en": {
        "name": "English",
        "voice": "en-US-ChristopherNeural",
        "voice_female": "en-US-JennyNeural",
        "country": "United States",
        "currency": "USD",
        "date_format": "%m/%d/%Y"
    },
    "pt": {
        "name": "Português",
        "voice": "pt-BR-AntonioNeural",
        "voice_female": "pt-BR-FranciscaNeural",
        "country": "Brasil",
        "currency": "BRL",
        "date_format": "%d/%m/%Y"
    },
    "fr": {
        "name": "Français",
        "voice": "fr-FR-HenriNeural",
        "voice_female": "fr-FR-DeniseNeural", 
        "country": "France",
        "currency": "EUR",
        "date_format": "%d/%m/%Y"
    },
    "it": {
        "name": "Italiano",
        "voice": "it-IT-DiegoNeural",
        "voice_female": "it-IT-ElsaNeural",
        "country": "Italia",
        "currency": "EUR",
        "date_format": "%d/%m/%Y"
    },
    "de": {
        "name": "Deutsch",
        "voice": "de-DE-ConradNeural",
        "voice_female": "de-DE-KatjaNeural",
        "country": "Deutschland",
        "currency": "EUR",
        "date_format": "%d.%m.%Y"
    }
}

# ===== CONFIGURACIÓN POR TEMAS =====

THEMES_CONFIG = {
    "curiosidades": {
        "es": {
            "channel_name": "Datos Increíbles",
            "description": "Curiosidades y datos sorprendentes del mundo",
            "tags_base": ["curiosidades", "datos", "increible", "sorprendente", "viral"],
            "content_types": ["TOP_5", "CURIOSIDADES", "DATOS_LOCOS"],
            "topics_pool": [
                "animales más extraños del mundo",
                "lugares más peligrosos de la Tierra", 
                "inventos más raros de la historia",
                "comidas más caras del planeta",
                "países con leyes más extrañas"
            ]
        },
        "en": {
            "channel_name": "Mind-Blowing Facts",
            "description": "Amazing curiosities and surprising facts",
            "tags_base": ["facts", "amazing", "incredible", "surprising", "viral"],
            "content_types": ["TOP_5", "CURIOSITIES", "CRAZY_FACTS"],
            "topics_pool": [
                "strangest animals in the world",
                "most dangerous places on Earth",
                "weirdest inventions in history", 
                "most expensive foods on the planet",
                "countries with strangest laws"
            ]
        }
    },
    "tecnologia": {
        "es": {
            "channel_name": "Tech Viral",
            "description": "Lo último en tecnología e innovación",
            "tags_base": ["tecnologia", "innovation", "gadgets", "futuro", "viral"],
            "content_types": ["TOP_5", "TECH_NEWS", "GADGETS"],
            "topics_pool": [
                "gadgets más innovadores de 2024",
                "aplicaciones que cambiarán tu vida",
                "inventos tecnológicos del futuro",
                "robots más avanzados del mundo",
                "inteligencia artificial más potente"
            ]
        },
        "en": {
            "channel_name": "Tech Viral",
            "description": "Latest in technology and innovation",
            "tags_base": ["technology", "innovation", "gadgets", "future", "viral"],
            "content_types": ["TOP_5", "TECH_NEWS", "GADGETS"],
            "topics_pool": [
                "most innovative gadgets of 2024",
                "apps that will change your life",
                "technological inventions of the future",
                "most advanced robots in the world",
                "most powerful artificial intelligence"
            ]
        }
    },
    "historia": {
        "es": {
            "channel_name": "Historia Viral",
            "description": "Hechos históricos fascinantes y secretos del pasado",
            "tags_base": ["historia", "pasado", "secretos", "misterios", "viral"],
            "content_types": ["TOP_5", "MISTERIOS", "SECRETOS"],
            "topics_pool": [
                "secretos mejor guardados de la historia",
                "batallas más épicas de la humanidad",
                "inventos que cambiaron el mundo",
                "personajes más influyentes de la historia",
                "civilizaciones perdidas más misteriosas"
            ]
        },
        "en": {
            "channel_name": "Viral History",
            "description": "Fascinating historical facts and secrets from the past",
            "tags_base": ["history", "past", "secrets", "mysteries", "viral"],
            "content_types": ["TOP_5", "MYSTERIES", "SECRETS"],
            "topics_pool": [
                "best kept secrets in history",
                "most epic battles in humanity",
                "inventions that changed the world",
                "most influential people in history",
                "most mysterious lost civilizations"
            ]
        }
    }
}

# ===== TEXTOS LOCALIZADOS =====

LOCALIZED_TEXTS = {
    "es": {
        "intro_phrases": [
            "¿Sabías que...",
            "Te vas a sorprender con...",
            "No vas a creer...",
            "Esto te va a impactar...",
            "Prepárate para...",
        ],
        "transition_phrases": [
            "Pero eso no es todo...",
            "Y ahora viene lo mejor...",
            "Espera porque falta lo más loco...",
            "Pero hay algo aún más impactante...",
            "Y el siguiente te va a dejar sin palabras...",
        ],
        "outro_phrases": [
            "¡Dale like si te sorprendió!",
            "¿Conocías estos datos? ¡Comenta!",
            "¡Suscríbete para más contenido así!",
            "¡Comparte si te gustó!",
            "¿Cuál te impactó más? ¡Dímelo en comentarios!",
        ],
        "numbers": ["Primero", "Segundo", "Tercero", "Cuarto", "Quinto"],
        "hashtags": ["#Shorts", "#Viral", "#Curiosidades", "#DatosIncreibles", "#Sabias"]
    },
    "en": {
        "intro_phrases": [
            "Did you know that...",
            "You'll be amazed by...",
            "You won't believe...",
            "This will blow your mind...",
            "Get ready for...",
        ],
        "transition_phrases": [
            "But that's not all...",
            "And now comes the best part...",
            "Wait because the craziest is yet to come...",
            "But there's something even more shocking...",
            "And the next one will leave you speechless...",
        ],
        "outro_phrases": [
            "Hit like if this amazed you!",
            "Did you know these facts? Comment!",
            "Subscribe for more content like this!",
            "Share if you liked it!",
            "Which one shocked you most? Tell me in comments!",
        ],
        "numbers": ["First", "Second", "Third", "Fourth", "Fifth"],
        "hashtags": ["#Shorts", "#Viral", "#Facts", "#Amazing", "#DidYouKnow"]
    },
    "pt": {
        "intro_phrases": [
            "Você sabia que...",
            "Você vai se surpreender com...",
            "Você não vai acreditar...",
            "Isso vai te impressionar...",
            "Prepare-se para...",
        ],
        "transition_phrases": [
            "Mas isso não é tudo...",
            "E agora vem o melhor...",
            "Espere porque falta o mais louco...",
            "Mas há algo ainda mais impressionante...",
            "E o próximo vai te deixar sem palavras...",
        ],
        "outro_phrases": [
            "Deixe like se te surpreendeu!",
            "Conhecia esses dados? Comente!",
            "Se inscreva para mais conteúdo assim!",
            "Compartilhe se gostou!",
            "Qual te impressionou mais? Me diga nos comentários!",
        ],
        "numbers": ["Primeiro", "Segundo", "Terceiro", "Quarto", "Quinto"],
        "hashtags": ["#Shorts", "#Viral", "#Curiosidades", "#DadosIncriveis", "#Vocebia"]
    }
}

# ===== FUNCIONES DE CONFIGURACIÓN =====

def get_language_config(language: str = None) -> dict:
    """Obtiene la configuración para un idioma específico."""
    lang = language or DEFAULT_LANGUAGE
    return LANGUAGES_CONFIG.get(lang, LANGUAGES_CONFIG[DEFAULT_LANGUAGE])

def get_theme_config(theme: str = None, language: str = None) -> dict:
    """Obtiene la configuración de tema para un idioma específico."""
    theme = theme or DEFAULT_THEME
    lang = language or DEFAULT_LANGUAGE
    
    if theme in THEMES_CONFIG and lang in THEMES_CONFIG[theme]:
        return THEMES_CONFIG[theme][lang]
    else:
        # Fallback al primer idioma disponible del tema
        first_lang = list(THEMES_CONFIG[theme].keys())[0]
        return THEMES_CONFIG[theme][first_lang]

def get_localized_texts(language: str = None) -> dict:
    """Obtiene los textos localizados para un idioma."""
    lang = language or DEFAULT_LANGUAGE
    return LOCALIZED_TEXTS.get(lang, LOCALIZED_TEXTS[DEFAULT_LANGUAGE])

def get_voice_for_language(language: str = None, female: bool = False) -> str:
    """Obtiene la voz apropiada para un idioma."""
    config = get_language_config(language)
    return config["voice_female"] if female else config["voice"]

# ===== CONFIGURACIÓN ACTUAL ACTIVA =====

def get_current_config() -> dict:
    """Obtiene la configuración completa actual."""
    return {
        "language": DEFAULT_LANGUAGE,
        "theme": DEFAULT_THEME,
        "language_config": get_language_config(),
        "theme_config": get_theme_config(),
        "texts": get_localized_texts(),
        "voice": get_voice_for_language(),
        "voice_female": get_voice_for_language(female=True)
    }

if __name__ == "__main__":
    # Ejemplo de uso
    config = get_current_config()
    print(f"Configuración actual:")
    print(f"- Idioma: {config['language_config']['name']}")
    print(f"- Tema: {config['theme']}")
    print(f"- Canal: {config['theme_config']['channel_name']}")
    print(f"- Voz: {config['voice']}")
    print(f"- Hashtags: {config['texts']['hashtags']}")