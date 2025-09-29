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
        
        logger.info(f"VideoCreator inicializado - Voz: {self.tts_voice}")
    
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
            audio_file = await self._generate_tts_audio(config.script, config.title)
            
            # 2. Buscar y preparar imágenes (simplificado)
            images = await self._prepare_images(config.title)
            
            # 3. Crear estructura básica del video
            video_info = self._create_video_structure(config, audio_file, images)
            
            logger.info(f"Estructura de video creada: {video_info['output_file']}")
            return video_info['output_file']
            
        except Exception as e:
            logger.error(f"Error creando video: {e}")
            raise
    
    async def _generate_tts_audio(self, script: str, title: str) -> str:
        """Genera audio usando Edge TTS (gratuito)."""
        
        # Limpiar script para TTS
        clean_script = self._clean_script_for_tts(script)
        
        # Usar voz configurada dinámicamente
        voice = self.tts_voice
        
        # Nombre de archivo seguro
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()[:20]
        output_file = self.temp_dir / f"audio_{safe_title.replace(' ', '_')}.mp3"
        
        try:
            # Generar audio con Edge TTS
            communicate = edge_tts.Communicate(clean_script, voice)
            await communicate.save(str(output_file))
            
            logger.info(f"Audio TTS generado: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error generando TTS: {e}")
            raise
    
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
        """Prepara imágenes para Shorts (menos imágenes, más impacto)."""
        
        # Para Shorts solo necesitamos pocas imágenes de alta calidad
        try:
            # Intentar buscar imágenes reales si hay API
            images = await self._fetch_images_simple(topic, count)
            
            if not images:
                # Crear imágenes placeholder si no hay API
                images = self._create_placeholder_images(count)
            
            logger.info(f"Preparadas {len(images)} imágenes para Short")
            return images
            
        except Exception as e:
            logger.error(f"Error preparando imágenes: {e}")
            return self._create_placeholder_images(count)
    
    async def _fetch_images_simple(self, topic: str, count: int = 3) -> List[str]:
        """Busca imágenes de forma simplificada."""
        
        # Por ahora retornamos lista vacía, se implementará con APIs
        # cuando se configure Unsplash o Pexels
        return []
    
    def _create_placeholder_images(self, count: int = 3) -> List[str]:
        """Crea imágenes placeholder para Shorts."""
        
        if not PIL_AVAILABLE:
            logger.warning("PIL no disponible. No se pueden crear placeholders.")
            return []
        
        placeholder_images = []
        
        # Colores vibrantes para Shorts
        colors = [
            (255, 20, 147),   # Rosa vibrante
            (50, 205, 50),    # Verde lima
            (255, 140, 0),    # Naranja
            (138, 43, 226),   # Púrpura
            (0, 191, 255),    # Azul cielo
        ]
        
        for i in range(count):
            try:
                # Crear imagen vertical para Shorts
                img = Image.new('RGB', (1080, 1920), color=colors[i % len(colors)])
                draw = ImageDraw.Draw(img)
                
                try:
                    # Usar fuente más grande para Shorts
                    font = ImageFont.truetype("arial.ttf", 200)
                except:
                    font = ImageFont.load_default()
                
                text = f"#{i+1}"
                
                # Calcular posición centrada
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (1080 - text_width) // 2
                y = (1920 - text_height) // 2
                
                # Añadir sombra para mejor legibilidad
                shadow_offset = 5
                draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0, 128), font=font)
                draw.text((x, y), text, fill=(255, 255, 255), font=font)
                
                # Guardar imagen
                img_path = self.temp_dir / f"placeholder_{i+1}.jpg"
                img.save(img_path, quality=95)
                placeholder_images.append(str(img_path))
                
            except Exception as e:
                logger.error(f"Error creando placeholder {i}: {e}")
        
        return placeholder_images
    
    def _create_video_structure(self, config: VideoConfig, audio_file: str, images: List[str]) -> Dict:
        """
        Crea la estructura del video sin MoviePy (preparación para futuro).
        Por ahora genera la información necesaria para el montaje.
        """
        
        try:
            # Información del video estructurada
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
                    "image_duration": config.duration / max(len(images), 1) if images else config.duration,
                    "transition_time": 0.5
                },
                "output_file": str(self.output_dir / f"short_{config.title[:20].replace(' ', '_')}.json"),
                "status": "structured"
            }
            
            # Guardar estructura en JSON para futuro procesamiento
            import json
            with open(video_structure["output_file"], 'w', encoding='utf-8') as f:
                json.dump(video_structure, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Estructura de video guardada: {video_structure['output_file']}")
            
            # Crear archivo de instrucciones para el video
            instructions_file = str(self.output_dir / f"instructions_{config.title[:20].replace(' ', '_')}.txt")
            
            with open(instructions_file, 'w', encoding='utf-8') as f:
                f.write(f"INSTRUCCIONES PARA VIDEO SHORT\n")
                f.write(f"=" * 40 + "\n\n")
                f.write(f"Título: {config.title}\n")
                f.write(f"Duración: {config.duration} segundos\n")
                f.write(f"Resolución: {config.resolution[0]}x{config.resolution[1]} (Vertical)\n")
                f.write(f"Formato: YouTube Short\n\n")
                f.write(f"ASSETS:\n")
                f.write(f"- Audio: {audio_file}\n")
                f.write(f"- Imágenes: {len(images)} archivos\n")
                for i, img in enumerate(images, 1):
                    f.write(f"  {i}. {img}\n")
                f.write(f"\nTIMING:\n")
                f.write(f"- Duración por imagen: {video_structure['timing']['image_duration']:.1f}s\n")
                f.write(f"- Transiciones: {video_structure['timing']['transition_time']}s\n")
                f.write(f"\nNOTA: Para generar el video final, instala MoviePy:\n")
                f.write(f"pip install moviepy\n")
            
            video_structure["instructions_file"] = instructions_file
            
            return video_structure
            
        except Exception as e:
            logger.error(f"Error creando estructura de video: {e}")
            raise
    
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