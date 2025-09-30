"""
Generador de contenido usando IA para YouTube.
Soporte para OpenAI (pago) y Ollama (local gratuito).
"""

import openai
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from config.settings import settings, CONTENT_TEMPLATES

# Importar Ollama generator
try:
    from .ollama_generator import OllamaGenerator, OllamaConfig
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
try:
    from config.localization import (
        get_current_config, get_theme_config, 
        get_localized_texts, DEFAULT_LANGUAGE, DEFAULT_THEME
    )
except ImportError:
    # Fallback
    DEFAULT_LANGUAGE = "es"
    DEFAULT_THEME = "curiosidades"
    def get_current_config():
        return {"language": "es", "theme": "curiosidades"}
    def get_theme_config(theme=None, lang=None):
        return {"content_types": ["TOP_5"], "tags_base": ["viral"]}
    def get_localized_texts(lang=None):
        return {"hashtags": ["#Shorts", "#Viral"]}

logger = logging.getLogger(__name__)

@dataclass
class ContentRequest:
    """Solicitud de generación de contenido."""
    content_type: str  # Dinámico según configuración
    topic: str
    target_duration: int = 45  # 45 segundos para Shorts
    language: str = DEFAULT_LANGUAGE  # Configurable
    target_audience: str = "general"
    theme: str = DEFAULT_THEME  # Temática configurable

@dataclass
class GeneratedContent:
    """Contenido generado por IA."""
    title: str
    script: str
    description: str
    tags: List[str]
    thumbnail_suggestions: List[str]
    estimated_duration: int
    seo_score: float

