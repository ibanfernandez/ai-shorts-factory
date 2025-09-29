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
        GUIÓN: [guión completo de {request.target_duration}s]
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
            # Obtener template apropiado
            template = CONTENT_TEMPLATES.get(request.content_type)
            if not template:
                raise ValueError(f"Tipo de contenido no soportado: {request.content_type}")
            
            # Generar guión principal
            script = self._generate_script(request, template)
            
            # Generar elementos adicionales
            title = self._extract_title(script)
            description = self._generate_description(script, request.topic)
            tags = self._generate_tags(request.topic, request.content_type)
            thumbnail_suggestions = self._generate_thumbnail_ideas(request.topic)
            
            # Calcular duración estimada
            estimated_duration = self._estimate_duration(script)
            
            # Calcular score SEO básico
            seo_score = self._calculate_seo_score(title, description, tags)
            
            content = GeneratedContent(
                title=title,
                script=script,
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
    
    def _generate_script(self, request: ContentRequest, template: Dict) -> str:
        """Genera el guión principal usando Ollama u OpenAI."""
        
        if self.use_ollama and self.ollama_generator:
            # Usar Ollama (gratuito)
            logger.info("🆓 Generando con Ollama (IA local)")
            
            ollama_result = self.ollama_generator.generate_shorts_script(
                topic=request.topic,
                language=self.language,
                content_type=request.content_type
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
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": template["system_prompt"]},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=0.8,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error en IA: {e}")
            raise
    
    def _extract_title(self, script: str) -> str:
        """Extrae el título del guión generado."""
        lines = script.split('\n')
        for line in lines:
            if 'título' in line.lower() or 'title' in line.lower():
                # Buscar después de dos puntos
                if ':' in line:
                    return line.split(':', 1)[1].strip().strip('"\'')
        
        # Fallback: primera línea no vacía
        for line in lines:
            if line.strip() and not line.startswith('#'):
                return line.strip()[:100]  # Máximo 100 chars
        
        return "TOP 10 - Contenido Increíble"
    
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
        
        try:
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "user", "content": description_prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generando descripción: {e}")
            return f"Descubre las mejores curiosidades sobre {topic}. ¡Suscríbete para más contenido increíble!"
    
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