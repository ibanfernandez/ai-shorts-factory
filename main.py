"""
Script principal para ejecutar el flujo completo de automatización.
Orquesta todos los módulos: generación de contenido, creación de video y publicación.
"""

import asyncio
import logging
import logging.config
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

# Añadir src al path para imports
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from content_generator.ai_generator import ContentGenerator, ContentRequest
    from video_creator.video_generator import VideoCreator, VideoConfig
    from youtube_publisher.uploader import YouTubePublisher, VideoMetadata
    from config.settings import settings, LOGGING_CONFIG
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de instalar las dependencias: pip install -r requirements.txt")
    sys.exit(1)

# Configurar logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

class YouTubeAutomation:
    """Clase principal para automatización completa de YouTube."""
    
    def __init__(self, language: str = None, theme: str = None):
        """Inicializa todos los componentes necesarios."""
        try:
            from config.localization import get_current_config
            self.config = get_current_config()
            self.language = language or self.config.get('language', 'es')
            self.theme = theme or self.config.get('theme', 'curiosidades')
        except ImportError:
            self.language = language or 'es'
            self.theme = theme or 'curiosidades'
        
        self.content_generator = ContentGenerator(self.language, self.theme)
        self.video_creator = VideoCreator()
        self.youtube_publisher = YouTubePublisher()
        
        logger.info(f"YouTubeAutomation inicializado - Idioma: {self.language}, Tema: {self.theme}")
    
    async def create_and_publish_video(self, topic: str, content_type: str = "TOP_5", 
                                     privacy: str = "private", 
                                     publish_immediately: bool = False) -> dict:
        """
        Flujo completo: genera contenido, crea video y publica.
        
        Args:
            topic: Tema del video
            content_type: Tipo de contenido ("TOP_5" o "CURIOSIDADES")
            privacy: Estado de privacidad ("private", "public", "unlisted")
            publish_immediately: Si publicar inmediatamente
            
        Returns:
            dict: Resultado del proceso completo
        """
        
        start_time = datetime.now()
        result = {
            "success": False,
            "topic": topic,
            "content_type": content_type,
            "steps_completed": [],
            "errors": [],
            "start_time": start_time.isoformat()
        }
        
        try:
            # PASO 1: Generar contenido con IA
            logger.info(f"Iniciando generación de contenido: {topic}")
            
            request = ContentRequest(
                content_type=content_type,
                topic=topic,
                target_duration=45  # 45 segundos para Shorts
            )
            
            generated_content = self.content_generator.generate_content(request)
            result["steps_completed"].append("content_generation")
            result["generated_content"] = {
                "title": generated_content.title,
                "duration": generated_content.estimated_duration,
                "seo_score": generated_content.seo_score,
                "tags_count": len(generated_content.tags)
            }
            
            logger.info(f"Contenido generado: '{generated_content.title}'")
            
            # PASO 2: Crear video
            logger.info("Iniciando creación de video")
            
            video_config = VideoConfig(
                title=generated_content.title,
                script=generated_content.script,
                duration=min(generated_content.estimated_duration, 60),  # Máx 60s para Shorts
                resolution=(1080, 1920),  # Formato vertical
                is_short=True,
                show_captions=True
            )
            
            video_path = await self.video_creator.create_video(video_config)
            result["steps_completed"].append("video_creation")
            result["video_path"] = video_path
            
            logger.info(f"Video creado: {video_path}")
            
            # PASO 3: Crear thumbnail
            thumbnail_path = self.video_creator.create_thumbnail(
                generated_content.title,
                []  # Las imágenes se obtienen dentro del método
            )
            
            if thumbnail_path:
                result["thumbnail_path"] = thumbnail_path
                logger.info(f"Thumbnail creado: {thumbnail_path}")
            
            # PASO 4: Preparar metadatos para YouTube
            metadata = VideoMetadata(
                title=generated_content.title,
                description=generated_content.description,
                tags=generated_content.tags,
                privacy_status=privacy,
                thumbnail_path=thumbnail_path if thumbnail_path else None
            )
            
            # PASO 5: Publicar en YouTube
            if publish_immediately:
                logger.info("Publicando video en YouTube")
                
                upload_result = self.youtube_publisher.upload_video(video_path, metadata)
                result["steps_completed"].append("youtube_upload")
                
                if upload_result.success:
                    result["youtube_url"] = upload_result.url
                    result["video_id"] = upload_result.video_id
                    logger.info(f"Video publicado: {upload_result.url}")
                else:
                    result["errors"].append(f"Error en upload: {upload_result.error_message}")
                    logger.error(f"Error en upload: {upload_result.error_message}")
            else:
                logger.info("Video preparado (no publicado)")
            
            # Limpiar archivos temporales
            self.video_creator.cleanup_temp_files()
            
            # Resultado final
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            result.update({
                "success": True,
                "end_time": end_time.isoformat(),
                "processing_time_seconds": processing_time,
                "processing_time_minutes": round(processing_time / 60, 2)
            })
            
            logger.info(f"Proceso completado en {processing_time:.1f} segundos")
            return result
            
        except Exception as e:
            error_msg = f"Error en el proceso: {str(e)}"
            result["errors"].append(error_msg)
            logger.error(error_msg, exc_info=True)
            return result
    
    async def batch_create_videos(self, topics: list, content_type: str = "TOP_5", 
                                count: int = None) -> list:
        """
        Crea múltiples videos en lote.
        
        Args:
            topics: Lista de temas
            content_type: Tipo de contenido
            count: Número máximo de videos a crear
            
        Returns:
            list: Resultados de cada video
        """
        
        if count:
            topics = topics[:count]
        
        results = []
        
        for i, topic in enumerate(topics, 1):
            logger.info(f"Procesando video {i}/{len(topics)}: {topic}")
            
            try:
                result = await self.create_and_publish_video(
                    topic=topic,
                    content_type=content_type,
                    privacy="private",  # Siempre privado en lote
                    publish_immediately=False
                )
                
                results.append(result)
                
                # Pausa entre videos para evitar rate limits
                if i < len(topics):
                    await asyncio.sleep(30)
                    
            except Exception as e:
                logger.error(f"Error procesando {topic}: {e}")
                results.append({
                    "success": False,
                    "topic": topic,
                    "error": str(e)
                })
        
        return results
    
    def get_suggested_topics(self, category: str = "general") -> list:
        """
        Obtiene temas sugeridos para crear contenido.
        
        Args:
            category: Categoría de temas
            
        Returns:
            list: Lista de temas sugeridos
        """
        
        topics_by_category = {
            "general": [
                "animales más venenosos",
                "datos que no conoces",
                "inventos raros",
                "hechos del espacio",
                "trucos del cuerpo",
                "lugares prohibidos",
                "comidas extrañas",
                "records locos",
                "curiosidades virales",
                "datos perturbadores"
            ],
            "ciencia": [
                "experimentos científicos más peligrosos",
                "descubrimientos que cambiaron el mundo",
                "teorías científicas más controversiales",
                "elementos químicos más raros",
                "planetas más extraños del universo",
                "especies animales recién descubiertas",
                "enfermedades más raras del mundo",
                "inventos científicos fallidos",
                "científicos más geniales de la historia",
                "predicciones científicas del futuro"
            ],
            "historia": [
                "batallas más épicas de la historia",
                "emperadores más poderosos",
                "civilizaciones más avanzadas",
                "tesoros perdidos más valiosos",
                "conspiraciones históricas reales",
                "personajes históricos más influyentes",
                "inventos de la antiguedad",
                "culturas más fascinantes",
                "monumentos antiguos más impresionantes",
                "tradiciones históricas más extrañas"
            ]
        }
        
        return topics_by_category.get(category, topics_by_category["general"])

