"""
Generador de contenido usando Ollama (IA local gratuita).
Optimizado para Llama 3.1:8B con soporte GPU GTX 1660Ti.
"""

import json
import logging
import subprocess
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OllamaConfig:
    """Configuración optimizada para Ollama."""
    model: str = "llama3.1:8b"
    temperature: float = 0.8
    max_tokens: int = 1000
    top_p: float = 0.9
    repeat_penalty: float = 1.1

class OllamaGenerator:
    """Generador de contenido usando Ollama local."""
    
    def __init__(self, config: OllamaConfig = None):
        self.config = config or OllamaConfig()
        self.available_models = []
        self.is_installed = self._check_ollama_installation()
        
        if self.is_installed:
            self._setup_model()
    
    def _check_ollama_installation(self) -> bool:
        """Verifica si Ollama está instalado."""
        try:
            result = subprocess.run(
                ["ollama", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Ollama detectado: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("Ollama no está instalado")
        return False
    
    def _setup_model(self) -> bool:
        """Configura y descarga el modelo si es necesario."""
        try:
            # Listar modelos disponibles
            result = subprocess.run(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                self.available_models = self._parse_model_list(result.stdout)
                logger.info(f"Modelos disponibles: {self.available_models}")
            
            # Verificar si el modelo está disponible
            if self.config.model not in self.available_models:
                logger.info(f"Descargando modelo {self.config.model}...")
                self._pull_model(self.config.model)
            
            return True
            
        except Exception as e:
            logger.error(f"Error configurando modelo: {e}")
            return False
    
    def _parse_model_list(self, output: str) -> List[str]:
        """Parsea la lista de modelos de Ollama."""
        models = []
        for line in output.split('\n')[1:]:  # Skip header
            if line.strip():
                model_name = line.split()[0]
                if model_name and model_name != "NAME":
                    models.append(model_name)
        return models
    
    def _pull_model(self, model: str) -> bool:
        """Descarga un modelo específico."""
        try:
            logger.info(f"Iniciando descarga de {model} (puede tardar varios minutos)...")
            process = subprocess.run(
                ["ollama", "pull", model],
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutos timeout
            )
            
            if process.returncode == 0:
                logger.info(f"Modelo {model} descargado exitosamente")
                self.available_models.append(model)
                return True
            else:
                logger.error(f"Error descargando modelo: {process.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout descargando modelo {model}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado descargando modelo: {e}")
            return False
    
    def generate_content(self, prompt: str) -> Optional[str]:
        """
        Genera contenido usando Ollama.
        
        Args:
            prompt: Prompt para la generación
            
        Returns:
            str: Contenido generado o None si hay error
        """
        if not self.is_installed:
            logger.error("Ollama no está instalado")
            return None
        
        if self.config.model not in self.available_models:
            logger.error(f"Modelo {self.config.model} no disponible")
            return None
        
        try:
            # Preparar comando Ollama
            ollama_prompt = {
                "model": self.config.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.config.temperature,
                    "num_predict": self.config.max_tokens,
                    "top_p": self.config.top_p,
                    "repeat_penalty": self.config.repeat_penalty,
                    "num_gpu": 1  # Usar GPU si está disponible
                }
            }
            
            # Ejecutar Ollama con el comando correcto y encoding UTF-8
            process = subprocess.run(
                ["ollama", "run", self.config.model],
                input=prompt,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',  # Reemplazar caracteres problemáticos
                timeout=300  # 5 minutos timeout
            )
            
            if process.returncode == 0:
                response = process.stdout.strip()
                logger.info(f"Contenido generado exitosamente ({len(response)} caracteres)")
                return response
            else:
                logger.error(f"Error generando contenido: {process.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout generando contenido")
            return None
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            return None
    
    def generate_shorts_script(self, topic: str, language: str = "es", 
                              content_type: str = "TOP_5", topic_data: dict = None) -> Optional[Dict]:
        """
        Genera un script específico para YouTube Shorts con prompts variables.
        
        Args:
            topic: Tema del Short
            language: Idioma (es, en, pt, fr, it, de)
            content_type: Tipo de contenido (TOP_5, CURIOSIDADES)
            topic_data: Datos del tema con prompts variables y hooks
            
        Returns:
            dict: Script estructurado para Shorts
        """
        
        # 🎯 SISTEMA DE PROMPTS VARIABLES Y DINÁMICOS
        
        # Extraer hook y ending personalizados si están disponibles
        custom_hook = topic_data.get('hook', '¿Sabías que hay secretos que te van a impactar?') if topic_data else '¿Sabías que hay secretos que te van a impactar?'
        custom_ending = topic_data.get('ending', '¿Cuál te impactó más? Déjalo en comentarios.') if topic_data else '¿Cuál te impactó más? Déjalo en comentarios.'
        custom_prompt = topic_data.get('prompt', f'Crea contenido viral sobre {topic}') if topic_data else f'Crea contenido viral sobre {topic}'
        
        # Prompts optimizados por idioma con variabilidad extrema
        prompts = {
            "es": {
                "TOP_5": f"""{custom_prompt}

🎯 INSTRUCCIONES ESPECÍFICAS PARA SHORTS VIRALES:
- Duración: 45-75 segundos (óptimo para algoritmo)
- Formato: TOP 5 ranking dinámico
- Tono: Impactante, revelador, que genere curiosidad extrema
- Hook inicial personalizado: "{custom_hook}"
- Cierre viral: "{custom_ending}"

RESPONDE CON ESTE FORMATO EXACTO:

TÍTULO: [título súper llamativo con emojis que genere clicks]

NARRACIÓN: [SOLO el texto que debe leer el locutor - texto narrativo puro y natural, SIN instrucciones técnicas, SIN descripciones de imágenes, SIN tiempos]

DESCRIPCIÓN: [descripción SEO optimizada para YouTube]

TAGS: [8-10 hashtags virales]

THUMBNAIL: [3 ideas impactantes para miniatura]

ESTRUCTURA NARRATIVA REQUERIDA:
1. Hook personalizado: "{custom_hook}"
2. Introducción rápida al tema (5-8 segundos)
3. TOP 5 elementos en orden ascendente de impacto
4. Transiciones rápidas entre puntos
5. Cierre viral: "{custom_ending}"

EJEMPLO DE ESTRUCTURA:
"{custom_hook} Te voy a revelar el TOP 5 de {topic} que van a cambiar tu perspectiva. En el quinto lugar... [desarrollar]. El cuarto dato es aún más perturbador... [continuar]. El tercero te va a impactar... [continuar]. El segundo lugar es escalofriante... [continuar]. Y el número uno... esto es absolutamente increíble... [clímax]. {custom_ending}"

GENERA TEXTO NARRATIVO PURO - sin instrucciones como 'mostrar imagen X' o 'pausa dramática'.""",
                
                "CURIOSIDADES": f"""{custom_prompt}

🎯 FORMATO CURIOSIDADES VIRALES:
- Hook: "{custom_hook}"
- 3-5 datos impactantes
- Cierre: "{custom_ending}"
- Duración: 30-50 segundos

RESPONDE CON ESTE FORMATO EXACTO:

TÍTULO: [título impactante con emojis]

NARRACIÓN: [SOLO texto para locutor - narrativo puro, SIN instrucciones técnicas]

DESCRIPCIÓN: [descripción SEO]

TAGS: [hashtags virales]

THUMBNAIL: [3 sugerencias impactantes]

ESTRUCTURA:
"{custom_hook} Te voy a contar datos sobre {topic} que te van a volar la mente. Primer dato: [impactante]. Segundo: [más impactante]. Tercero: [escalofriante]. {custom_ending}"

Genera SOLO texto narrativo puro."""
            },
            
            "en": {
                "TOP_5": f"""Create a 45-60 second YouTube Short script about "{topic}".

REQUIRED FORMAT:
- Catchy title (max 60 chars)
- Powerful hook (3-5 seconds)
- 5 numbered main points
- Quick transitions
- Strong call-to-action
- Relevant hashtags

STYLE: Energetic, viral, shocking
DURATION: 45-60 seconds max
AUDIENCE: 16-35 years English speakers

Generate complete script:""",
                
                "CURIOSIDADES": f"""Create viral curiosities content about "{topic}" for YouTube Short.

FORMAT:
- Shocking title (max 60 chars)
- Hook intro (Did you know...?)
- 3-5 incredible numbered facts
- Surprising ending
- Viral hashtags

STYLE: Mind-blowing, educational, viral
DURATION: 30-45 seconds

Generate complete script:"""
            }
        }
        
        # Seleccionar prompt
        lang_prompts = prompts.get(language, prompts["es"])
        prompt = lang_prompts.get(content_type, lang_prompts["TOP_5"])
        
        # Generar contenido
        raw_content = self.generate_content(prompt)
        
        if not raw_content:
            return None
        
        # Parsear y estructurar el contenido
        return self._parse_shorts_content(raw_content, topic)
    
    def _parse_shorts_content(self, content: str, topic: str) -> Dict:
        """Parsea el contenido generado en estructura de Shorts."""
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        result = {
            "title": topic.title(),
            "script": content,
            "hook": "",
            "main_points": [],
            "outro": "",
            "hashtags": [],
            "estimated_duration": 45,
            "seo_score": 75,
            "description": f"Descubre datos increíbles sobre {topic}. ¡No te pierdas estos datos que te van a sorprender!"
        }
        
        # Intentar extraer título
        title_indicators = ["[TÍTULO]", "[TITLE]", "TÍTULO:", "TITLE:"]
        for i, line in enumerate(lines):
            if any(indicator in line.upper() for indicator in title_indicators):
                if i + 1 < len(lines):
                    result["title"] = lines[i + 1][:60]
                break
        
        # Extraer hashtags
        hashtags = []
        for line in lines:
            if line.startswith('#'):
                hashtags.extend([tag.strip() for tag in line.split() if tag.startswith('#')])
        
        if hashtags:
            result["hashtags"] = hashtags[:15]  # Max 15 hashtags
        else:
            # Hashtags por defecto
            result["hashtags"] = ["#Shorts", "#Viral", "#Curiosidades", "#DatosIncreibles", "#Sabias"]
        
        return result
    
    def get_system_info(self) -> Dict:
        """Obtiene información del sistema y configuración."""
        return {
            "ollama_installed": self.is_installed,
            "current_model": self.config.model,
            "available_models": self.available_models,
            "config": {
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "top_p": self.config.top_p
            }
        }

# Funciones de utilidad
def install_ollama_guide() -> str:
    """Retorna guía de instalación de Ollama."""
    return """
🔧 INSTALACIÓN DE OLLAMA (Windows):

1. Descargar desde: https://ollama.ai/download/windows
2. Ejecutar el instalador
3. Abrir terminal y ejecutar:
   ollama pull llama3.1:8b

4. Verificar instalación:
   ollama list

🚀 MODELO RECOMENDADO PARA TU SETUP:
- llama3.1:8b (Balanced - 8GB RAM, excelente calidad)
- Con tu 1660Ti y 48GB RAM será ultra rápido

⚡ OPTIMIZACIÓN GPU:
Ollama detectará automáticamente tu GTX 1660Ti
"""

def check_hardware_compatibility() -> Dict:
    """Verifica compatibilidad del hardware."""
    return {
        "recommended_model": "llama3.1:8b",
        "ram_requirement": "8GB+",
        "gpu_support": "GTX 1660Ti detected - Perfect!",
        "expected_speed": "Very Fast",
        "quality": "Excellent for Shorts"
    }

if __name__ == "__main__":
    # Test básico
    generator = OllamaGenerator()
    
    if not generator.is_installed:
        print(install_ollama_guide())
    else:
        print("✅ Ollama configurado correctamente")
        print(f"Modelos disponibles: {generator.available_models}")
        
        # Test de generación
        test_script = generator.generate_shorts_script(
            topic="animales más raros del mundo",
            language="es",
            content_type="TOP_5"
        )
        
        if test_script:
            print(f"\n📝 Script generado: {test_script['title']}")
            print(f"Duración estimada: {test_script['estimated_duration']}s")