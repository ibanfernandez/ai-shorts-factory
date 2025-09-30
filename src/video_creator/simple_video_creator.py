"""
🎬 SISTEMA DE VIDEO AVANZADO CON WHISPER TIMESTAMPS
Crea videos con plantillas y subtítulos usando timestamps precisos de Whisper
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

try:
    from .whisper_timestamps import PreciseSubtitleGenerator
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logging.warning("⚠️ Whisper no disponible, usando sistema de fallback")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import numpy as np

logger = logging.getLogger(__name__)

class SimpleVideoCreator:
    """
    Creador de videos simplificado que no depende de MoviePy
    Genera frames individuales que se pueden convertir a video
    """
    
    def __init__(self):
        self.video_size = (1080, 1920)  # 9:16 para shorts
        self.fps = 30
        
        # Sistema de timestamps precisos con Whisper
        self.whisper_generator = None
        if WHISPER_AVAILABLE:
            try:
                self.whisper_generator = PreciseSubtitleGenerator()
                logger.info("✅ Sistema Whisper inicializado para timestamps precisos")
            except Exception as e:
                logger.warning(f"⚠️ Error inicializando Whisper: {e}")
                self.whisper_generator = None
        
        # Colores para diferentes tipos de contenido
        self.color_schemes = {
            'tech': [(10, 10, 10), (26, 35, 60), (0, 255, 65)],
            'space': [(26, 26, 46), (22, 33, 62), (15, 52, 96)],
            'ocean': [(19, 78, 94), (113, 178, 128), (168, 230, 207)],
            'energy': [(255, 107, 107), (238, 90, 111), (96, 163, 188)],
            'default': [(67, 126, 234), (118, 75, 162), (240, 147, 251)]
        }
    
    def create_gradient_frame(self, scheme_name: str, frame_number: int, total_frames: int) -> Image.Image:
        """
        Crea un frame con gradiente animado
        """
        colors = self.color_schemes.get(scheme_name, self.color_schemes['default'])
        
        # Crear imagen base
        img = Image.new('RGB', self.video_size)
        draw = ImageDraw.Draw(img)
        
        # Progreso de animación
        progress = (frame_number / total_frames) % 1.0
        
        # Crear gradiente vertical animado
        for y in range(self.video_size[1]):
            y_progress = y / self.video_size[1]
            
            # Animación con ondas
            wave_offset = np.sin(progress * 4 * np.pi + y_progress * 2 * np.pi) * 0.2
            adjusted_progress = max(0, min(1, y_progress + wave_offset))
            
            # Interpolación entre colores
            if adjusted_progress < 0.5:
                # Color 1 a Color 2
                blend = adjusted_progress * 2
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * blend)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * blend)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * blend)
            else:
                # Color 2 a Color 3
                blend = (adjusted_progress - 0.5) * 2
                r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * blend)
                g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * blend)
                b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * blend)
            
            # Dibujar línea horizontal
            draw.line([(0, y), (self.video_size[0], y)], fill=(r, g, b))
        
        # Añadir partículas/efectos
        self._add_particles(draw, frame_number, total_frames)
        
        return img
    
    def _add_particles(self, draw: ImageDraw.Draw, frame_number: int, total_frames: int):
        """
        Añade partículas animadas al frame
        """
        progress = (frame_number / total_frames) % 1.0
        
        # Partículas flotantes
        for i in range(30):
            # Posición basada en progreso y seed
            x = int((np.sin(progress * 2 * np.pi + i * 0.3) * 0.4 + 0.5) * self.video_size[0])
            y = int(((progress * 100 + i * 80) % (self.video_size[1] + 100)) - 50)
            
            if 0 <= x < self.video_size[0] and 0 <= y < self.video_size[1]:
                # Tamaño y brillo variable (mínimo 1)
                size = max(1, 2 + int(3 * np.sin(progress * 4 * np.pi + i)))
                brightness = max(50, min(255, int(150 + 105 * np.sin(progress * 3 * np.pi + i * 0.5))))
                
                # Coordenadas válidas
                x0, y0 = max(0, x-size), max(0, y-size)
                x1, y1 = min(self.video_size[0]-1, x+size), min(self.video_size[1]-1, y+size)
                
                # Dibujar partícula solo si las coordenadas son válidas
                if x1 > x0 and y1 > y0:
                    draw.ellipse([x0, y0, x1, y1], 
                               fill=(brightness, brightness, min(255, brightness + 50)))
    
    def create_subtitle_frame(self, text: str, base_frame: Image.Image, 
                            highlight_word: str = None, all_words: List[str] = None, word_index: int = 0) -> Image.Image:
        """
        Añade subtítulos estilo CapCut con highlighting amarillo de palabra actual.
        INTELIGENTE: Ajusta automáticamente para evitar overflow.
        """
        frame = base_frame.copy()
        draw = ImageDraw.Draw(frame)
        
        if not text.strip():
            return frame
        
        # Preparar palabras del contexto completo
        words = text.upper().split()
        if not words:
            return frame
        
        # Configurar área de trabajo (con márgenes seguros)
        margin = 80  # Margen mínimo por lado
        max_width = self.video_size[0] - (margin * 2)  # Ancho máximo disponible
        y_position = int(self.video_size[1] * 0.78)  # 78% hacia abajo
        
        # Sistema inteligente de ajuste de fuente y modo
        font, display_mode, display_words = self._determine_optimal_display(words, highlight_word, max_width, draw)
        
        # Determinar si usar amarillo o blanco (alternancia basada en índice)
        use_yellow = (word_index % 2 == 1) if word_index >= 0 else True
        
        # Siempre renderizar una sola palabra perfectamente centrada
        return self._render_optimized_single_word(frame, display_words[0], highlight_word, font, y_position, use_yellow)
    
    def _determine_optimal_display(self, words: List[str], highlight_word: str, max_width: int, draw) -> tuple:
        """
        SISTEMA SIMPLIFICADO: Mostrar SIEMPRE solo UNA palabra centrada.
        Esto elimina todos los problemas de overflow y posicionamiento.
        
        Returns:
            tuple: (font, display_mode, display_words)
        """
        # Usar solo la palabra destacada
        target_word = highlight_word if highlight_word and highlight_word in words else words[0]
        
        # Encontrar el mejor tamaño de fuente para esta palabra
        font = self._find_optimal_font_for_text(target_word, max_width, draw)
        
        logger.debug(f"🎯 Mostrando palabra única: '{target_word}'")
        return font, "single_word", [target_word]
    
    def _select_display_words(self, words: List[str], highlight_word: str) -> tuple:
        """
        Selecciona las palabras a mostrar priorizando la destacada.
        
        Returns:
            tuple: (palabra_principal, palabra_contexto)
        """
        if not words:
            return "", None
        
        # Buscar la palabra destacada en la lista
        highlight_index = -1
        if highlight_word:
            for i, word in enumerate(words):
                if word.upper() == highlight_word.upper():
                    highlight_index = i
                    break
        
        # Si encontramos la palabra destacada, usarla como principal
        if highlight_index >= 0:
            target_word = words[highlight_index]
            
            # Buscar palabra de contexto adyacente
            context_word = None
            
            # Prioridad 1: Palabra anterior (si existe)
            if highlight_index > 0:
                context_word = words[highlight_index - 1]
            # Prioridad 2: Palabra siguiente (si no hay anterior)
            elif highlight_index < len(words) - 1:
                context_word = words[highlight_index + 1]
            
            return target_word, context_word
        
        # Si no hay palabra destacada, usar la palabra central
        center_index = len(words) // 2
        target_word = words[center_index]
        
        # Buscar contexto para palabra central
        context_word = None
        if center_index > 0:
            context_word = words[center_index - 1]
        elif center_index < len(words) - 1:
            context_word = words[center_index + 1]
        
        return target_word, context_word
    
    def _find_optimal_font_for_text(self, text: str, max_width: int, draw) -> object:
        """
        Encuentra el tamaño de fuente óptimo para el texto dado.
        
        Args:
            text: Texto a renderizar
            max_width: Ancho máximo disponible
            draw: Objeto ImageDraw
            
        Returns:
            Font object
        """
        # Tamaños de fuente de mayor a menor
        font_sizes = [140, 120, 100, 85, 70, 60, 50, 45]  # Empezamos más grande
        
        for font_size in font_sizes:
            font = self._load_font(font_size)
            text_width = self._get_text_width(text, font, draw)
            
            if text_width <= max_width:
                logger.debug(f"✅ Fuente óptima: {font_size}px para '{text}' (ancho: {text_width}px)")
                return font
        
        # Fallback: fuente mínima
        logger.debug(f"⚠️ Usando fuente mínima 45px para '{text}'")
        return self._load_font(45)
    

    
    def _render_optimized_single_word(self, frame: Image.Image, word: str, 
                                    highlight_word: str, font, y_position: int, use_yellow: bool = True) -> Image.Image:
        """
        Renderiza UNA sola palabra PERFECTAMENTE CENTRADA con alternancia amarillo/blanco.
        Sistema profesional con stroke y efectos visuales.
        """
        draw = ImageDraw.Draw(frame)
        
        # Calcular dimensiones del texto
        text_bbox = draw.textbbox((0, 0), word, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # CENTRADO PERFECTO: horizontal y vertical
        x_position = (frame.width - text_width) // 2
        y_position = (frame.height - text_height) // 2  # Centrar verticalmente
        
        # SISTEMA DE ALTERNANCIA: Amarillo brillante o Blanco puro
        if use_yellow:
            # Amarillo vibrante estilo CapCut
            text_color = (255, 223, 0)  # Amarillo dorado brillante
            glow_color = (255, 255, 100)  # Amarillo más claro para glow
            effect_name = "amarillo"
        else:
            # Blanco puro para contraste
            text_color = (255, 255, 255)  # Blanco puro
            glow_color = (240, 240, 240)  # Blanco suave para glow
            effect_name = "blanco"
        
        border_color = (0, 0, 0)  # Negro profundo
        
        # EFECTO GLOW SUTIL (opcional)
        glow_thickness = 1
        for dx in range(-glow_thickness, glow_thickness + 1):
            for dy in range(-glow_thickness, glow_thickness + 1):
                if dx != 0 or dy != 0:
                    draw.text((x_position + dx, y_position + dy), word, 
                             font=font, fill=glow_color)
        
        # STROKE NEGRO GRUESO para máximo contraste
        stroke_thickness = 4
        for dx in range(-stroke_thickness, stroke_thickness + 1):
            for dy in range(-stroke_thickness, stroke_thickness + 1):
                if dx != 0 or dy != 0:
                    draw.text((x_position + dx, y_position + dy), word, 
                             font=font, fill=border_color)
        
        # TEXTO PRINCIPAL con color alternante
        draw.text((x_position, y_position), word, font=font, fill=text_color)
        
        logger.debug(f"🎯 Palabra {effect_name} centrada: '{word}' en ({x_position}, {y_position})")
        return frame
    
    def _render_optimized_two_words(self, frame: Image.Image, display_words: List[str], 
                                  highlight_word: str, font, y_position: int) -> Image.Image:
        """
        Renderiza DOS palabras con espaciado óptimo.
        """
        draw = ImageDraw.Draw(frame)
        
        if len(display_words) != 2:
            # Fallback a palabra única si no hay exactamente 2
            return self._render_optimized_single_word(frame, display_words[0], highlight_word, font, y_position)
        
        word1, word2 = display_words
        
        # Calcular espacio entre palabras (20px fijo)
        word_spacing = 20
        
        # Calcular anchos individuales
        width1 = self._get_text_width(word1, font, draw)
        width2 = self._get_text_width(word2, font, draw)
        total_width = width1 + word_spacing + width2
        
        # Centrar el grupo completo
        start_x = (self.video_size[0] - total_width) // 2
        
        # Posiciones de cada palabra
        x1 = start_x
        x2 = start_x + width1 + word_spacing
        
        # Determinar cuál está destacada
        is_word1_highlighted = highlight_word and word1.upper() == highlight_word.upper()
        is_word2_highlighted = highlight_word and word2.upper() == highlight_word.upper()
        
        # Renderizar ambas palabras
        self._draw_text_with_effects(draw, word1, x1, y_position, font, is_word1_highlighted)
        self._draw_text_with_effects(draw, word2, x2, y_position, font, is_word2_highlighted)
        
        logger.debug(f"🎯 Renderizadas dos palabras: '{word1}' + '{word2}' " +
                    f"(destacada: {'1' if is_word1_highlighted else '2' if is_word2_highlighted else 'ninguna'})")
        return frame
    

    
    def _load_font(self, font_size: int):
        """
        Carga fuente con fallbacks seguros.
        """
        try:
            return ImageFont.truetype("C:/Windows/Fonts/seguibl.ttf", font_size)  # Segoe UI Bold
        except:
            try:
                return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", font_size)  # Arial Bold
            except:
                try:
                    return ImageFont.truetype("arial.ttf", font_size)
                except:
                    return ImageFont.load_default()
    
    def _get_text_width(self, text: str, font, draw) -> int:
        """
        Obtiene ancho del texto de forma segura.
        """
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            return max(0, bbox[2] - bbox[0])
        except:
            try:
                return int(draw.textlength(text, font=font))
            except:
                return len(text) * 20  # Fallback estimado
    
    def _draw_text_with_effects(self, draw, word: str, x: int, y: int, font, is_highlighted: bool = False):
        """
        Dibuja texto con todos los efectos (borde, sombra, brillo).
        """
        # Colores estilo CapCut
        if is_highlighted:
            text_color = (255, 255, 0)    # Amarillo brillante
            border_color = (0, 0, 0)      # Borde negro fuerte
            border_width = 6
        else:
            text_color = (255, 255, 255)  # Blanco
            border_color = (0, 0, 0)      # Borde negro
            border_width = 5
        
        # Dibujar borde/sombra
        try:
            for dx in range(-border_width, border_width + 1):
                for dy in range(-border_width, border_width + 1):
                    if dx != 0 or dy != 0:
                        border_x = int(x + dx)
                        border_y = int(y + dy)
                        if border_x >= 0 and border_y >= 0:
                            draw.text((border_x, border_y), word, font=font, fill=border_color)
        except Exception as e:
            logger.warning(f"Error dibujando borde: {e}")
        
        # Dibujar texto principal
        try:
            draw.text((int(x), int(y)), word, font=font, fill=text_color)
        except Exception as e:
            logger.warning(f"Error dibujando texto: {e}")
        
        # Efecto de brillo para palabras destacadas
        if is_highlighted:
            try:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx != 0 or dy != 0:
                            glow_x = int(x + dx)
                            glow_y = int(y + dy)
                            if glow_x >= 0 and glow_y >= 0:
                                draw.text((glow_x, glow_y), word, font=font, fill=(255, 255, 100))
            except Exception as e:
                logger.warning(f"Error añadiendo brillo: {e}")
    
    def select_color_scheme(self, topic: str) -> str:
        """
        Selecciona esquema de color basado en el tema
        """
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['espacio', 'universo', 'planeta', 'estrella']):
            return 'space'
        elif any(word in topic_lower for word in ['océano', 'mar', 'agua']):
            return 'ocean'
        elif any(word in topic_lower for word in ['tecnología', 'tech', 'digital']):
            return 'tech'
        elif any(word in topic_lower for word in ['energía', 'poder', 'fuerza']):
            return 'energy'
        else:
            return 'default'
    
    def generate_video_frames_with_whisper(self, config, audio_path: str, audio_duration: float) -> List[str]:
        """
        Genera frames de video usando timestamps precisos de Whisper
        """
        logger.info(f"🎬 Generando frames con Whisper para video de {audio_duration:.1f}s")
        
        # Intentar usar Whisper para timestamps precisos
        if self.whisper_generator and Path(audio_path).exists():
            try:
                logger.info("🤖 Analizando audio con Whisper...")
                precise_timeline = self.whisper_generator.generate_precise_timeline(
                    audio_path, config.script
                )
                
                if precise_timeline:
                    return self._generate_frames_from_timeline(config, precise_timeline, audio_duration)
                    
            except Exception as e:
                logger.warning(f"⚠️ Error con Whisper: {e}, usando fallback")
        
        # Fallback al sistema anterior
        logger.info("📝 Usando sistema de timing estimado (fallback)")
        return self.generate_video_frames(config, audio_duration)
    
    def _generate_frames_from_timeline(self, config, timeline: List[Dict], audio_duration: float) -> List[str]:
        """
        Genera frames usando timeline preciso de Whisper
        """
        logger.info(f"✅ Usando timeline preciso de Whisper con {len(timeline)} palabras")
        
        # Calcular número total de frames
        total_frames = int(audio_duration * self.fps)
        
        # Seleccionar esquema de color
        color_scheme = self.select_color_scheme(config.title + " " + config.script)
        
        frame_paths = []
        frames_dir = Path("output/temp/frames")
        frames_dir.mkdir(exist_ok=True)
        
        # Generar frames con timestamps precisos
        for frame_num in range(total_frames):
            # Tiempo actual del frame
            current_time = frame_num / self.fps
            
            # Crear frame base con gradiente
            base_frame = self.create_gradient_frame(color_scheme, frame_num, total_frames)
            
            # Encontrar palabra(s) activas en este momento
            active_words = []
            highlight_word = None
            
            for word_data in timeline:
                if word_data['start'] <= current_time < word_data['end']:
                    highlight_word = word_data['word']
                    break
            
            # Crear contexto de palabras (máximo 3 para estilo CapCut)
            if highlight_word:
                # Encontrar índice de palabra actual
                current_index = -1
                for i, word_data in enumerate(timeline):
                    if word_data['word'] == highlight_word and word_data['start'] <= current_time < word_data['end']:
                        current_index = i
                        break
                
                if current_index >= 0:
                    # Contexto: 1 antes, actual, 1 después (máximo 3)
                    start_idx = max(0, current_index - 1)
                    end_idx = min(len(timeline), current_index + 2)
                    
                    context_words = timeline[start_idx:end_idx]
                    current_text = ' '.join([w['word'] for w in context_words])
                else:
                    current_text = highlight_word
            else:
                # Si no hay palabra activa, mostrar contexto basado en tiempo
                current_text = self._get_context_by_time(timeline, current_time)
                highlight_word = None
            
            # Añadir subtítulos estilo CapCut con índice para alternancia
            word_idx = current_index if 'current_index' in locals() and current_index >= 0 else frame_num
            final_frame = self.create_subtitle_frame(current_text, base_frame, 
                                                   highlight_word, [w['word'] for w in timeline], word_idx)
            
            # Guardar frame
            frame_path = frames_dir / f"frame_{frame_num:06d}.jpg"
            final_frame.save(frame_path, "JPEG", quality=85)
            frame_paths.append(str(frame_path))
            
            # Log progreso cada 100 frames
            if frame_num % 100 == 0:
                progress = (frame_num / total_frames) * 100
                logger.info(f"📸 Progreso frames: {progress:.1f}%")
        
        logger.info(f"✅ Generados {len(frame_paths)} frames con timestamps precisos")
        return frame_paths
    
    def _get_context_by_time(self, timeline: List[Dict], current_time: float) -> str:
        """
        Obtiene contexto de palabras basado en el tiempo actual
        """
        # Encontrar las palabras más cercanas al tiempo actual
        closest_words = []
        
        for word_data in timeline:
            word_center = (word_data['start'] + word_data['end']) / 2
            distance = abs(current_time - word_center)
            closest_words.append((distance, word_data))
        
        # Ordenar por distancia y tomar las 3 más cercanas
        closest_words.sort(key=lambda x: x[0])
        context_words = [w[1]['word'] for w in closest_words[:3]]
        
        return ' '.join(context_words)

    def generate_video_frames(self, config, audio_duration: float) -> List[str]:
        """
        Genera todos los frames del video y los guarda como imágenes (sistema fallback)
        """
        logger.info(f"🎬 Generando frames para video de {audio_duration:.1f}s (sistema fallback)")
        
        # Calcular número total de frames
        total_frames = int(audio_duration * self.fps)
        
        # Seleccionar esquema de color
        color_scheme = self.select_color_scheme(config.title + " " + config.script)
        
        # Preparar texto para subtítulos con sincronización REAL
        script_words = config.script.split()
        total_words = len(script_words)
        
        # Crear timeline de palabras más realista
        # Edge TTS habla aproximadamente 2.5-3 palabras por segundo
        realistic_wps = 2.7  # Palabras por segundo más natural
        
        # Calcular timing más realista
        if total_words > 0:
            # Tiempo que realmente toma el audio vs tiempo disponible
            needed_time = total_words / realistic_wps
            time_factor = audio_duration / needed_time
            adjusted_wps = realistic_wps * time_factor
            seconds_per_word = 1.0 / adjusted_wps
        else:
            seconds_per_word = 0.5
        
        # Crear timeline de palabras
        word_timeline = []
        for i, word in enumerate(script_words):
            start_time = i * seconds_per_word
            end_time = (i + 1) * seconds_per_word
            word_timeline.append({
                'word': word,
                'start': start_time,
                'end': end_time,
                'index': i
            })
        
        logger.info(f"📝 Procesando {total_words} palabras en {audio_duration:.1f}s")
        logger.info(f"⏱️ {seconds_per_word:.2f} segundos por palabra (ajustado: {adjusted_wps:.2f} wps)")
        
        frame_paths = []
        frames_dir = Path("output/temp/frames")
        frames_dir.mkdir(exist_ok=True)
        
        # Generar frames con sincronización precisa
        for frame_num in range(total_frames):
            # Tiempo actual del frame
            current_time = frame_num / self.fps
            
            # Crear frame base con gradiente
            base_frame = self.create_gradient_frame(color_scheme, frame_num, total_frames)
            
            # Encontrar palabra activa en este momento
            current_word_data = None
            current_word_index = -1
            
            for word_data in word_timeline:
                if word_data['start'] <= current_time < word_data['end']:
                    current_word_data = word_data
                    current_word_index = word_data['index']
                    break
            
            # Si no hay palabra activa, usar la más cercana
            if current_word_data is None and word_timeline:
                if current_time < word_timeline[0]['start']:
                    current_word_data = word_timeline[0]
                    current_word_index = 0
                elif current_time >= word_timeline[-1]['end']:
                    current_word_data = word_timeline[-1]
                    current_word_index = len(word_timeline) - 1
            
            # Determinar contexto de palabras a mostrar (máximo 3)
            if current_word_index >= 0:
                # Mostrar palabra actual + contexto mínimo
                context_size = 1
                start_word = max(0, current_word_index - context_size)
                end_word = min(total_words, current_word_index + context_size + 1)
                
                # Asegurar máximo 3 palabras
                if end_word - start_word > 3:
                    if current_word_index - start_word >= 1:
                        start_word = current_word_index - 1
                    end_word = start_word + 3
                
                context_words = script_words[start_word:end_word]
                current_text = ' '.join(context_words)
                highlight_word = script_words[current_word_index]
            else:
                # Fallback: mostrar primeras palabras
                current_text = ' '.join(script_words[:3])
                highlight_word = script_words[0] if script_words else None
            
            # Añadir subtítulos estilo CapCut
            final_frame = self.create_subtitle_frame(current_text, base_frame, 
                                                   highlight_word, script_words)
            
            # Guardar frame
            frame_path = frames_dir / f"frame_{frame_num:06d}.jpg"
            final_frame.save(frame_path, "JPEG", quality=85)
            frame_paths.append(str(frame_path))
            
            # Log progreso cada 100 frames
            if frame_num % 100 == 0:
                progress = (frame_num / total_frames) * 100
                logger.info(f"📸 Progreso frames: {progress:.1f}%")
        
        logger.info(f"✅ Generados {len(frame_paths)} frames exitosamente")
        return frame_paths
    
    def frames_to_video_command(self, frame_paths: List[str], audio_file: str, 
                               output_path: str) -> str:
        """
        Genera comando FFmpeg para convertir frames a video
        """
        frames_pattern = str(Path(frame_paths[0]).parent / "frame_%06d.jpg")
        
        command = f"""ffmpeg -y -framerate {self.fps} -i "{frames_pattern}" -i "{audio_file}" -c:v libx264 -c:a aac -pix_fmt yuv420p -shortest -movflags +faststart "{output_path}" """
        
        return command.strip()