async def main():
    """Función principal para ejecutar la automatización."""
    
    # Configurar logging para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)
    
    automation = YouTubeAutomation()
    
    # Ejemplo: crear un Short individual
    topic = "datos perturbadores del océano"
    
    logger.info(f"Iniciando automatización para: {topic}")
    
    try:
        result = await automation.create_and_publish_video(
            topic=topic,
            content_type="CURIOSIDADES",  # Mejor para Shorts
            privacy="private",
            publish_immediately=False  # Cambiar a True para publicar
        )
        
        print("\n" + "="*60)
        print("RESULTADO DE LA AUTOMATIZACIÓN")
        print("="*60)
        print(f"Tema: {result['topic']}")
        print(f"Éxito: {result['success']}")
        print(f"Pasos completados: {', '.join(result['steps_completed'])}")
        
        if result["success"]:
            content = result.get("generated_content", {})
            print(f"Título generado: {content.get('title', 'N/A')}")
            print(f"Duración: {content.get('duration', 0)} segundos")
            print(f"SEO Score: {content.get('seo_score', 0):.1f}/100")
            print(f"Video guardado en: {result.get('video_path', 'N/A')}")
            
            if "youtube_url" in result:
                print(f"URL de YouTube: {result['youtube_url']}")
        
        if result.get("errors"):
            print(f"Errores: {', '.join(result['errors'])}")
        
        print(f"Tiempo total: {result.get('processing_time_minutes', 0):.1f} minutos")
        print("="*60)
        
    except KeyboardInterrupt:
        logger.info("Proceso interrumpido por el usuario")
    except Exception as e:
        logger.error(f"Error en main: {e}", exc_info=True)

def show_config_info():
    """Muestra información de configuración actual."""
    try:
        from config.localization import LANGUAGES_CONFIG, THEMES_CONFIG
        
        print("\n🌍 CONFIGURACIÓN ACTUAL")
        print("=" * 30)
        print(f"📍 Idioma: {settings.LANGUAGE}")
        if settings.LANGUAGE in LANGUAGES_CONFIG:
            lang_info = LANGUAGES_CONFIG[settings.LANGUAGE]
            print(f"   Nombre: {lang_info['name']}")
            print(f"   Voz: {settings.TTS_VOICE}")
        
        print(f"🎬 Tema: {settings.THEME}")
        
        print(f"\n💡 Para cambiar, usa variables de entorno:")
        print(f"   CONTENT_LANGUAGE={settings.LANGUAGE}")
        print(f"   CONTENT_THEME={settings.THEME}")
        print()
        
    except ImportError:
        print(f"📍 Idioma: {settings.LANGUAGE}")
        print(f"🎬 Tema: {settings.THEME}")

if __name__ == "__main__":
    # Verificar configuración básica
    if not settings.OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY no configurada")
        print("📝 Copia .env.example a .env y configura tus APIs")
        sys.exit(1)
    
    print("🚀 YouTube Shorts IA Automate")
    print("=" * 40)
    
    # Mostrar configuración
    show_config_info()
    
    print(f"📁 Directorio: {settings.PROJECT_ROOT}")
    print(f"🔧 Debug: {settings.DEBUG}")
    
    # Ejecutar automatización
    asyncio.run(main())