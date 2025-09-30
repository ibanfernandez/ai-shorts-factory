"""
🎬 GENERADOR DE SUBTÍTULOS DINÁMICOS PARA SHORTS VIRALES
Sistema avanzado de subtítulos sincronizados con efectos visuales
"""

import re
import json
import logging
from typing import List, Dict, Tuple, Any
import numpy as np

# MoviePy imports con manejo de errores
try:
    from moviepy.editor import TextClip, VideoClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    # Clases mock para desarrollo
    class TextClip:
        pass
    class VideoClip:
        pass

logger = logging.getLogger(__name__)

class SubtitleGenerator:
    """
    Genera subtítulos dinámicos sincronizados con audio para shorts virales
    """
    
    def __init__(self):
        self.subtitle_style = {
            'font_size': 80,
            'font_color': 'white',
            'font_stroke_color': 'black',
            'font_stroke_width': 4,
            'font_family': 'Arial-Bold',
            'position': ('center', 'center'),
            'duration_per_word': 0.5,  # segundos por palabra
            'fade_duration': 0.1
        }
        
        # Colores dinámicos para palabras clave
        self.highlight_colors = [
            '#FF6B6B',  # Rojo coral
            '#4ECDC4',  # Turquesa
            '#45B7D1',  # Azul
            '#96CEB4',  # Verde menta
            '#FFEAA7',  # Amarillo suave
            '#DDA0DD',  # Púrpura claro
            '#FFB347',  # Naranja
        ]
        
        # Palabras que deben destacarse
        self.highlight_words = [
            'top', 'secretos', 'increíble', 'impactante', 'sorprendente',
            'nunca', 'jamás', 'siempre', 'todos', 'nadie', 'mundo',
            'universo', 'tierra', 'océano', 'espacio', 'misterio',
            'peligroso', 'mortal', 'extremo', 'único', 'especial'
        ]
    
    def extract_words_with_timing(self, text: str, audio_duration: float) -> List[Dict]:
        """
        Extrae palabras del texto y calcula timing para sincronización
        """
        # Limpiar texto y dividir en palabras
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        
        if total_words == 0:
            return []
        
        # Calcular duración por palabra basada en audio
        word_duration = audio_duration / total_words
        
        word_timings = []
        current_time = 0
        
        for i, word in enumerate(words):
            # Ajustar duración para palabras importantes
            duration = word_duration
            if word in self.highlight_words:
                duration *= 1.2  # Palabras clave duran más
            
            word_data = {
                'word': word,
                'start': current_time,
                'end': current_time + duration,
                'duration': duration,
                'is_highlight': word in self.highlight_words,
                'index': i
            }
            
            word_timings.append(word_data)
            current_time += duration
        
        logger.info(f"✅ Extraídas {total_words} palabras con timing sincronizado")
        return word_timings
    
    def create_subtitle_clip(self, word_data: Dict, video_size: Tuple[int, int]) -> TextClip:
        """
        Crea un clip de subtítulo individual para una palabra
        """
        word = word_data['word'].upper()
        
        # Seleccionar color
        if word_data['is_highlight']:
            color = np.random.choice(self.highlight_colors)
            font_size = int(self.subtitle_style['font_size'] * 1.2)
        else:
            color = self.subtitle_style['font_color']
            font_size = self.subtitle_style['font_size']
        
        try:
            # Crear clip de texto
            text_clip = TextClip(
                word,
                fontsize=font_size,
                color=color,
                stroke_color=self.subtitle_style['font_stroke_color'],
                stroke_width=self.subtitle_style['font_stroke_width'],
                font='Arial-Bold',
                method='caption'
            )
            
            # Posicionar en centro de pantalla
            text_clip = text_clip.set_position('center')
            
            # Configurar timing
            text_clip = text_clip.set_start(word_data['start'])
            text_clip = text_clip.set_duration(word_data['duration'])
            
            # Añadir efectos de entrada y salida
            fade_dur = min(0.1, word_data['duration'] / 4)
            text_clip = text_clip.crossfadein(fade_dur).crossfadeout(fade_dur)
            
            # Efecto de zoom para palabras destacadas
            if word_data['is_highlight']:
                # Efecto de zoom in
                def zoom_effect(get_frame, t):
                    frame = get_frame(t)
                    progress = t / text_clip.duration
                    zoom = 1 + 0.1 * np.sin(progress * np.pi)
                    return frame
                
                text_clip = text_clip.fl(zoom_effect)
            
            return text_clip
            
        except Exception as e:
            logger.error(f"❌ Error creando subtitle para '{word}': {e}")
            # Fallback simple
            return TextClip(
                word,
                fontsize=60,
                color='white',
                stroke_color='black',
                stroke_width=2
            ).set_position('center').set_start(word_data['start']).set_duration(word_data['duration'])
    
    def create_grouped_subtitles(self, text: str, audio_duration: float, video_size: Tuple[int, int]) -> List[VideoClip]:
        """
        Crea subtítulos agrupando 2-3 palabras para mejor legibilidad
        """
        words = re.findall(r'\S+', text)  # Incluye puntuación
        total_words = len(words)
        
        if total_words == 0:
            return []
        
        # Agrupar palabras en chunks de 2-3
        word_groups = []
        group_size = 2 if total_words > 20 else 3
        
        for i in range(0, total_words, group_size):
            group = words[i:i+group_size]
            word_groups.append(' '.join(group))
        
        # Calcular timing por grupo
        group_duration = audio_duration / len(word_groups)
        
        subtitle_clips = []
        current_time = 0
        
        for i, group_text in enumerate(word_groups):
            # Determinar si el grupo contiene palabras importantes
            has_highlight = any(word.lower() in self.highlight_words for word in group_text.split())
            
            # Seleccionar estilo
            if has_highlight:
                color = np.random.choice(self.highlight_colors)
                font_size = 85
            else:
                color = 'white'
                font_size = 75
            
            try:
                # Crear clip de texto
                text_clip = TextClip(
                    group_text.upper(),
                    fontsize=font_size,
                    color=color,
                    stroke_color='black',
                    stroke_width=3,
                    font='Arial-Bold',
                    method='caption'
                ).set_position('center').set_start(current_time).set_duration(group_duration)
                
                # Efectos de animación
                fade_dur = min(0.15, group_duration / 3)
                text_clip = text_clip.crossfadein(fade_dur).crossfadeout(fade_dur)
                
                # Efecto de aparición desde abajo para grupos destacados
                if has_highlight:
                    def slide_up_effect(get_frame, t):
                        frame = get_frame(t)
                        progress = min(t / 0.3, 1.0)  # Animación de 0.3s
                        return frame
                    
                    # Posición inicial desde abajo
                    text_clip = text_clip.set_position(lambda t: ('center', 'center') if t > 0.3 else ('center', video_size[1] + 50))
                
                subtitle_clips.append(text_clip)
                current_time += group_duration
                
            except Exception as e:
                logger.error(f"❌ Error creando subtitle grupal: {e}")
                continue
        
        logger.info(f"✅ Creados {len(subtitle_clips)} grupos de subtítulos dinámicos")
        return subtitle_clips
    
    def generate_dynamic_subtitles(self, text: str, audio_duration: float, video_size: Tuple[int, int] = (1080, 1920)) -> List[VideoClip]:
        """
        Genera subtítulos dinámicos completos para el video
        """
        logger.info(f"🎬 Generando subtítulos dinámicos para texto de {len(text)} caracteres")
        
        try:
            # Usar sistema de grupos para mejor legibilidad
            subtitle_clips = self.create_grouped_subtitles(text, audio_duration, video_size)
            
            if not subtitle_clips:
                logger.warning("⚠️ No se pudieron crear subtítulos")
                return []
            
            logger.info(f"✅ Generados {len(subtitle_clips)} subtítulos dinámicos exitosamente")
            return subtitle_clips
            
        except Exception as e:
            logger.error(f"❌ Error generando subtítulos dinámicos: {e}")
            return []
    
    def add_subtitle_effects(self, subtitle_clips: List[VideoClip]) -> List[VideoClip]:
        """
        Añade efectos adicionales a los subtítulos
        """
        enhanced_clips = []
        
        for clip in subtitle_clips:
            try:
                # Efecto de sombra/glow
                shadow_clip = clip.copy()
                
                # Añadir el clip original encima de la sombra
                enhanced_clips.append(clip)
                
            except Exception as e:
                logger.error(f"❌ Error añadiendo efectos: {e}")
                enhanced_clips.append(clip)
        
        return enhanced_clips