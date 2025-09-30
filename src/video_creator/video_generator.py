"""
Creador de videos automatizado para YouTube Shorts.
Versión simplificada que funciona sin dependencias pesadas.
"""

import logging
import os
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import requests
from io import BytesIO
import edge_tts

# Imagen processing básico
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL no disponible. Funciones de imagen limitadas.")

logger = logging.getLogger(__name__)

def clean_filename(filename: str, max_length: int = 50) -> str:
    """Limpia un string para ser usado como nombre de archivo válido."""
    import re
    # Remover caracteres no permitidos en Windows
    cleaned = re.sub(r'[<>:"/\|?*\*\*]', '', filename)
    # Reemplazar espacios y caracteres especiales
    cleaned = re.sub(r'[\s\-\.\_]+', '_', cleaned)
    # Remover caracteres no ASCII
    cleaned = re.sub(r'[^\w\-_]', '', cleaned)
    # Limitar longitud y remover underscores múltiples
    cleaned = re.sub(r'_+', '_', cleaned)[:max_length].strip('_')
    return cleaned or 'video_sin_titulo'

@dataclass
class VideoAssets:
    """Assets necesarios para crear un video."""
    audio_file: str
    images: List[str]
    background_music: Optional[str] = None
    intro_video: Optional[str] = None
    outro_video: Optional[str] = None

@dataclass 
class VideoConfig:
    """Configuración del video a generar (optimizado para Shorts)."""
    title: str
    script: str
    duration: int
    resolution: Tuple[int, int] = (1080, 1920)  # Vertical 9:16 para Shorts
    fps: int = 30
    background_color: str = "#000000"  # Negro para mejor contraste
    text_color: str = "#ffffff"
    font_size: int = 72  # Texto más grande para móvil
    is_short: bool = True
    text_position: str = "center"  # Posición del texto
    show_captions: bool = True  # Subtítulos siempre visibles

