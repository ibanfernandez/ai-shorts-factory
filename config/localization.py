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
# Opciones: "curiosidades", "tecnologia", "historia", "entretenimiento", "comida", "deportes", "viajes", "negocios", "musica", "ciencia"

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
    },
    "entretenimiento": {
        "es": {
            "channel_name": "Entre Viral",
            "description": "Lo mejor del entretenimiento, películas, series y celebridades",
            "tags_base": ["entretenimiento", "peliculas", "series", "celebridades", "viral"],
            "content_types": ["TOP_5", "CELEBS", "CINE_TV"],
            "topics_pool": [
                "actores más pagados de Hollywood",
                "películas más taquilleras de la historia",
                "series más adictivas del momento",
                "secretos de celebridades famosas",
                "escenas más épicas del cine"
            ]
        },
        "en": {
            "channel_name": "Entertainment Viral",
            "description": "The best of entertainment, movies, series and celebrities",
            "tags_base": ["entertainment", "movies", "series", "celebrities", "viral"],
            "content_types": ["TOP_5", "CELEBS", "MOVIES_TV"],
            "topics_pool": [
                "highest paid actors in Hollywood",
                "highest grossing movies in history",
                "most addictive series of the moment",
                "secrets of famous celebrities",
                "most epic scenes in cinema"
            ]
        }
    },
    "comida": {
        "es": {
            "channel_name": "Sabores Virales",
            "description": "Recetas increíbles y datos gastronómicos sorprendentes",
            "tags_base": ["comida", "recetas", "gastronomia", "cocina", "viral"],
            "content_types": ["TOP_5", "RECETAS", "GASTRONOMIA"],
            "topics_pool": [
                "comidas más caras del mundo",
                "platos más raros de diferentes países",
                "ingredientes más exóticos que existen",
                "restaurantes más exclusivos del planeta",
                "datos curiosos sobre la comida"
            ]
        },
        "en": {
            "channel_name": "Viral Flavors",
            "description": "Incredible recipes and surprising gastronomic facts",
            "tags_base": ["food", "recipes", "gastronomy", "cooking", "viral"],
            "content_types": ["TOP_5", "RECIPES", "GASTRONOMY"],
            "topics_pool": [
                "most expensive foods in the world",
                "weirdest dishes from different countries",
                "most exotic ingredients that exist",
                "most exclusive restaurants on the planet",
                "curious facts about food"
            ]
        }
    },
    "deportes": {
        "es": {
            "channel_name": "Deporte Viral",
            "description": "Estadísticas increíbles y curiosidades deportivas",
            "tags_base": ["deportes", "estadisticas", "futbol", "records", "viral"],
            "content_types": ["TOP_5", "ESTADISTICAS", "RECORDS"],
            "topics_pool": [
                "records deportivos más impresionantes",
                "jugadores más veloces del mundo",
                "estadios más grandes del planeta",
                "momentos más épicos del deporte",
                "datos locos del fútbol mundial"
            ]
        },
        "en": {
            "channel_name": "Sports Viral",
            "description": "Incredible statistics and sports curiosities",
            "tags_base": ["sports", "statistics", "soccer", "records", "viral"],
            "content_types": ["TOP_5", "STATS", "RECORDS"],
            "topics_pool": [
                "most impressive sports records",
                "fastest players in the world",
                "largest stadiums on the planet",
                "most epic moments in sports",
                "crazy facts about world soccer"
            ]
        }
    },
    "viajes": {
        "es": {
            "channel_name": "Viajes Virales",
            "description": "Destinos increíbles y culturas fascinantes del mundo",
            "tags_base": ["viajes", "destinos", "culturas", "turismo", "viral"],
            "content_types": ["TOP_5", "DESTINOS", "CULTURAS"],
            "topics_pool": [
                "destinos más baratos para viajar",
                "países más seguros del mundo",
                "culturas más fascinantes del planeta",
                "lugares más fotogénicos para Instagram",
                "ciudades más caras para vivir"
            ]
        },
        "en": {
            "channel_name": "Travel Viral",
            "description": "Incredible destinations and fascinating cultures of the world",
            "tags_base": ["travel", "destinations", "cultures", "tourism", "viral"],
            "content_types": ["TOP_5", "DESTINATIONS", "CULTURES"],
            "topics_pool": [
                "cheapest destinations to travel",
                "safest countries in the world",
                "most fascinating cultures on the planet",
                "most photogenic places for Instagram",
                "most expensive cities to live in"
            ]
        }
    },
    "negocios": {
        "es": {
            "channel_name": "Business Viral",
            "description": "Emprendimiento, finanzas y éxito empresarial",
            "tags_base": ["negocios", "emprendimiento", "finanzas", "exito", "viral"],
            "content_types": ["TOP_5", "EMPRESAS", "FINANZAS"],
            "topics_pool": [
                "empresarios más jóvenes del mundo",
                "negocios más rentables del momento",
                "inversiones más inteligentes que puedes hacer",
                "marcas más valiosas del planeta",
                "historias de éxito empresarial increíbles"
            ]
        },
        "en": {
            "channel_name": "Business Viral",
            "description": "Entrepreneurship, finance and business success",
            "tags_base": ["business", "entrepreneurship", "finance", "success", "viral"],
            "content_types": ["TOP_5", "COMPANIES", "FINANCE"],
            "topics_pool": [
                "youngest entrepreneurs in the world",
                "most profitable businesses right now",
                "smartest investments you can make",
                "most valuable brands on the planet",
                "incredible business success stories"
            ]
        }
    },
    "musica": {
        "es": {
            "channel_name": "Música Viral",
            "description": "Artistas, géneros y datos musicales fascinantes",
            "tags_base": ["musica", "artistas", "canciones", "generos", "viral"],
            "content_types": ["TOP_5", "ARTISTAS", "CANCIONES"],
            "topics_pool": [
                "artistas más escuchados del mundo",
                "canciones más virales de la historia",
                "géneros musicales más raros que existen",
                "instrumentos más difíciles de tocar",
                "datos curiosos de tus artistas favoritos"
            ]
        },
        "en": {
            "channel_name": "Music Viral",
            "description": "Artists, genres and fascinating musical facts",
            "tags_base": ["music", "artists", "songs", "genres", "viral"],
            "content_types": ["TOP_5", "ARTISTS", "SONGS"],
            "topics_pool": [
                "most listened artists in the world",
                "most viral songs in history",
                "weirdest music genres that exist",
                "most difficult instruments to play",
                "curious facts about your favorite artists"
            ]
        }
    },
    "ciencia": {
        "es": {
            "channel_name": "Ciencia Viral",
            "description": "Descubrimientos científicos y experimentos fascinantes",
            "tags_base": ["ciencia", "experimentos", "descubrimientos", "fisica", "viral"],
            "content_types": ["TOP_5", "EXPERIMENTOS", "DESCUBRIMIENTOS"],
            "topics_pool": [
                "experimentos científicos más peligrosos",
                "descubrimientos que cambiaron la humanidad",
                "teorías científicas más controversiales",
                "inventos del futuro que ya existen",
                "datos científicos que te van a sorprender"
            ]
        },
        "en": {
            "channel_name": "Science Viral",
            "description": "Scientific discoveries and fascinating experiments",
            "tags_base": ["science", "experiments", "discoveries", "physics", "viral"],
            "content_types": ["TOP_5", "EXPERIMENTS", "DISCOVERIES"],
            "topics_pool": [
                "most dangerous scientific experiments",
                "discoveries that changed humanity",
                "most controversial scientific theories",
                "future inventions that already exist",
                "scientific facts that will amaze you"
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

# ===== CARGA DE TEMAS PERSONALIZADOS =====

def load_custom_themes():
    """Carga temas personalizados desde templates/custom_themes.json."""
    import json
    import os
    from pathlib import Path
    
    try:
        project_root = Path(__file__).parent.parent
        custom_themes_file = project_root / "templates" / "custom_themes.json"
        
        if custom_themes_file.exists():
            with open(custom_themes_file, 'r', encoding='utf-8') as f:
                custom_data = json.load(f)
                
            # Agregar temas custom a THEMES_CONFIG
            custom_themes = custom_data.get("custom_themes", {})
            if custom_themes:
                THEMES_CONFIG.update(custom_themes)
                print(f"✅ Cargados {len(custom_themes)} temas personalizados")
            return True
    except Exception as e:
        print(f"⚠️ No se pudieron cargar temas personalizados: {e}")
    
    return False

# Cargar temas personalizados al importar el módulo
load_custom_themes()

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