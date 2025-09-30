"""
🎭 PLANTILLAS DE VIDEO DINÁMICAS PARA SHORTS VIRALES
Sistema de fondos de video profesionales que se repiten en loop
"""

import os
import logging
from typing import List, Tuple, Optional, Any
import numpy as np

# MoviePy imports con manejo de errores
try:
    from moviepy.editor import VideoFileClip, ColorClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    # Clases mock para desarrollo
    class VideoFileClip:
        pass
    class ColorClip:
        pass
    def concatenate_videoclips(clips):
        pass

logger = logging.getLogger(__name__)

class VideoTemplateGenerator:
    """
    Genera plantillas de video de fondo dinámicas para shorts
    """
    
    def __init__(self, templates_dir: str = "assets/video_templates"):
        self.templates_dir = templates_dir
        self.video_size = (1080, 1920)  # 9:16 para shorts
        
        # Crear directorio si no existe
        os.makedirs(templates_dir, exist_ok=True)
        
        # Plantillas disponibles (se crearán programáticamente)
        self.template_configs = {
            'cosmic_particles': {
                'name': 'Partículas Cósmicas',
                'description': 'Fondo con partículas flotantes en el espacio',
                'colors': ['#1a1a2e', '#16213e', '#0f3460'],
                'type': 'particles'
            },
            'gradient_waves': {
                'name': 'Ondas Gradiente',
                'description': 'Ondas de color que se mueven suavemente',
                'colors': ['#667eea', '#764ba2', '#f093fb'],
                'type': 'waves'
            },
            'tech_grid': {
                'name': 'Grid Tecnológico',
                'description': 'Grid digital con efectos de matriz',
                'colors': ['#0a0a0a', '#1a1a1a', '#00ff41'],
                'type': 'tech'
            },
            'nature_flow': {
                'name': 'Flujo Natural',
                'description': 'Patrones orgánicos y fluidos',
                'colors': ['#134e5e', '#71b280', '#a8e6cf'],
                'type': 'organic'
            },
            'energy_burst': {
                'name': 'Explosión de Energía',
                'description': 'Rayos de energía y brillos',
                'colors': ['#ff6b6b', '#ee5a6f', '#60a3bc'],
                'type': 'energy'
            }
        }
    
    def create_particle_template(self, duration: float, colors: List[str]) -> VideoFileClip:
        """
        Crea plantilla con partículas flotantes
        """
        logger.info("🌌 Creando plantilla de partículas cósmicas")
        
        try:
            # Crear clip base con gradiente
            def make_frame(t):
                # Gradiente vertical
                frame = np.zeros((self.video_size[1], self.video_size[0], 3), dtype=np.uint8)
                
                # Color base gradiente
                for y in range(self.video_size[1]):
                    progress = y / self.video_size[1]
                    # Interpolación entre colores
                    r = int(26 + (22 - 26) * progress)  # #1a1a2e a #16213e
                    g = int(26 + (33 - 26) * progress)
                    b = int(46 + (62 - 46) * progress)
                    frame[y, :] = [r, g, b]
                
                # Añadir partículas animadas
                num_particles = 50
                for i in range(num_particles):
                    # Posición de partícula basada en tiempo
                    x = int((np.sin(t * 0.5 + i * 0.1) * 0.3 + 0.5) * self.video_size[0])
                    y = int(((t * 20 + i * 50) % (self.video_size[1] + 100)) - 50)
                    
                    if 0 <= x < self.video_size[0] and 0 <= y < self.video_size[1]:
                        # Brillo de partícula
                        brightness = int(100 + 50 * np.sin(t * 2 + i))
                        frame[y:y+3, x:x+3] = [brightness, brightness, brightness + 50]
                
                return frame
            
            # Crear clip de video
            clip = VideoFileClip.__new__(VideoFileClip)
            clip.make_frame = make_frame
            clip.duration = duration
            clip.fps = 30
            clip.size = self.video_size
            
            return clip
            
        except Exception as e:
            logger.error(f"❌ Error creando plantilla de partículas: {e}")
            return self.create_fallback_template(duration)
    
    def create_gradient_template(self, duration: float, colors: List[str]) -> VideoFileClip:
        """
        Crea plantilla con gradientes animados
        """
        logger.info("🌊 Creando plantilla de gradientes ondulantes")
        
        try:
            def make_frame(t):
                frame = np.zeros((self.video_size[1], self.video_size[0], 3), dtype=np.uint8)
                
                # Gradiente ondulante
                for y in range(self.video_size[1]):
                    for x in range(self.video_size[0]):
                        # Crear ondas
                        wave1 = np.sin(x * 0.01 + t * 2) * 0.5 + 0.5
                        wave2 = np.sin(y * 0.01 + t * 1.5) * 0.5 + 0.5
                        combined = (wave1 + wave2) / 2
                        
                        # Interpolación de colores
                        if combined < 0.33:
                            # Azul a púrpura
                            r = int(102 + (118 - 102) * (combined * 3))
                            g = int(126 + (75 - 126) * (combined * 3))
                            b = int(234 + (162 - 234) * (combined * 3))
                        elif combined < 0.66:
                            # Púrpura a rosa
                            progress = (combined - 0.33) * 3
                            r = int(118 + (240 - 118) * progress)
                            g = int(75 + (147 - 75) * progress)
                            b = int(162 + (251 - 162) * progress)
                        else:
                            # Rosa brillante
                            r, g, b = 240, 147, 251
                        
                        frame[y, x] = [r, g, b]
                
                return frame
            
            clip = VideoFileClip.__new__(VideoFileClip)
            clip.make_frame = make_frame
            clip.duration = duration
            clip.fps = 24
            clip.size = self.video_size
            
            return clip
            
        except Exception as e:
            logger.error(f"❌ Error creando plantilla de gradientes: {e}")
            return self.create_fallback_template(duration)
    
    def create_tech_template(self, duration: float, colors: List[str]) -> VideoFileClip:
        """
        Crea plantilla tecnológica con grid
        """
        logger.info("⚡ Creando plantilla tecnológica")
        
        try:
            def make_frame(t):
                frame = np.zeros((self.video_size[1], self.video_size[0], 3), dtype=np.uint8)
                
                # Fondo oscuro
                frame.fill(10)
                
                # Grid vertical
                grid_spacing = 80
                for x in range(0, self.video_size[0], grid_spacing):
                    alpha = 0.3 + 0.2 * np.sin(t * 2 + x * 0.01)
                    color_val = int(255 * alpha * 0.3)
                    if x < self.video_size[0]:
                        frame[:, x:x+2] = [0, color_val, int(color_val * 1.5)]
                
                # Grid horizontal
                for y in range(0, self.video_size[1], grid_spacing):
                    alpha = 0.3 + 0.2 * np.sin(t * 1.5 + y * 0.01)
                    color_val = int(255 * alpha * 0.3)
                    if y < self.video_size[1]:
                        frame[y:y+2, :] = [0, color_val, int(color_val * 1.5)]
                
                # Pulsos de energía
                pulse_y = int((t * 100) % self.video_size[1])
                if pulse_y < self.video_size[1] - 20:
                    brightness = int(200 * np.exp(-((pulse_y % 200) / 50) ** 2))
                    frame[pulse_y:pulse_y+20, :] = [0, brightness, brightness]
                
                return frame
            
            clip = VideoFileClip.__new__(VideoFileClip)
            clip.make_frame = make_frame
            clip.duration = duration
            clip.fps = 30
            clip.size = self.video_size
            
            return clip
            
        except Exception as e:
            logger.error(f"❌ Error creando plantilla tech: {e}")
            return self.create_fallback_template(duration)
    
    def create_fallback_template(self, duration: float) -> VideoFileClip:
        """
        Crea plantilla de respaldo simple
        """
        logger.info("🎨 Creando plantilla de respaldo")
        
        try:
            # Gradiente simple negro a azul oscuro
            def make_frame(t):
                frame = np.zeros((self.video_size[1], self.video_size[0], 3), dtype=np.uint8)
                
                for y in range(self.video_size[1]):
                    progress = y / self.video_size[1]
                    blue_val = int(50 * progress)
                    frame[y, :] = [10, 15, blue_val]
                
                return frame
            
            clip = VideoFileClip.__new__(VideoFileClip)
            clip.make_frame = make_frame
            clip.duration = duration
            clip.fps = 24
            clip.size = self.video_size
            
            return clip
            
        except Exception as e:
            logger.error(f"❌ Error creando plantilla fallback: {e}")
            # Como último recurso, usar ColorClip
            return ColorClip(size=self.video_size, color=[20, 30, 60]).set_duration(duration)
    
    def get_template_for_topic(self, topic: str, duration: float) -> VideoFileClip:
        """
        Selecciona plantilla apropiada según el tema
        """
        topic_lower = topic.lower()
        
        # Mapear temas a plantillas
        if any(word in topic_lower for word in ['espacio', 'universo', 'planeta', 'estrella', 'cósmico']):
            template_key = 'cosmic_particles'
        elif any(word in topic_lower for word in ['tecnología', 'tech', 'digital', 'futuro']):
            template_key = 'tech_grid'
        elif any(word in topic_lower for word in ['océano', 'agua', 'mar', 'naturaleza']):
            template_key = 'nature_flow'
        elif any(word in topic_lower for word in ['energía', 'poder', 'fuerza', 'explosión']):
            template_key = 'energy_burst'
        else:
            template_key = 'gradient_waves'  # Por defecto
        
        config = self.template_configs[template_key]
        
        logger.info(f"🎭 Seleccionada plantilla '{config['name']}' para tema: {topic}")
        
        # Crear plantilla según tipo
        if config['type'] == 'particles':
            return self.create_particle_template(duration, config['colors'])
        elif config['type'] == 'tech':
            return self.create_tech_template(duration, config['colors'])
        elif config['type'] == 'waves':
            return self.create_gradient_template(duration, config['colors'])
        else:
            return self.create_gradient_template(duration, config['colors'])
    
    def create_looped_background(self, topic: str, target_duration: float) -> VideoFileClip:
        """
        Crea fondo de video en loop para la duración completa
        """
        logger.info(f"🔄 Creando fondo en loop para {target_duration:.1f}s")
        
        # Crear segmento base de 10 segundos
        base_duration = min(10.0, target_duration)
        base_clip = self.get_template_for_topic(topic, base_duration)
        
        if target_duration <= base_duration:
            return base_clip.set_duration(target_duration)
        
        # Hacer loop para cubrir duración completa
        loops_needed = int(np.ceil(target_duration / base_duration))
        
        try:
            # Crear clips repetidos
            clips = [base_clip.copy() for _ in range(loops_needed)]
            looped_clip = concatenate_videoclips(clips)
            
            # Ajustar a duración exacta
            final_clip = looped_clip.set_duration(target_duration)
            
            logger.info(f"✅ Fondo en loop creado: {loops_needed} repeticiones")
            return final_clip
            
        except Exception as e:
            logger.error(f"❌ Error creando loop: {e}")
            return base_clip.set_duration(target_duration)