class VideoCreator:
    """Creador principal de videos automatizados para Shorts."""
    
    def __init__(self):
        """Inicializa el creador de videos."""
        # Obtener rutas del proyecto
        project_root = Path(__file__).parent.parent.parent
        self.output_dir = project_root / "output" / "videos"
        self.temp_dir = project_root / "output" / "temp"
        
        # Crear directorios necesarios
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración localizada
        try:
            from config.settings import settings
            self.tts_voice = getattr(settings, 'TTS_VOICE', 'es-ES-AlvaroNeural')
            self.language = getattr(settings, 'LANGUAGE', 'es')
        except ImportError:
            self.tts_voice = 'es-ES-AlvaroNeural' 
            self.language = 'es'
        
        # 🎬 NUEVOS SISTEMAS VISUALES PROFESIONALES
        try:
            from .simple_video_creator import SimpleVideoCreator
            
            self.simple_video_creator = SimpleVideoCreator()
            logger.info("🎯 Sistema de video avanzado con subtítulos activado")
            self.use_new_system = True
        except ImportError as e:
            logger.warning(f"⚠️ Sistema avanzado no disponible: {e}")
            self.simple_video_creator = None
            self.use_new_system = False
        
        logger.info(f"VideoCreator inicializado - Voz: {self.tts_voice}")
    
    async def _create_advanced_video(self, config: VideoConfig, audio_file: Path) -> str:
        """
        🚀 CREA VIDEO CON SISTEMA AVANZADO: FONDOS DINÁMICOS + SUBTÍTULOS
        """
        logger.info("🎬 Usando sistema avanzado de video con subtítulos dinámicos")
        
        try:
            import subprocess
            import os
            from mutagen.mp3 import MP3
            
            # 1. Obtener duración del audio
            try:
                audio = MP3(str(audio_file))
                audio_duration = audio.info.length
            except:
                # Fallback con subprocess
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
                    '-of', 'csv=p=0', str(audio_file)
                ], capture_output=True, text=True)
                audio_duration = float(result.stdout.strip()) if result.stdout.strip() else 30.0
            
            logger.info(f"� Duración del audio: {audio_duration:.1f}s")
            
            # 2. Generar frames con subtítulos dinámicos usando Whisper
            frame_paths = self.simple_video_creator.generate_video_frames_with_whisper(
                config, str(audio_file), audio_duration
            )
            
            logger.info(f"� Generados {len(frame_paths)} frames")
            
            # 3. Crear video final con FFmpeg
            clean_title = clean_filename(config.title, 40)
            output_path = self.output_dir / f"short_{clean_title}.mp4"
            
            # Comando FFmpeg
            ffmpeg_command = self.simple_video_creator.frames_to_video_command(
                frame_paths, str(audio_file), str(output_path)
            )
            
            logger.info("🎬 Creando video final con FFmpeg...")
            
            # Ejecutar FFmpeg
            result = subprocess.run(ffmpeg_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Limpiar frames temporales
                import shutil
                frames_dir = Path(frame_paths[0]).parent
                shutil.rmtree(frames_dir, ignore_errors=True)
                
                logger.info(f"✅ Video avanzado creado exitosamente: {output_path}")
                return str(output_path)
            else:
                logger.error(f"❌ Error de FFmpeg: {result.stderr}")
                raise Exception(f"FFmpeg falló: {result.stderr}")
                
        except Exception as e:
            logger.error(f"❌ Error creando video avanzado: {e}")
            logger.info("🔄 Fallback al sistema clásico")
            raise e
    
    async def create_video(self, config: VideoConfig) -> str:
        """
        Crea un video completo automaticamente.
        
        Args:
            config: Configuración del video
            
        Returns:
            str: Path del video generado
        """
        logger.info(f"Creando Short: {config.title}")
        
        try:
            # 1. Generar audio con TTS
            clean_title = clean_filename(config.title)
            audio_file = await self._generate_tts_audio(config.script, clean_title)
            
            # 🚀 USAR SISTEMA AVANZADO SI ESTÁ DISPONIBLE
            if self.use_new_system and self.simple_video_creator:
                try:
                    logger.info("🎯 Usando sistema avanzado con fondos dinámicos y subtítulos")
                    video_path = await self._create_advanced_video(config, Path(audio_file))
                    logger.info(f"✅ Sistema avanzado completado exitosamente: {video_path}")
                    return video_path
                except Exception as e:
                    logger.error(f"❌ Error creando video avanzado: {e}")
                    logger.warning(f"⚠️ Sistema avanzado falló: {e}")
                    logger.info("🔄 Usando sistema clásico como fallback")
                    import traceback
                    traceback.print_exc()
            
            # 2. Sistema clásico como fallback
            logger.info("📱 Usando sistema clásico de imágenes CON SUBTÍTULOS")
            images = await self._prepare_images(config.title)
            
            # 3. Crear estructura básica del video CON SUBTÍTULOS
            video_info = self._create_video_structure_with_subtitles(config, Path(audio_file), images)
            
            logger.info(f"Estructura de video creada: {video_info['output_file']}")
            return video_info['output_file']
            
        except Exception as e:
            logger.error(f"Error creando video: {e}")
            raise
    
    async def _generate_tts_audio(self, script: str, title: str) -> str:
        """Genera audio usando Edge TTS (gratuito)."""
        
        # Asegurar que el directorio temporal existe
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Limpiar script para TTS
        clean_script = self._clean_script_for_tts(script)
        
        # Usar voz configurada dinámicamente
        voice = self.tts_voice
        
        # Nombre de archivo seguro
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:20]
        output_file = self.temp_dir / f"audio_{safe_title.replace(' ', '_')}.mp3"
        
        logger.info(f"Intentando generar audio en: {output_file}")
        
        try:
            # Generar audio con Edge TTS
            logger.info(f"Generando TTS con voz {voice}...")
            communicate = edge_tts.Communicate(clean_script, voice)
            await communicate.save(str(output_file))
            
            # Verificar que el archivo se creó
            if output_file.exists():
                logger.info(f"✓ Audio TTS generado exitosamente: {output_file}")
                return str(output_file)
            else:
                raise ValueError(f"El archivo de audio no se creó: {output_file}")
            
        except Exception as e:
            logger.error(f"Error generando TTS: {e}")
            logger.error(f"Script limpio: {clean_script[:100]}...")
            raise ValueError(f"Error en TTS: {e}")
    
    def _clean_script_for_tts(self, script: str) -> str:
        """Limpia el script para optimizar TTS en Shorts."""
        
        # Remover elementos de formato
        clean_text = script.replace("**", "")
        clean_text = clean_text.replace("*", "")
        clean_text = clean_text.replace("#", "")
        clean_text = clean_text.replace("HOOK", "")
        clean_text = clean_text.replace("CTA", "")
        
        # Remover secciones de metadatos
        sections_to_remove = [
            "TÍTULO:",
            "DESCRIPCIÓN:",
            "TAGS:",
            "THUMBNAIL:",
            "DATO 1:",
            "DATO 2:", 
            "DATO 3:",
            "(3s):",
            "(5s):",
            "(12s):",
            "(15s):"
        ]
        
        lines = clean_text.split('\n')
        filtered_lines = []
        
        for line in lines:
            line = line.strip()
            # Filtrar líneas vacías y secciones no deseadas
            if line and not any(section in line.upper() for section in sections_to_remove):
                # Limpiar números de lista al inicio
                if line.startswith(('1.', '2.', '3.', '4.', '5.')):
                    line = line[2:].strip()
                filtered_lines.append(line)
        
        # Unir con pausas naturales para Shorts
        result = '. '.join(filtered_lines)
        
        # Optimizaciones específicas para Shorts
        result = result.replace('TOP 5', 'Top cinco')
        result = result.replace('TOP5', 'Top cinco') 
        result = result.replace('¿Sabías que', 'Sabías que')
        result = result.replace('...', '.')
        
        # Limitar longitud para Shorts (45-60 segundos máximo)
        return result[:1500]  # Límite de caracteres para TTS de Shorts
    
    async def _prepare_images(self, topic: str, count: int = 3) -> List[str]:
        """Prepara imágenes dinámicas basadas en la temática."""
        
        # Obtener tema actual (del settings o detectar automáticamente)
        try:
            from config.settings import settings
            current_theme = getattr(settings, 'THEME', 'curiosidades')
        except:
            current_theme = 'curiosidades'
        
        # Para Shorts solo necesitamos pocas imágenes de alta calidad
        try:
            # Intentar buscar imágenes reales si hay API
            images = await self._fetch_images_simple(topic, count)
            
            if not images:
                # Crear imágenes dinámicas basadas en temática
                images = self._create_placeholder_images(count, topic, current_theme)
            
            logger.info(f"✓ Preparadas {len(images)} imágenes temáticas para: {topic}")
            return images
            
        except Exception as e:
            logger.error(f"Error preparando imágenes: {e}")
            return self._create_placeholder_images(count, topic, current_theme)
    
    async def _fetch_images_simple(self, topic: str, count: int = 3) -> List[str]:
        """Busca imágenes de forma simplificada."""
        
        # Por ahora retornamos lista vacía, se implementará con APIs
        # cuando se configure Unsplash o Pexels
        return []
    
    def _create_placeholder_images(self, count: int = 3, topic: str = "", theme: str = "") -> List[str]:
        """Crea imágenes dinámicas basadas en temática y tópico."""
        
        if not PIL_AVAILABLE:
            logger.warning("PIL no disponible. No se pueden crear placeholders.")
            return []
        
        placeholder_images = []
        
        # Obtener configuración dinámica basada en tema y tópico
        theme_config = self._get_dynamic_theme_config(topic, theme)
        
        for i in range(count):
            try:
                # Crear imagen base 9:16 para Shorts
                img = Image.new('RGB', (1080, 1920))
                
                # CREAR GRADIENTE DINÁMICO BASADO EN TEMÁTICA
                img = self._create_dynamic_background(theme_config, i)
                
                draw = ImageDraw.Draw(img)
                
                # AÑADIR EFECTOS DINÁMICOS SEGÚN TEMÁTICA
                img = self._add_dynamic_effects(img, theme_config, i)
                
                # TEXTO PRINCIPAL CLICKBAIT DINÁMICO
                title = self._generate_dynamic_title(topic, theme, i, theme_config)
                
                # Fuente para título principal
                try:
                    title_font = ImageFont.truetype("arial.ttf", 85)  # Más pequeño
                    subtitle_font = ImageFont.truetype("arial.ttf", 45)
                except:
                    title_font = ImageFont.load_default()
                    subtitle_font = ImageFont.load_default()
                
                # DISEÑO PROFESIONAL CON CAPAS
                
                # 1. Fondo semi-transparente para texto
                text_bg_height = 400
                text_bg_y = (1920 - text_bg_height) // 2
                
                # Rectángulo con gradiente oscuro
                for y in range(text_bg_y, text_bg_y + text_bg_height):
                    alpha = int(180 * (1 - abs(y - (text_bg_y + text_bg_height/2)) / (text_bg_height/2)))
                    for x in range(100, 980):  # Márgenes laterales
                        current_pixel = img.getpixel((x, y))
                        new_pixel = (
                            max(0, current_pixel[0] - alpha//3),
                            max(0, current_pixel[1] - alpha//3),
                            max(0, current_pixel[2] - alpha//4)
                        )
                        img.putpixel((x, y), new_pixel)
                
                # 2. Texto con sombra y outline
                lines = title.split('\n')
                line_height = 90
                total_height = len(lines) * line_height
                start_y = (1920 - total_height) // 2
                
                for j, line in enumerate(lines):
                    y_pos = start_y + j * line_height
                    
                    # Obtener tamaño del texto
                    bbox = draw.textbbox((0, 0), line, font=title_font)
                    text_width = bbox[2] - bbox[0]
                    x_pos = (1080 - text_width) // 2
                    
                    # Outline negro grueso (múltiples capas)
                    for offset_x in [-3, -2, -1, 0, 1, 2, 3]:
                        for offset_y in [-3, -2, -1, 0, 1, 2, 3]:
                            if offset_x != 0 or offset_y != 0:
                                draw.text(
                                    (x_pos + offset_x, y_pos + offset_y), 
                                    line, 
                                    fill=(0, 0, 0), 
                                    font=title_font
                                )
                    
                    # Texto principal blanco
                    draw.text((x_pos, y_pos), line, fill=(255, 255, 255), font=title_font)
                
                # 3. Subtítulo inferior
                subtitle = f"TOP {i+1} IMPACTANTE"
                bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
                subtitle_width = bbox[2] - bbox[0]
                subtitle_x = (1080 - subtitle_width) // 2
                subtitle_y = start_y + total_height + 50
                
                # Outline para subtítulo
                for offset_x in [-2, -1, 0, 1, 2]:
                    for offset_y in [-2, -1, 0, 1, 2]:
                        if offset_x != 0 or offset_y != 0:
                            draw.text(
                                (subtitle_x + offset_x, subtitle_y + offset_y), 
                                subtitle, 
                                fill=(0, 0, 0), 
                                font=subtitle_font
                            )
                
                draw.text((subtitle_x, subtitle_y), subtitle, fill=(255, 255, 0), font=subtitle_font)
                
                # 4. Elemento decorativo (líneas de énfasis)
                line_y1 = start_y - 30
                line_y2 = subtitle_y + 80
                
                for thickness in range(5):
                    draw.line([(200, line_y1 + thickness), (880, line_y1 + thickness)], fill=(255, 255, 255))
                    draw.line([(200, line_y2 + thickness), (880, line_y2 + thickness)], fill=(255, 255, 255))
                
                # Guardar imagen
                safe_theme = "".join(c for c in theme if c.isalnum())[:10] or "generic"
                img_path = self.temp_dir / f"{safe_theme}_image_{i+1}.jpg"
                img.save(img_path, quality=90, optimize=True)
                placeholder_images.append(str(img_path))
                
                logger.info(f"✓ Imagen temática profesional creada: {img_path.name}")
                
            except Exception as e:
                logger.error(f"Error creando imagen temática {i}: {e}")
        
        return placeholder_images
    
    def _get_dynamic_theme_config(self, topic: str, theme: str) -> Dict:
        """Genera configuración dinámica basada en tema y tópico."""
        
        # Detectar temática automáticamente
        topic_lower = topic.lower()
        theme_lower = theme.lower()
        
        # Mapeo de temáticas a configuraciones
        if any(word in topic_lower for word in ['océano', 'mar', 'marina', 'agua', 'pez', 'ballena', 'tiburón']):
            return {
                'colors': [(0, 50, 120), (20, 80, 150), (40, 120, 180)],
                'accent_color': (100, 200, 255),
                'effect_type': 'bubbles',
                'keywords': ['OCÉANO', 'MARINO', 'PROFUNDO', 'ABISMO', 'MISTERIOSO']
            }
        elif any(word in topic_lower for word in ['espacio', 'planeta', 'galaxia', 'estrella', 'universo', 'nasa']):
            return {
                'colors': [(10, 10, 30), (30, 20, 60), (60, 40, 100)],
                'accent_color': (200, 150, 255),
                'effect_type': 'stars',
                'keywords': ['ESPACIO', 'GALÁCTICO', 'CÓSMICO', 'INFINITO', 'ALIENÍGENA']
            }
        elif any(word in topic_lower for word in ['tecnología', 'ia', 'robot', 'futuro', 'digital', 'cyber']):
            return {
                'colors': [(0, 30, 30), (20, 60, 60), (40, 100, 100)],
                'accent_color': (0, 255, 255),
                'effect_type': 'circuits',
                'keywords': ['TECH', 'DIGITAL', 'FUTURO', 'IA', 'INNOVACIÓN']
            }
        elif any(word in topic_lower for word in ['historia', 'antiguo', 'civilización', 'pasado', 'arqueología']):
            return {
                'colors': [(60, 40, 20), (100, 70, 40), (140, 100, 60)],
                'accent_color': (255, 215, 0),
                'effect_type': 'ancient',
                'keywords': ['HISTORIA', 'ANTIGUO', 'PERDIDO', 'SECRETO', 'LEGENDARIO']
            }
        elif any(word in topic_lower for word in ['comida', 'cocina', 'receta', 'chef', 'gastronomía']):
            return {
                'colors': [(80, 20, 20), (120, 40, 40), (160, 80, 60)],
                'accent_color': (255, 150, 50),
                'effect_type': 'food',
                'keywords': ['DELICIOSO', 'SABROSO', 'INCREÍBLE', 'VIRAL', 'ÉPICO']
            }
        elif any(word in topic_lower for word in ['deporte', 'fútbol', 'basketball', 'atleta', 'competencia']):
            return {
                'colors': [(20, 80, 20), (40, 120, 40), (60, 160, 60)],
                'accent_color': (255, 255, 100),
                'effect_type': 'energy',
                'keywords': ['ÉPICO', 'INCREÍBLE', 'BRUTAL', 'INSANO', 'VIRAL']
            }
        elif any(word in topic_lower for word in ['ciencia', 'experimento', 'laboratorio', 'química', 'física']):
            return {
                'colors': [(40, 40, 80), (60, 60, 120), (80, 80, 160)],
                'accent_color': (150, 255, 150),
                'effect_type': 'science',
                'keywords': ['CIENCIA', 'LOCO', 'EXPERIMENTO', 'INCREÍBLE', 'IMPOSIBLE']
            }
        else:
            # Configuración genérica pero atractiva
            return {
                'colors': [(40, 40, 80), (80, 60, 120), (120, 100, 160)],
                'accent_color': (255, 200, 100),
                'effect_type': 'generic',
                'keywords': ['INCREÍBLE', 'IMPACTANTE', 'VIRAL', 'ÉPICO', 'INSANO']
            }
    
    def _generate_dynamic_title(self, topic: str, theme: str, index: int, theme_config: Dict) -> str:
        """Genera títulos clickbait dinámicos basados en el contenido."""
        
        keywords = theme_config['keywords']
        
        # Extraer palabras clave del tópico
        topic_words = topic.upper().split()
        main_word = topic_words[0] if topic_words else "DATOS"
        
        # Plantillas de clickbait dinámicas
        templates = [
            f"DATOS {keywords[0]}\nDE {main_word}",
            f"SECRETOS {keywords[1]}\nQUE NO SABÍAS", 
            f"LO MÁS {keywords[2]}\nDEL MUNDO",
            f"{keywords[3]} HECHOS\nQUE TE IMPACTARÁN",
            f"MISTERIOS {keywords[4]}\nREVELADOS"
        ]
        
        return templates[index % len(templates)]
    
    def _create_dynamic_background(self, theme_config: Dict, index: int) -> Image.Image:
        """Crea fondo fotorrealista dinámico basado en la configuración temática."""
        
        img = Image.new('RGB', (1080, 1920))
        colors = theme_config['colors']
        effect_type = theme_config['effect_type']
        
        # Crear fondo fotorrealista según la temática
        if effect_type == 'bubbles':  # Océano
            img = self._create_ocean_background(colors, index)
        elif effect_type == 'stars':  # Espacio
            img = self._create_space_background(colors, index)
        elif effect_type == 'circuits':  # Tecnología
            img = self._create_tech_background(colors, index)
        elif effect_type == 'ancient':  # Historia
            img = self._create_ancient_background(colors, index)
        elif effect_type == 'food':  # Comida
            img = self._create_food_background(colors, index)
        elif effect_type == 'energy':  # Deportes
            img = self._create_sports_background(colors, index)
        elif effect_type == 'science':  # Ciencia
            img = self._create_science_background(colors, index)
        else:  # Genérico
            img = self._create_generic_realistic_background(colors, index)
        
        return img
    
    def _add_dynamic_effects(self, img: Image.Image, theme_config: Dict, index: int) -> Image.Image:
        """Añade efectos dinámicos según la temática."""
        
        import random
        random.seed(42 + index)
        draw = ImageDraw.Draw(img)
        effect_type = theme_config['effect_type']
        accent_color = theme_config['accent_color']
        
        if effect_type == 'bubbles':  # Océano
            for _ in range(40):
                x = random.randint(0, 1080)
                y = random.randint(300, 1920)
                size = random.randint(5, 20)
                draw.ellipse([x-size, y-size, x+size, y+size], fill=(*accent_color, 60))
                
        elif effect_type == 'stars':  # Espacio
            for _ in range(60):
                x = random.randint(0, 1080)
                y = random.randint(0, 1920)
                size = random.randint(2, 8)
                draw.ellipse([x-size, y-size, x+size, y+size], fill=accent_color)
                
        elif effect_type == 'circuits':  # Tecnología
            for _ in range(30):
                x1, y1 = random.randint(0, 1080), random.randint(0, 1920)
                x2, y2 = x1 + random.randint(-100, 100), y1 + random.randint(-100, 100)
                draw.line([(x1, y1), (x2, y2)], fill=accent_color, width=2)
                
        elif effect_type == 'energy':  # Deportes
            for _ in range(20):
                x = random.randint(0, 1080)
                y = random.randint(0, 1920)
                w, h = random.randint(10, 50), random.randint(5, 15)
                draw.ellipse([x, y, x+w, y+h], fill=accent_color)
                
        else:  # Efectos genéricos
            for _ in range(25):
                x = random.randint(0, 1080)
                y = random.randint(0, 1920)
                size = random.randint(3, 15)
                draw.rectangle([x, y, x+size, y+size], fill=accent_color)
        
        return img
    
    def _create_ocean_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo oceánico fotorrealista con ondas y profundidad."""
        
        img = Image.new('RGB', (1080, 1920))
        import math
        
        # Simular capas oceánicas realistas
        for y in range(1920):
            for x in range(1080):
                # Profundidad oceánica (más oscuro hacia abajo)
                depth = y / 1920
                
                # Ondas sinusoidales realistas
                wave1 = math.sin(x * 0.01 + y * 0.003) * 30
                wave2 = math.sin(x * 0.007 + y * 0.005) * 20
                wave3 = math.sin(x * 0.013 + y * 0.002) * 15
                
                # Rayos de luz que penetran
                light_ray = max(0, 100 - depth * 150 + wave1 + wave2)
                
                # Color base oceánico
                base_blue = int(colors[0][2] + depth * (colors[2][2] - colors[0][2]))
                base_green = int(colors[0][1] + depth * (colors[2][1] - colors[0][1]) + light_ray * 0.3)
                base_red = int(colors[0][0] + depth * (colors[2][0] - colors[0][0]) + light_ray * 0.1)
                
                # Efectos de ondas
                final_r = max(0, min(255, int(base_red + wave3)))
                final_g = max(0, min(255, int(base_green + wave1 * 0.5)))
                final_b = max(0, min(255, int(base_blue + wave2 * 0.3)))
                
                img.putpixel((x, y), (final_r, final_g, final_b))
        
        return img
    
    def _create_space_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo espacial fotorrealista con nebulosas y estrellas."""
        
        img = Image.new('RGB', (1080, 1920))
        import math, random
        
        # Base nebulosa cósmica
        for y in range(1920):
            for x in range(1080):
                # Nebulosa con patrones fractales
                distance = math.sqrt((x - 540)**2 + (y - 960)**2) / 1000
                noise1 = math.sin(x * 0.005) * math.cos(y * 0.007) * 50
                noise2 = math.sin(x * 0.003 + y * 0.004) * 30
                
                # Colores cósmicos
                cosmic_intensity = max(0, 100 - distance * 80 + noise1 + noise2)
                
                r = max(0, min(255, colors[0][0] + cosmic_intensity * 0.8))
                g = max(0, min(255, colors[1][1] + cosmic_intensity * 0.6))
                b = max(0, min(255, colors[2][2] + cosmic_intensity))
                
                img.putpixel((x, y), (int(r), int(g), int(b)))
        
        # Añadir estrellas realistas
        random.seed(42 + index)
        for _ in range(200):
            star_x = random.randint(0, 1079)
            star_y = random.randint(0, 1919)
            brightness = random.randint(150, 255)
            size = random.choice([1, 1, 1, 2, 2, 3])  # Más estrellas pequeñas
            
            # Estrella con halo
            for dx in range(-size, size + 1):
                for dy in range(-size, size + 1):
                    if 0 <= star_x + dx < 1080 and 0 <= star_y + dy < 1920:
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance <= size:
                            star_brightness = int(brightness * (1 - distance / (size + 1)))
                            current = img.getpixel((star_x + dx, star_y + dy))
                            new_color = (
                                min(255, current[0] + star_brightness),
                                min(255, current[1] + star_brightness),
                                min(255, current[2] + star_brightness)
                            )
                            img.putpixel((star_x + dx, star_y + dy), new_color)
        
        return img
    
    def _create_tech_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo tecnológico con circuitos y patrones digitales."""
        
        img = Image.new('RGB', (1080, 1920))
        import math
        
        # Patrón de circuito base
        for y in range(1920):
            for x in range(1080):
                # Patrón de rejilla tecnológica
                grid_x = (x // 40) % 2
                grid_y = (y // 40) % 2
                grid_intensity = (grid_x + grid_y) % 2 * 20
                
                # Líneas de circuito
                circuit_line = 0
                if x % 80 < 3 or y % 120 < 3:
                    circuit_line = 40
                
                # Pulso digital
                pulse = math.sin(x * 0.02 + y * 0.01) * 15
                
                # Color tecnológico
                base_color = colors[1] if (x + y) % 100 < 50 else colors[0]
                
                r = max(0, min(255, base_color[0] + grid_intensity + circuit_line))
                g = max(0, min(255, base_color[1] + grid_intensity + circuit_line + pulse))
                b = max(0, min(255, base_color[2] + grid_intensity + circuit_line + pulse * 0.5))
                
                img.putpixel((x, y), (int(r), int(g), int(b)))
        
        return img
    
    def _create_ancient_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo histórico con texturas de piedra y pergamino."""
        
        img = Image.new('RGB', (1080, 1920))
        import math
        
        # Textura de piedra/pergamino
        for y in range(1920):
            for x in range(1080):
                # Textura rugosa
                texture1 = math.sin(x * 0.1) * math.cos(y * 0.08) * 20
                texture2 = math.sin(x * 0.05 + y * 0.07) * 15
                aged_effect = math.sin(x * 0.03) * math.sin(y * 0.04) * 10
                
                # Vetas de edad
                age_lines = 0
                if (x + y * 0.5) % 200 < 5:
                    age_lines = 25
                
                # Color envejecido
                base_color = colors[index % len(colors)]
                
                r = max(0, min(255, base_color[0] + texture1 + aged_effect + age_lines))
                g = max(0, min(255, base_color[1] + texture2 + aged_effect + age_lines))
                b = max(0, min(255, base_color[2] + texture1 * 0.5 + aged_effect))
                
                img.putpixel((x, y), (int(r), int(g), int(b)))
        
        return img
    
    def _create_food_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo gastronómico con texturas orgánicas."""
        
        img = Image.new('RGB', (1080, 1920))
        import math
        
        # Textura orgánica/culinaria
        for y in range(1920):
            for x in range(1080):
                # Patrones orgánicos
                organic1 = math.sin(x * 0.02) * math.cos(y * 0.025) * 30
                organic2 = math.sin(x * 0.015 + y * 0.02) * 25
                
                # Efectos de cocción/caramelización
                heat_effect = max(0, math.sin(y * 0.01) * 20)
                
                # Color gastronómico cálido
                base_color = colors[(x + y) // 200 % len(colors)]
                
                r = max(0, min(255, base_color[0] + organic1 + heat_effect))
                g = max(0, min(255, base_color[1] + organic2 + heat_effect * 0.7))
                b = max(0, min(255, base_color[2] + organic1 * 0.3))
                
                img.putpixel((x, y), (int(r), int(g), int(b)))
        
        return img
    
    def _create_sports_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo deportivo con energía y movimiento."""
        
        img = Image.new('RGB', (1080, 1920))
        import math
        
        # Patrones de energía y velocidad
        for y in range(1920):
            for x in range(1080):
                # Líneas de velocidad
                speed_lines = 0
                if (x + y * 2) % 60 < 8:
                    speed_lines = 40
                
                # Energía radiante
                center_distance = math.sqrt((x - 540)**2 + (y - 960)**2)
                energy = max(0, 100 - center_distance * 0.1) * math.sin(center_distance * 0.01)
                
                # Pulso deportivo
                pulse = math.sin(x * 0.01 + y * 0.008) * 20
                
                base_color = colors[index % len(colors)]
                
                r = max(0, min(255, base_color[0] + speed_lines + energy * 0.3))
                g = max(0, min(255, base_color[1] + speed_lines + energy + pulse))
                b = max(0, min(255, base_color[2] + speed_lines * 0.5 + pulse))
                
                img.putpixel((x, y), (int(r), int(g), int(b)))
        
        return img
    
    def _create_science_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo científico con patrones moleculares."""
        
        img = Image.new('RGB', (1080, 1920))
        import math
        
        # Estructura molecular/cristalina
        for y in range(1920):
            for x in range(1080):
                # Patrón hexagonal (como moléculas)
                hex_pattern = (math.sin(x * 0.02) + math.sin(y * 0.02) + 
                             math.sin((x + y) * 0.015)) * 20
                
                # Ondas científicas
                wave_pattern = math.sin(x * 0.005) * math.cos(y * 0.007) * 25
                
                # Enlaces moleculares
                bonds = 0
                if (x % 100 < 3 and y % 80 < 3) or (x % 80 < 3 and y % 100 < 3):
                    bonds = 30
                
                base_color = colors[(x // 50 + y // 50) % len(colors)]
                
                r = max(0, min(255, base_color[0] + hex_pattern + bonds))
                g = max(0, min(255, base_color[1] + hex_pattern + wave_pattern + bonds))
                b = max(0, min(255, base_color[2] + wave_pattern + bonds))
                
                img.putpixel((x, y), (int(r), int(g), int(b)))
        
        return img
    
    def _create_generic_realistic_background(self, colors: List[tuple], index: int) -> Image.Image:
        """Crea fondo genérico pero atractivo con patrones abstractos."""
        
        img = Image.new('RGB', (1080, 1920))
        import math
        
        # Patrón abstracto elegante
        for y in range(1920):
            for x in range(1080):
                # Ondas suaves entrelazadas
                wave1 = math.sin(x * 0.008) * math.cos(y * 0.01) * 40
                wave2 = math.sin(x * 0.012 + y * 0.006) * 30
                
                # Gradiente diagonal
                diagonal = (x + y) * 0.05
                gradient_effect = math.sin(diagonal * 0.01) * 20
                
                base_color = colors[((x // 100) + (y // 150)) % len(colors)]
                
                r = max(0, min(255, base_color[0] + wave1 + gradient_effect))
                g = max(0, min(255, base_color[1] + wave2 + gradient_effect))
                b = max(0, min(255, base_color[2] + wave1 * 0.7 + wave2 * 0.5))
                
                img.putpixel((x, y), (int(r), int(g), int(b)))
        
        return img
    
    def _create_video_structure(self, config: VideoConfig, audio_file: str, images: List[str]) -> Dict:
        """
        Genera video MP4 real usando MoviePy.
        """
        
        try:
            # Intentar importar MoviePy v2.x
            try:
                from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
                from moviepy import concatenate_videoclips
                # Importar efectos de transición
                try:
                    from moviepy.video.fx import fadein, fadeout
                except ImportError:
                    # Fallback para transiciones simples
                    fadein = fadeout = None
                moviepy_available = True
            except ImportError:
                logger.warning("MoviePy no instalado. Generando estructura JSON.")
                moviepy_available = False
                fadein = fadeout = None
            
            # Crear directorios necesarios
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Nombre del archivo de salida
            if moviepy_available:
                output_filename = f"short_{clean_filename(config.title)}.mp4"
            else:
                output_filename = f"short_{clean_filename(config.title)}.json"
            
            output_path = str(self.output_dir / output_filename)
            
            if moviepy_available:
                # GENERAR VIDEO MP4 REAL
                
                # VERIFICACIONES EXHAUSTIVAS DEL AUDIO
                if not os.path.exists(audio_file):
                    raise FileNotFoundError(f"❌ Audio no encontrado: {audio_file}")
                
                # Verificar tamaño del archivo de audio
                audio_size = os.path.getsize(audio_file) / 1024  # KB
                logger.info(f"📊 Tamaño del audio: {audio_size:.2f} KB")
                
                if audio_size < 10:  # Menos de 10KB es sospechoso
                    logger.error(f"⚠️  Archivo de audio muy pequeño: {audio_size:.2f}KB")
                
                # Cargar audio para obtener duración real
                try:
                    audio = AudioFileClip(audio_file)
                    real_duration = audio.duration
                    logger.info(f"✅ Audio cargado correctamente")
                    logger.info(f"📏 Duración real del audio: {real_duration:.1f}s")
                    
                    if real_duration <= 0:
                        raise ValueError(f"Audio tiene duración inválida: {real_duration}s")
                        
                except Exception as e:
                    logger.error(f"❌ Error cargando audio: {e}")
                    raise
                
                # Verificar imágenes
                valid_images = []
                for img_path in images:
                    if os.path.exists(img_path):
                        valid_images.append(img_path)
                    else:
                        logger.warning(f"Imagen no encontrada: {img_path}")
                
                if not valid_images:
                    raise FileNotFoundError("No se encontraron imágenes válidas")
                
                # Calcular duración por imagen
                image_duration = real_duration / len(valid_images)
                
                # Crear clips de imagen con EFECTOS VIRALES DINÁMICOS
                video_clips = []
                for i, img_path in enumerate(valid_images):
                    # Crear clip de imagen con duración calculada
                    clip = ImageClip(img_path, duration=image_duration)
                    
                    # Redimensionar a 1080x1920 (formato Shorts) con margen para zoom
                    clip = clip.resized((1200, 2100))  # Más grande para efectos de zoom
                    
                    # 🎬 EFECTOS VIRALES DINÁMICOS 🎬
                    # Efecto 1: Zoom gradual (muy viral)
                    if i % 3 == 0:
                        # Zoom in progresivo
                        clip = clip.resized(lambda t: 1 + 0.3 * t / image_duration)
                    elif i % 3 == 1:
                        # Pan lateral suave
                        clip = clip.with_position(lambda t: ('center', -50 + 100 * t / image_duration))
                    else:
                        # Zoom out + rotación sutil
                        clip = clip.resized(lambda t: 1.3 - 0.2 * t / image_duration)
                    
                    # Recortar al tamaño final de Shorts (sintaxis correcta MoviePy v2.x)
                    clip = clip.cropped(x_center=600, y_center=1050, width=1080, height=1920)
                    
                    # Añadir efectos de transición suaves
                    if fadein and i == 0:
                        clip = fadein(clip, 0.5)
                    if fadeout and i == len(valid_images) - 1:
                        clip = fadeout(clip, 0.5)
                    
                    video_clips.append(clip)
                
                # Concatenar todos los clips
                video = concatenate_videoclips(video_clips, method="compose")
                
                # Ajustar duración exacta del video al audio
                video = video.with_duration(real_duration)
                
                # DIAGNÓSTICOS DETALLADOS DEL AUDIO
                logger.info(f"🔊 === DIAGNÓSTICO DE AUDIO ===")
                logger.info(f"📁 Archivo de audio: {audio_file}")
                logger.info(f"📏 Duración del audio: {audio.duration:.2f}s")
                logger.info(f"🎵 Audio válido: {audio.duration > 0}")
                
                # Verificar propiedades del audio
                try:
                    audio_fps = audio.fps if hasattr(audio, 'fps') else 'N/A'
                    logger.info(f"🎛️  Audio FPS: {audio_fps}")
                except Exception as e:
                    logger.warning(f"⚠️  No se pudo obtener FPS del audio: {e}")
                
                # Añadir audio con verificación robusta
                logger.info(f"� Integrando audio al video...")
                final_video = video.with_audio(audio)
                
                # Verificaciones post-integración
                logger.info(f"✅ Audio integrado: {final_video.audio is not None}")
                if final_video.audio is None:
                    logger.error("❌ FALLO: Audio no se integró correctamente")
                    raise ValueError("Audio no se pudo integrar al video")
                else:
                    logger.info(f"✅ Duración video final: {final_video.duration:.2f}s")
                    logger.info(f"✅ Audio final presente: {hasattr(final_video.audio, 'duration')}")
                
                logger.info(f"Generando video MP4: {output_path}")
                
                # Exportar video optimizado para Shorts con audio garantizado
                logger.info(f"🎬 Exportando con codec de audio: aac")
                logger.info(f"🎵 Archivo temporal de audio: temp-audio.m4a")
                
                final_video.write_videofile(
                    output_path,
                    fps=config.fps,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    write_logfile=False,  # Evitar logs innecesarios
                    audio_bitrate='128k',  # Asegurar bitrate de audio
                    audio=True  # Forzar inclusión de audio
                )
                
                logger.info(f"✅ write_videofile completado exitosamente")
                
                # Limpiar clips de memoria
                final_video.close()
                video.close()
                audio.close()
                for clip in video_clips:
                    clip.close()
                
                logger.info(f"✅ Video MP4 generado exitosamente: {output_path}")
                
                # VERIFICACIÓN FINAL DEL ARCHIVO GENERADO
                try:
                    file_size = os.path.getsize(output_path) / (1024*1024)  # MB
                    logger.info(f"📊 Tamaño del video: {file_size:.2f} MB")
                    
                    # Verificar que el archivo no esté vacío
                    if file_size < 0.1:
                        logger.error(f"⚠️  Video muy pequeño ({file_size:.2f}MB) - posible problema")
                    else:
                        logger.info(f"✅ Video generado correctamente")
                        
                except Exception as e:
                    logger.warning(f"No se pudo verificar el archivo: {e}")
                
                # Información del video
                video_structure = {
                    "config": {
                        "title": config.title,
                        "resolution": config.resolution,
                        "duration": real_duration,
                        "fps": config.fps,
                        "is_short": config.is_short
                    },
                    "assets": {
                        "audio_file": audio_file,
                        "audio_size_kb": audio_size,
                        "images": valid_images,
                        "image_count": len(valid_images)
                    },
                    "timing": {
                        "total_duration": real_duration,
                        "image_duration": image_duration,
                        "audio_fps": audio_fps,
                        "transition_time": 0.5
                    },
                    "output_file": output_path,
                    "status": "completed"
                }
            
            else:
                # FALLBACK: GENERAR SOLO JSON (compatibilidad)
                import json
                
                video_structure = {
                    "config": {
                        "title": config.title,
                        "resolution": config.resolution,
                        "duration": config.duration,
                        "fps": config.fps,
                        "is_short": config.is_short
                    },
                    "assets": {
                        "audio_file": audio_file,
                        "images": images,
                        "image_count": len(images)
                    },
                    "timing": {
                        "total_duration": config.duration,
                        "image_duration": config.duration / max(len(images), 1),
                        "transition_time": 0.5
                    },
                    "output_file": output_path,
                    "status": "structured",
                    "note": "Para generar MP4 real, instala: pip install moviepy"
                }
                
                # Guardar estructura en JSON
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(video_structure, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Estructura JSON guardada: {output_path}")
            
            return video_structure
            
        except Exception as e:
            logger.error(f"Error creando estructura de video: {e}")
            raise
    
    def _create_video_structure_with_subtitles(self, config: VideoConfig, audio_file: Path, images: List[str]) -> Dict:
        """
        Crea estructura de video CON SUBTÍTULOS usando sistema clásico mejorado
        """
        logger.info("🎬 Creando video clásico CON SUBTÍTULOS integrados")
        
        try:
            # Primero crear el video básico
            video_info = self._create_video_structure(config, audio_file, images)
            
            # Verificar MoviePy
            try:
                from moviepy.editor import VideoFileClip
                moviepy_available = True
            except ImportError:
                moviepy_available = False
            
            # Si no hay MoviePy, no se pueden añadir subtítulos
            if not moviepy_available:
                logger.warning("⚠️ MoviePy no disponible - subtítulos no añadidos")
                return video_info
            
            # Añadir subtítulos al video ya creado
            original_video_path = video_info['output_file']
            
            if Path(original_video_path).exists():
                logger.info("📝 Añadiendo subtítulos al video clásico...")
                subtitled_video_path = self._add_subtitles_to_existing_video(
                    original_video_path, config.script, str(audio_file)
                )
                
                if subtitled_video_path:
                    # Actualizar la información del video
                    video_info['output_file'] = subtitled_video_path
                    video_info['subtitles_added'] = True
                    logger.info(f"✅ Subtítulos añadidos exitosamente: {subtitled_video_path}")
                else:
                    logger.warning("⚠️ No se pudieron añadir subtítulos")
                    video_info['subtitles_added'] = False
            
            return video_info
            
        except Exception as e:
            logger.error(f"Error creando video con subtítulos: {e}")
            # Fallback al método original sin subtítulos
            return self._create_video_structure(config, audio_file, images)
    
    def _add_subtitles_to_existing_video(self, video_path: str, script: str, audio_path: str) -> str:
        """
        Añade subtítulos a un video existente usando MoviePy
        """
        try:
            from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
            import os
            
            logger.info("🎬 Procesando subtítulos con MoviePy...")
            
            # Cargar video original
            video = VideoFileClip(video_path)
            
            # Usar Whisper si está disponible, sino usar timing estimado
            if hasattr(self, 'simple_video_creator') and self.simple_video_creator and \
               hasattr(self.simple_video_creator, 'whisper_generator') and \
               self.simple_video_creator.whisper_generator:
                
                try:
                    logger.info("🤖 Extrayendo timestamps con Whisper...")
                    timeline = self.simple_video_creator.whisper_generator.generate_precise_timeline(
                        audio_path, script
                    )
                    subtitle_clips = self._create_moviepy_subtitles_from_timeline(timeline, video.duration)
                except Exception as e:
                    logger.warning(f"⚠️ Whisper falló: {e}, usando timing estimado")
                    subtitle_clips = self._create_moviepy_subtitles_estimated(script, video.duration)
            else:
                logger.info("📝 Usando timing estimado para subtítulos...")
                subtitle_clips = self._create_moviepy_subtitles_estimated(script, video.duration)
            
            # Combinar video con subtítulos
            if subtitle_clips:
                final_video = CompositeVideoClip([video] + subtitle_clips)
                
                # Crear nombre del archivo con subtítulos
                base_name = Path(video_path).stem
                parent_dir = Path(video_path).parent
                subtitled_path = parent_dir / f"{base_name}_with_subtitles.mp4"
                
                # Exportar video con subtítulos
                logger.info(f"📤 Exportando video con subtítulos: {subtitled_path}")
                final_video.write_videofile(
                    str(subtitled_path),
                    fps=30,
                    codec='libx264',
                    audio_codec='aac'
                )
                
                # Limpiar recursos
                video.close()
                final_video.close()
                
                return str(subtitled_path)
            else:
                video.close()
                logger.warning("⚠️ No se generaron clips de subtítulos")
                return video_path
                
        except Exception as e:
            logger.error(f"❌ Error añadiendo subtítulos: {e}")
            return video_path
    
    def _create_moviepy_subtitles_from_timeline(self, timeline: List[Dict], video_duration: float) -> List:
        """Crea clips de subtítulos usando timeline de Whisper"""
        try:
            from moviepy.editor import TextClip
            
            subtitle_clips = []
            
            # Procesar palabras en grupos de 3 (estilo CapCut)
            for i in range(0, len(timeline), 3):
                word_group = timeline[i:i+3]
                
                if not word_group:
                    continue
                
                # Tiempo del grupo
                start_time = word_group[0]['start']
                end_time = word_group[-1]['end']
                
                # Asegurar que no exceda la duración del video
                if start_time >= video_duration:
                    break
                end_time = min(end_time, video_duration)
                
                # Texto del grupo
                group_text = ' '.join([w['word'] for w in word_group]).upper()
                
                # Crear clip de texto
                txt_clip = TextClip(
                    group_text,
                    fontsize=80,
                    color='white',
                    stroke_color='black',
                    stroke_width=4,
                    font='Arial-Bold'
                ).set_position(('center', 0.8), relative=True).set_start(start_time).set_end(end_time)
                
                subtitle_clips.append(txt_clip)
            
            logger.info(f"✅ Creados {len(subtitle_clips)} clips de subtítulos con Whisper")
            return subtitle_clips
            
        except Exception as e:
            logger.error(f"❌ Error creando subtítulos de Whisper: {e}")
            return []
    
    def _create_moviepy_subtitles_estimated(self, script: str, video_duration: float) -> List:
        """Crea clips de subtítulos usando timing estimado"""
        try:
            from moviepy.editor import TextClip
            
            words = script.split()
            subtitle_clips = []
            
            # Timing estimado
            words_per_second = len(words) / video_duration
            seconds_per_word = video_duration / len(words) if len(words) > 0 else 1.0
            
            # Procesar en grupos de 3 palabras
            for i in range(0, len(words), 3):
                word_group = words[i:i+3]
                
                # Tiempo del grupo
                start_time = i * seconds_per_word
                end_time = min((i + len(word_group)) * seconds_per_word, video_duration)
                
                if start_time >= video_duration:
                    break
                
                # Texto del grupo
                group_text = ' '.join(word_group).upper()
                
                # Crear clip de texto estilo CapCut
                txt_clip = TextClip(
                    group_text,
                    fontsize=80,
                    color='white',
                    stroke_color='black',
                    stroke_width=4,
                    font='Arial-Bold'
                ).set_position(('center', 0.8), relative=True).set_start(start_time).set_end(end_time)
                
                subtitle_clips.append(txt_clip)
            
            logger.info(f"✅ Creados {len(subtitle_clips)} clips de subtítulos estimados")
            return subtitle_clips
            
        except Exception as e:
            logger.error(f"❌ Error creando subtítulos estimados: {e}")
            return []

    def create_thumbnail(self, title: str, images: List[str] = None) -> str:
        """Crea un thumbnail optimizado para Shorts."""
        
        if not PIL_AVAILABLE:
            logger.warning("PIL no disponible. No se puede crear thumbnail.")
            return ""
        
        try:
            # Crear thumbnail vertical para Shorts (mismo aspect ratio que el video)
            img = Image.new('RGB', (1080, 1920), color=(255, 20, 147))  # Rosa vibrante
            
            # Añadir gradient overlay
            overlay = Image.new('RGBA', (1080, 1920), (0, 0, 0, 120))
            img = img.convert('RGBA')
            img = Image.alpha_composite(img, overlay)
            
            # Añadir texto del título
            draw = ImageDraw.Draw(img)
            
            try:
                font_large = ImageFont.truetype("arial.ttf", 100)
                font_small = ImageFont.truetype("arial.ttf", 60)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Procesar título para Shorts
            title_parts = title.upper().split()
            if len(title_parts) > 4:
                line1 = " ".join(title_parts[:2])
                line2 = " ".join(title_parts[2:4])
                line3 = " ".join(title_parts[4:6]) if len(title_parts) > 4 else ""
            else:
                line1 = " ".join(title_parts[:2])
                line2 = " ".join(title_parts[2:])
                line3 = ""
            
            # Dibujar texto centrado
            y_start = 600  # Centrado verticalmente
            
            for i, line in enumerate([line1, line2, line3]):
                if line:
                    bbox = draw.textbbox((0, 0), line, font=font_large)
                    text_width = bbox[2] - bbox[0]
                    x = (1080 - text_width) // 2
                    y = y_start + (i * 120)
                    
                    # Sombra
                    draw.text((x+3, y+3), line, fill=(0, 0, 0), font=font_large)
                    # Texto principal
                    draw.text((x, y), line, fill=(255, 255, 255), font=font_large)
            
            # Añadir badge "SHORTS"
            badge_text = "#SHORTS"
            bbox = draw.textbbox((0, 0), badge_text, font=font_small)
            badge_width = bbox[2] - bbox[0]
            badge_x = (1080 - badge_width) // 2
            badge_y = 1700
            
            draw.text((badge_x+2, badge_y+2), badge_text, fill=(0, 0, 0), font=font_small)
            draw.text((badge_x, badge_y), badge_text, fill=(255, 215, 0), font=font_small)
            
            # Guardar thumbnail
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:20]
            thumbnail_path = self.output_dir / f"thumbnail_{safe_title.replace(' ', '_')}.jpg"
            img.convert('RGB').save(thumbnail_path, 'JPEG', quality=95)
            
            logger.info(f"Thumbnail creado: {thumbnail_path}")
            return str(thumbnail_path)
            
        except Exception as e:
            logger.error(f"Error creando thumbnail: {e}")
            return ""
    
    def cleanup_temp_files(self):
        """Limpia archivos temporales."""
        try:
            for file_path in self.temp_dir.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
            logger.info("Archivos temporales limpiados")
        except Exception as e:
            logger.error(f"Error limpiando archivos temporales: {e}")

# Función de utilidad para crear videos rápidamente
async def quick_create_short(title: str, script: str, duration: int = 45) -> str:
    """
    Crea un Short rápidamente con configuración optimizada.
    
    Args:
        title: Título del Short
        script: Guión completo
        duration: Duración objetivo en segundos (máximo 60 para Shorts)
    
    Returns:
        str: Path del archivo de estructura generado
    """
    creator = VideoCreator()
    
    # Limitar duración a máximo de Shorts
    duration = min(duration, 60)
    
    config = VideoConfig(
        title=title,
        script=script,
        duration=duration,
        is_short=True
    )
    
    try:
        result = await creator.create_video(config)
        
        # Crear thumbnail también
        thumbnail = creator.create_thumbnail(title)
        if thumbnail:
            logger.info(f"Thumbnail generado: {thumbnail}")
        
        return result
    finally:
        creator.cleanup_temp_files()

# Ejemplo de uso
if __name__ == "__main__":
    import asyncio
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Ejemplo de creación de Short
    async def test_short_creation():
        title = "TOP 5 Datos Locos del Océano"
        script = """
        ¿Sabías que el océano esconde secretos increíbles?
        
        5. El océano produce el 70% del oxígeno que respiramos
        4. Hay más de 200,000 especies marinas sin descubrir
        3. La presión en la fosa más profunda aplastaría un humano instantáneamente
        2. Los océanos contienen 99% del espacio habitable del planeta
        1. Conocemos menos del 5% de nuestros océanos
        
        ¡Sígueme para más datos que te van a volar la mente!
        """
        
        try:
            result = await quick_create_short(title, script, 50)
            print(f"Short preparado: {result}")
            print("Para generar el video final, instala: pip install moviepy")
        except Exception as e:
            print(f"Error: {e}")
    
    # Ejecutar ejemplo
    # asyncio.run(test_short_creation())