class ContentGenerator:
    """Generador de contenido principal con soporte OpenAI y Ollama."""
    
    def __init__(self, language: str = None, theme: str = None, use_ollama: bool = None):
        """
        Inicializa el generador.
        
        Args:
            language: Idioma del contenido
            theme: Tema del contenido  
            use_ollama: Si usar Ollama (None = auto-detectar)
        """
        # Configuración localizada
        self.language = language or settings.LANGUAGE
        self.theme = theme or settings.THEME
        self.config = get_current_config()
        self.theme_config = get_theme_config(self.theme, self.language)
        self.texts = get_localized_texts(self.language)
        
        # Configurar proveedores de IA
        self.ollama_generator = None
        self.use_ollama = use_ollama
        
        # Auto-detectar mejor opción si no se especifica
        if use_ollama is None:
            self.use_ollama = self._auto_select_ai_provider()
        
        if self.use_ollama and OLLAMA_AVAILABLE:
            try:
                self.ollama_generator = OllamaGenerator()
                if self.ollama_generator.is_installed:
                    logger.info("✅ Usando Ollama (IA local gratuita)")
                else:
                    logger.warning("Ollama no disponible, usando OpenAI")
                    self.use_ollama = False
            except Exception as e:
                logger.warning(f"Error configurando Ollama: {e}")
                self.use_ollama = False
        
        # Configurar OpenAI como fallback
        if not self.use_ollama:
            if not settings.OPENAI_API_KEY:
                raise ValueError("Se necesita OPENAI_API_KEY o instalar Ollama para funcionar")
            openai.api_key = settings.OPENAI_API_KEY
            logger.info("💳 Usando OpenAI (servicio de pago)")
        
        logger.info(f"ContentGenerator inicializado - Proveedor: {'Ollama' if self.use_ollama else 'OpenAI'}")
    
    def _auto_select_ai_provider(self) -> bool:
        """Auto-selecciona el mejor proveedor de IA disponible."""
        # Prioridad: Ollama (gratis) > OpenAI (pago)
        if OLLAMA_AVAILABLE:
            try:
                test_generator = OllamaGenerator()
                if test_generator.is_installed:
                    logger.info("🎯 Auto-seleccionado: Ollama (gratuito)")
                    return True
            except:
                pass
        
        if settings.OPENAI_API_KEY:
            logger.info("🎯 Auto-seleccionado: OpenAI (de pago)")
            return False
        
        raise ValueError("No hay proveedores de IA disponibles. Instala Ollama o configura OPENAI_API_KEY")
    
    def _build_localized_prompt(self, request: ContentRequest) -> dict:
        """Construye prompts localizados basados en configuración."""
        # Usar configuración localizada
        content_types = self.theme_config.get("content_types", ["TOP_5"])
        if request.content_type not in content_types:
            request.content_type = content_types[0]  # Usar el primero disponible
            
        hashtags = " ".join(self.texts.get("hashtags", ["#Shorts", "#Viral"]))
        
        system_prompt = f"""Eres un experto creador de contenido para YouTube Shorts en {self.config['language_config']['name']}. 
        Especialízate en {self.theme_config.get('description', 'contenido viral')} para el canal '{self.theme_config.get('channel_name', 'Canal Viral')}'.
        Crea contenido viral, interesante y bien estructurado."""
        
        user_prompt = f"""Crea un guión para un YouTube SHORT sobre "{request.content_type.replace('_', ' ')} {request.topic}" (máximo {request.target_duration} segundos).

        REQUISITOS:
        1. Título llamativo ({hashtags})
        2. Gancho inicial potente (primeros 3 segundos)
        3. Formato {request.content_type.replace('_', ' ')} dinámico 
        4. Transiciones rápidas y enganchantes
        5. Call-to-action final
        6. Idioma: {self.config['language_config']['name']}
        
        Usa frases como: {', '.join(self.texts.get('intro_phrases', ['¿Sabías que...'])[:2])}
        
        FORMATO:
        TÍTULO: [título viral con emojis]
        NARRACIÓN: [SOLO el texto que el locutor debe leer, SIN instrucciones técnicas, SIN descripciones de imágenes, SIN tiempos - solo texto narrativo puro para TTS]
        DESCRIPCIÓN: [descripción SEO]
        TAGS: [5-8 tags]
        THUMBNAIL: [3 sugerencias]"""
        
        return {"system": system_prompt, "user": user_prompt}

    def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """
        Genera contenido completo para YouTube.
        
        Args:
            request: Solicitud de contenido
            
        Returns:
            GeneratedContent: Contenido completo generado
        """
        logger.info(f"Generando contenido: {request.content_type} - {request.topic}")
        
        try:
            # Validar y ajustar tema si es necesario
            validated_request = self._validate_and_fix_topic(request)
            
            # Obtener template apropiado
            template = CONTENT_TEMPLATES.get(validated_request.content_type)
            if not template:
                raise ValueError(f"Tipo de contenido no soportado: {validated_request.content_type}")
            
            # Generar guión principal
            raw_content = self._generate_script(validated_request, template)
            
            # Extraer elementos específicos del contenido generado
            title = self._extract_title(raw_content)
            script = self._extract_narration(raw_content)  # SOLO narración para TTS
            description = self._generate_description(script, validated_request.topic)
            tags = self._generate_tags(validated_request.topic, validated_request.content_type)
            thumbnail_suggestions = self._generate_thumbnail_ideas(validated_request.topic)
            
            # Calcular duración estimada basada en narración pura
            estimated_duration = self._estimate_duration(script)
            
            # Calcular score SEO básico
            seo_score = self._calculate_seo_score(title, description, tags)
            
            content = GeneratedContent(
                title=title,
                script=script,  # Ahora contiene SOLO la narración
                description=description,
                tags=tags,
                thumbnail_suggestions=thumbnail_suggestions,
                estimated_duration=estimated_duration,
                seo_score=seo_score
            )
            
            logger.info(f"Contenido generado exitosamente. Duración: {estimated_duration}s")
            return content
            
        except Exception as e:
            logger.error(f"Error generando contenido: {e}")
            raise
    
    def _validate_and_fix_topic(self, request: ContentRequest) -> ContentRequest:
        """
        Valida el tema y lo reemplaza con alternativas seguras si es problemático.
        
        Args:
            request: Solicitud original
            
        Returns:
            ContentRequest: Solicitud con tema validado/corregido
        """
        original_topic = request.topic.lower()
        
        # Lista de palabras problemáticas que causan rechazo
        problematic_keywords = [
            'alimentos', 'suplementos', 'medicamentos', 'fármacos', 'pastillas',
            'adelgazar', 'dieta', 'peso', 'grasa', 'músculo', 'proteína',
            'vitaminas', 'energía inmediatamente', 'salud', 'curar', 'sanar',
            'medicina', 'tratamiento', 'terapia', 'remedio', 'dosis'
        ]
        
        # Verificar si el tema contiene palabras problemáticas
        is_problematic = any(keyword in original_topic for keyword in problematic_keywords)
        
        if is_problematic:
            logger.warning(f"⚠️ Tema problemático detectado: '{request.topic}' - Generando alternativa segura...")
            
            # Temas alternativos seguros y virales por categoría
            safe_alternatives = {
                "TOP_5": [
                    "lugares más misteriosos del mundo",
                    "datos curiosos sobre el espacio",
                    "animales más raros del planeta", 
                    "lugares abandonados más escalofriantes",
                    "misterios sin resolver de la historia",
                    "fenómenos naturales más extraños",
                    "civilizaciones perdidas más fascinantes",
                    "tecnologías del futuro más increíbles",
                    "record mundiales más sorprendentes",
                    "curiosidades sobre los océanos"
                ],
                "CURIOSIDADES": [
                    "datos sorprendentes sobre el universo",
                    "misterios de las pirámides",
                    "secretos de la naturaleza",
                    "curiosidades sobre los dinosaurios", 
                    "fenómenos inexplicables",
                    "datos curiosos sobre los gatos",
                    "misterios del cerebro humano",
                    "curiosidades sobre la música",
                    "secretos de la física cuántica",
                    "datos raros sobre el tiempo"
                ]
            }
            
            # Seleccionar tema alternativo basado en el tipo de contenido
            alternatives = safe_alternatives.get(request.content_type, safe_alternatives["TOP_5"])
            
            # Usar hash del tema original para selección consistente
            import hashlib
            topic_hash = int(hashlib.md5(original_topic.encode()).hexdigest()[:8], 16)
            selected_topic = alternatives[topic_hash % len(alternatives)]
            
            logger.info(f"✅ Tema alternativo seleccionado: '{selected_topic}'")
            
            # Crear nueva solicitud con tema seguro
            return ContentRequest(
                content_type=request.content_type,
                topic=selected_topic,
                target_duration=request.target_duration,
                language=request.language,
                target_audience=request.target_audience,
                theme=request.theme
            )
        
        # Si el tema es seguro, retornar sin cambios
        return request
    
    def _generate_script(self, request: ContentRequest, template: Dict) -> str:
        """Genera el guión principal usando Ollama u OpenAI."""
        
        if self.use_ollama and self.ollama_generator:
            # Usar Ollama (gratuito)
            logger.info("🆓 Generando con Ollama (IA local)")
            
            ollama_result = self.ollama_generator.generate_shorts_script(
                topic=request.topic,
                language=self.language,
                content_type=request.content_type,
                topic_data=getattr(request, 'topic_data', None)
            )
            
            if ollama_result:
                return ollama_result["script"]
            else:
                logger.warning("Ollama falló, usando OpenAI como fallback")
                self.use_ollama = False
        
        # Usar OpenAI (de pago) 
        logger.info("💳 Generando con OpenAI")
        
        prompt = template["user_prompt"].format(
            topic=request.topic,
            duration=request.target_duration // 60  # Convertir a minutos
        )
        
        try:
            # OpenAI v1.x syntax
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": template["system_prompt"]},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=0.8,
                top_p=0.9
            )
            
            content = response.choices[0].message.content.strip()
            
            # Detectar si la IA rechazó la solicitud
            if self._is_ai_rejection(content):
                logger.warning(f"🚫 IA rechazó el contenido: '{request.topic}' - Generando contenido genérico")
                logger.info(f"📝 Contenido rechazado original: '{content[:100]}...'")
                
                # CRÍTICO: Generar y retornar contenido alternativo válido
                fallback_content = self._generate_fallback_content(request)
                logger.info(f"✅ Contenido alternativo generado exitosamente: '{fallback_content[:100]}...'")
                return fallback_content
            
            logger.info(f"✅ Contenido de IA aceptado: '{content[:100]}...'")
            return content
            
        except Exception as e:
            logger.error(f"Error en IA: {e}")
            raise
    
    def _is_ai_rejection(self, content: str) -> bool:
        """
        Detecta si la IA rechazó generar el contenido solicitado con patrones mejorados.
        
        Args:
            content: Respuesta de la IA
            
        Returns:
            bool: True si es un rechazo
        """
        if not content or not isinstance(content, str):
            return True
            
        content_lower = content.lower().strip()
        
        # Lista expandida de frases de rechazo (incluye el caso reportado por el usuario)
        rejection_phrases = [
            # Spanish rejections - Basic
            "no puedo generar contenido",
            "no puedo crear contenido", 
            "lo siento, pero no",
            "lo siento pero no",
            "lo siento, no puedo",
            "lo siento pero no puedo",  # Patrón específico reportado
            "lo siento pero no puedo generar",
            "lo siento pero no puedo generar contenido",
            "lo siento pero no puedo generar contenido sobre",
            
            # Specific content types that get rejected
            "contenido sobre fakis",     # Caso específico reportado por usuario
            "contenido sobre deepfakes",
            "contenido sobre suplementos",
            "promoción de alimentos",
            "promoción de suplementos",
            "contenido relacionado con la promoción",
            "contenido que promueva",
            
            # Other Spanish rejection patterns
            "no es apropiado",
            "no puedo proporcionar",
            "no puedo ayudar",
            "no está permitido",
            "no es recomendable",
            "evitar la promoción",
            "no puedo generar",
            "no puedo crear",
            "no puedo escribir",
            "¿en qué puedo ayudarte?",
            "en qué puedo ayudarte",
            "como modelo de lenguaje",
            "como ia no puedo",
            "mi programación no me permite",
            
            # English rejections
            "sorry, i can't",
            "i cannot generate",
            "i'm not able to",
            "i can't create",
            "i cannot create",
            "i'm sorry, but",
            "i apologize, but",
            "i can't generate content",
            "i cannot generate content about",
            "as an ai, i cannot",
            "as a language model",
            "against my programming"
        ]
        
        # Check for rejection phrases
        for phrase in rejection_phrases:
            if phrase in content_lower:
                logger.warning(f"🚫 Contenido rechazado detectado - Frase: '{phrase}' en: '{content_lower[:200]}...'")
                return True
        
        # Enhanced pattern detection with regex for more complex patterns
        import re
        
        rejection_patterns = [
            # Spanish patterns
            r"lo siento.*no puedo.*generar",
            r"no puedo.*generar.*contenido.*sobre",
            r"contenido.*sobre.*(?:fakis|deepfakes|suplementos)",
            r"como (?:modelo|ia).*no puedo",
            
            # English patterns
            r"sorry.*can(?:'t|not).*generate",
            r"i can(?:'t|not).*generate.*content.*about",
            r"as (?:an ai|a language model).*cannot"
        ]
        
        for pattern in rejection_patterns:
            if re.search(pattern, content_lower):
                logger.warning(f"🚫 Contenido rechazado - Patrón regex: '{pattern}' en: '{content_lower[:200]}...'")
                return True
        
        # Check if content starts with common rejection starters
        rejection_starters = [
            "lo siento",
            "i'm sorry", 
            "i apologize",
            "disculpa",
            "perdón",
            "no puedo",
            "i can't",
            "i cannot",
            "lamentablemente",
            "unfortunately"
        ]
        
        for starter in rejection_starters:
            if content_lower.startswith(starter):
                logger.warning(f"🚫 Contenido rechazado - Inicia con: '{starter}' - '{content_lower[:200]}...'")
                return True
        
        # Additional checks
        help_patterns = [
            "¿en qué puedo ayudarte?",
            "en qué puedo ayudarte",
            "what can i help you with?",
            "how can i help you?"
        ]
        
        for pattern in help_patterns:
            if pattern in content_lower:
                logger.warning(f"🚫 Contenido rechazado - Pregunta de ayuda detectada: '{pattern}'")
                return True
            
        # Check for very short responses (likely rejections)
        if len(content.strip()) < 100:
            logger.warning(f"🚫 Contenido rechazado - Muy corto: {len(content)} chars - '{content_lower[:100]}'")
            return True
        
        # Check for high ratio of apology/refusal words
        word_count = len(content.split())
        if word_count > 0:
            rejection_words = ["sorry", "siento", "disculpa", "apologize", "lamento", 
                             "puedo", "can't", "cannot", "no", "not"]
            rejection_word_count = sum(1 for word in content_lower.split() 
                                     if any(rw in word for rw in rejection_words))
            rejection_ratio = rejection_word_count / word_count
            
            if rejection_ratio > 0.4:  # More than 40% rejection-related words
                logger.warning(f"🚫 Contenido rechazado - Alto ratio de palabras de rechazo: {rejection_ratio:.2f}")
                return True
            
        return False
    
    def _generate_fallback_content(self, request: ContentRequest) -> str:
        """
        Genera contenido genérico cuando la IA rechaza la solicitud.
        
        Args:
            request: Solicitud original
            
        Returns:
            str: Contenido genérico pero válido
        """
        logger.info("🔄 Generando contenido alternativo genérico...")
        
        import random
        
        # Multiple templates for variety
        fallback_options = [
            {
                "title": "🚀 TOP 5 Datos del Espacio Que Te Dejarán Sin Palabras",
                "narration": """¿Pensabas que conocías el universo? ¡Prepárate para alucinar!
                
                Primero: Júpiter es tan masivo que no orbita alrededor del Sol, sino que ambos orbitan un punto común en el espacio.
                
                Segundo: En el espacio, los metales se sueldan automáticamente si se tocan. Se llama soldadura en frío.
                
                Tercero: Un día en Venus dura más que su año. ¡Su rotación es más lenta que su órbita!
                
                Cuarto: Hay una nube de alcohol en el espacio de 1000 veces el tamaño de nuestro sistema solar.
                
                Y quinto: Los astronautas crecen hasta 5 centímetros en el espacio porque la gravedad no comprime su columna.
                
                ¿Cuál te voló la mente? ¡Sígueme para más secretos del cosmos!"""
            },
            {
                "title": "🧠 TOP 5 Hechos Sobre el Cerebro Humano Que Te Impactarán",
                "narration": """Tu cerebro es más increíble de lo que imaginas. ¡Estos datos te lo demostrarán!
                
                Primero: Tu cerebro usa solo el 20% de la energía de tu cuerpo, pero consume el 20% de todo el oxígeno.
                
                Segundo: Tienes más conexiones neuronales que estrellas en la Vía Láctea. ¡86 mil millones de neuronas!
                
                Tercero: El cerebro no tiene receptores de dolor. Por eso las cirugías cerebrales pueden hacerse despierto.
                
                Cuarto: Puedes recordar hasta 2.5 petabytes de información. Eso son 3 millones de horas de video.
                
                Y quinto: Tu cerebro genera 20 watts de energía. ¡Suficiente para encender una bombilla LED!
                
                ¿Sabías estos datos? ¡Dale like si te sorprendieron y sígueme para más!"""
            },
            {
                "title": "🌊 TOP 5 Misterios del Océano Que Desafían la Ciencia",
                "narration": """El océano guarda secretos más extraños que cualquier película de ciencia ficción.
                
                Primero: Solo hemos explorado el 5% de los océanos. Conocemos mejor la superficie de Marte.
                
                Segundo: Hay ríos y lagos DENTRO del océano. Se forman por diferencias de salinidad y temperatura.
                
                Tercero: El océano produce más del 70% del oxígeno que respiramos, no los árboles como muchos creen.
                
                Cuarto: Existe una zona llamada 'Punto Nemo' donde lo más cercano son astronautas en el espacio.
                
                Y quinto: Hay criaturas que brillan en la oscuridad y otras que pueden vivir sin oxígeno.
                
                ¿Te atreverías a explorar estas profundidades? ¡Sígueme para más misterios marinos!"""
            },
            {
                "title": "⚡ TOP 5 Inventos Que Cambiaron el Mundo por Accidente",
                "narration": """Estos inventos revolucionarios nacieron de errores geniales que transformaron la humanidad.
                
                Primero: La penicilina se descubrió porque Alexander Fleming dejó una placa de cultivo sucia por error.
                
                Segundo: El microondas se inventó cuando un ingeniero notó que su chocolate se derritió cerca de un radar.
                
                Tercero: Los Post-it nacieron de un pegamento 'fallido' que no pegaba lo suficientemente fuerte.
                
                Cuarto: El marcapasos se creó por error mientras intentaban grabar sonidos del corazón.
                
                Y quinto: El Velcro se inspiró en las semillas que se pegaban al perro de su inventor durante un paseo.
                
                ¿Increíble verdad? ¡Los mejores descubrimientos a veces son accidentales! ¡Sígueme para más!"""
            }
        ]
        
        # Select random template for variety
        selected_template = random.choice(fallback_options)
        
        fallback_templates = {
            "TOP_5": selected_template,
            "CURIOSIDADES": selected_template
        }
        
        # Seleccionar template apropiado
        template = fallback_templates.get(request.content_type, fallback_templates["TOP_5"])
        
        # Formatear contenido con estructura completa
        fallback_content = f"""TÍTULO: {template['title']}

NARRACIÓN: {template['narration']}

DESCRIPCIÓN: Descubre datos increíbles que te sorprenderán. ¡Contenido educativo y entretenido para toda la familia! #Shorts #Curiosidades #DatosCuriosos

TAGS: curiosidades, datos curiosos, educativo, entretenido, viral, shorts, increíble, sorprendente

THUMBNAIL: Texto grande con números, expresión de sorpresa, colores llamativos"""
        
        return fallback_content
    
    def _extract_title(self, script: str) -> str:
        """Extrae el título del guión generado con mejor detección de rechazos."""
        if not script or not isinstance(script, str):
            return "TOP 5 - Contenido Increíble"
            
        # PROTECCIÓN: Si el script contiene frases de rechazo, usar título por defecto
        script_lower = script.lower()
        rejection_indicators = [
            "lo siento", "no puedo", "i'm sorry", "i can't", 
            "contenido sobre", "generar contenido", "crear contenido"
        ]
        
        if any(indicator in script_lower for indicator in rejection_indicators):
            logger.warning(f"🚫 Título extraído de contenido con rechazo detectado - Usando título por defecto")
            return "🚀 TOP 5 Datos Increíbles Que Te Sorprenderán"
        
        lines = script.split('\n')
        for line in lines:
            if 'título' in line.lower() or 'title' in line.lower():
                # Buscar después de dos puntos
                if ':' in line:
                    title = line.split(':', 1)[1].strip().strip('"\'')
                    # Verificar que el título extraído no sea un rechazo
                    if not any(indicator in title.lower() for indicator in rejection_indicators):
                        return title
        
        # Fallback: primera línea no vacía que no sea un rechazo
        for line in lines:
            if (line.strip() and 
                not line.startswith('#') and 
                not any(indicator in line.lower() for indicator in rejection_indicators)):
                return line.strip()[:100]  # Máximo 100 chars
        
        # Último recurso: título por defecto
        return "🚀 TOP 5 Datos Increíbles Que Te Sorprenderán"
    
    def _extract_narration(self, script: str) -> str:
        """Extrae SOLO la narración pura del contenido generado con protección contra rechazos."""
        if not script or not isinstance(script, str):
            return "Descubre datos increíbles que te sorprenderán. ¡Contenido educativo y entretenido!"
            
        # PROTECCIÓN: Si el script contiene frases de rechazo, usar narración por defecto
        script_lower = script.lower()
        rejection_indicators = [
            "lo siento", "no puedo", "i'm sorry", "i can't", 
            "contenido sobre", "generar contenido", "crear contenido"
        ]
        
        if any(indicator in script_lower for indicator in rejection_indicators):
            logger.warning(f"🚫 Narración extraída de contenido con rechazo detectado - Usando narración por defecto")
            return """¿Sabías que existen datos increíbles que la mayoría de personas no conoce? 
            Hoy te traigo curiosidades que cambiarán tu perspectiva del mundo.
            
            Primero, los pulpos tienen tres corazones y sangre azul. ¡Increíble!
            
            Segundo, un día en Venus dura más que un año venusiano. La rotación es más lenta que la órbita.
            
            Tercero, las bananas son técnicamente bayas, pero las fresas no. La ciencia puede ser confusa.
            
            ¿Cuál te sorprendió más? ¡Déjamelo en los comentarios y sígueme para más curiosidades increíbles!"""
        
        # Buscar la sección de NARRACIÓN con diferentes formatos
        import re
        
        # Patrón para encontrar la sección NARRACIÓN
        narration_pattern = r'\*{0,2}NARRACIÓN\*{0,2}:?\s*(["\"]?)([^"]*?)\1(?=\*{0,2}DESCRIPCIÓN|\*{0,2}TAGS|\*{0,2}THUMBNAIL|$)'
        
        match = re.search(narration_pattern, script, re.IGNORECASE | re.DOTALL)
        if match:
            narration = match.group(2).strip()
            # Limpiar asteriscos y caracteres extra
            narration = re.sub(r'\*{2,}', '', narration)
            narration = narration.strip()
            
            # Verificar que la narración extraída no sea un rechazo
            if not any(indicator in narration.lower() for indicator in rejection_indicators):
                return narration
            else:
                logger.warning(f"🚫 Narración extraída contiene rechazo - Usando narración por defecto")
                return """¿Sabías que existen datos increíbles que cambiarán tu día? 
                Descubre curiosidades fascinantes sobre nuestro mundo.
                ¡Sígueme para más contenido increíble que te dejará sin palabras!"""
        
        # Fallback: si no encuentra NARRACIÓN, buscar patrones comunes
        lines = script.split('\n')
        narration_lines = []
        capturing = False
        
        for line in lines:
            line = line.strip()
            
            # Empezar a capturar después de NARRACIÓN, GUIÓN, etc.
            if any(keyword in line.lower() for keyword in ['narración:', 'guión:', '**narración**']):
                capturing = True
                # Si hay contenido después de los dos puntos, incluirlo
                if ':' in line:
                    content_after = line.split(':', 1)[1].strip()
                    if content_after and not content_after.startswith('*'):
                        narration_lines.append(content_after)
                continue
            
            # Parar de capturar en la siguiente sección
            if capturing and line and any(line.lower().startswith(keyword) for keyword in ['**descripción', '**tags', '**thumbnail', 'descripción:', 'tags:', 'thumbnail:']):
                break
            
            # Capturar líneas de narración (evitar líneas con solo asteriscos)
            if capturing and line and not line.startswith('**') and line != '':
                narration_lines.append(line)
        
        if narration_lines:
            result = ' '.join(narration_lines)
            # Limpiar comillas al principio y final
            result = result.strip('"').strip("'").strip()
            return result
        
        # Si no encontró nada, usar todo el script como fallback
        return script
    
    def _generate_description(self, script: str, topic: str) -> str:
        """Genera descripción optimizada para YouTube."""
        
        description_prompt = f"""
        Basándote en este guión de YouTube sobre "{topic}", crea una descripción optimizada:

        GUIÓN:
        {script[:500]}...

        REQUISITOS para la descripción:
        1. Máximo 200 palabras
        2. Incluir palabras clave SEO
        3. Call-to-action para suscribirse
        4. Mencionar contenido relacionado
        5. Incluir hashtags relevantes
        6. Tono amigable y profesional

        DESCRIPCIÓN:
        """
        
        # Usar Ollama si está disponible, sino fallback simple
        if self.use_ollama and self.ollama_generator:
            try:
                response = self.ollama_generator.generate_content(description_prompt)
                if response and len(response) > 50:
                    return response.strip()
            except Exception as e:
                logger.warning(f"Ollama falló para descripción: {e}")
        
        # Fallback simple sin OpenAI
        return f"Descubre datos increíbles sobre {topic}. ¡Sigue para más contenido viral! #Shorts #Curiosidades #Top5"
    
    def _generate_tags(self, topic: str, content_type: str) -> List[str]:
        """Genera tags relevantes para YouTube."""
        
        base_tags = [
            "top 10",
            "curiosidades", 
            "datos curiosos",
            "español",
            "interesante",
            "viral",
            "educativo"
        ]
        
        # Tags específicos por tema
        topic_words = topic.lower().split()
        for word in topic_words:
            if len(word) > 3:  # Solo palabras significativas
                base_tags.append(word)
        
        # Tags por tipo de contenido
        if content_type == "TOP_5":
            base_tags.extend(["ranking", "mejores", "lista"])
        elif content_type == "CURIOSIDADES":
            base_tags.extend(["increíble", "sorprendente", "sabías que"])
        
        return list(set(base_tags))[:15]  # Máximo 15 tags únicos
    
    def _generate_thumbnail_ideas(self, topic: str) -> List[str]:
        """Genera ideas para thumbnails."""
        
        return [
            f"Texto grande: 'TOP 10 {topic.upper()}'",
            "Expresión facial sorprendida",
            "Números grandes y coloridos (10, 1)",
            "Flechas y elementos llamativos",
            f"Imágenes representativas de {topic}",
            "Colores contrastantes (rojo, amarillo)"
        ]
    
    def _estimate_duration(self, script: str) -> int:
        """Estima duración en segundos basada en palabras."""
        # Promedio: 150 palabras por minuto en español
        words = len(script.split())
        return int((words / 150) * 60)
    
    def _calculate_seo_score(self, title: str, description: str, tags: List[str]) -> float:
        """Calcula un score básico de SEO (0-100)."""
        score = 0.0
        
        # Título optimizado (30 puntos)
        if len(title) >= 30 and len(title) <= 70:
            score += 15
        if any(keyword in title.lower() for keyword in ["top", "mejor", "increíble"]):
            score += 15
        
        # Descripción optimizada (30 puntos)
        if len(description) >= 100:
            score += 15
        if "suscríbete" in description.lower():
            score += 15
        
        # Tags relevantes (40 puntos)
        if len(tags) >= 5:
            score += 20
        if len(tags) <= 15:
            score += 20
        
        return min(score, 100.0)

def quick_generate(topic: str, content_type: str = "TOP_5") -> GeneratedContent:
    """
    Función de utilidad para generar contenido rápidamente.
    
    Args:
        topic: Tema del contenido
        content_type: Tipo de contenido ("TOP_5" o "CURIOSIDADES")
    
    Returns:
        GeneratedContent: Contenido generado
    """
    generator = ContentGenerator()
    request = ContentRequest(
        content_type=content_type,
        topic=topic
    )
    return generator.generate_content(request)

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging para testing
    logging.basicConfig(level=logging.INFO)
    
    # Ejemplo de generación
    try:
        content = quick_generate("animales más peligrosos del mundo", "TOP_5")
        print(f"Título: {content.title}")
        print(f"Duración estimada: {content.estimated_duration}s")
        print(f"SEO Score: {content.seo_score}")
        print(f"Tags: {', '.join(content.tags[:5])}...")
    except Exception as e:
        print(f"Error: {e}")
        print("Recuerda configurar OPENAI_API_KEY en tu archivo .env")