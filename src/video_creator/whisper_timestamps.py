"""
🎯 SISTEMA DE TIMESTAMPS PRECISOS CON WHISPER
Analiza audio generado por IA y extrae timestamps exactos de cada palabra
"""

import whisper
import logging
from pathlib import Path
from typing import List, Dict, Optional
import json

logger = logging.getLogger(__name__)

class WhisperTimestampExtractor:
    """Extractor de timestamps precisos usando Whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Inicializa el extractor de timestamps
        
        Args:
            model_size: Tamaño del modelo Whisper (tiny, base, small, medium, large)
                       - tiny: Más rápido, menos preciso
                       - base: Buen balance (recomendado para Shorts)
                       - small/medium: Más preciso, más lento
        """
        self.model_size = model_size
        self.model = None
        self.last_audio_path = None
        self.last_results = None
        
    def load_model(self):
        """Carga el modelo Whisper solo cuando se necesita"""
        if self.model is None:
            logger.info(f"🤖 Cargando modelo Whisper '{self.model_size}'...")
            try:
                self.model = whisper.load_model(self.model_size)
                logger.info("✅ Modelo Whisper cargado exitosamente")
            except Exception as e:
                logger.error(f"❌ Error cargando Whisper: {e}")
                raise
    
    def extract_word_timestamps(self, audio_path: str, expected_text: str = None) -> List[Dict]:
        """
        Extrae timestamps precisos de cada palabra del audio
        
        Args:
            audio_path: Ruta al archivo de audio
            expected_text: Texto esperado (opcional, para validación)
            
        Returns:
            Lista de diccionarios con formato:
            [
                {
                    'word': 'palabra',
                    'start': 1.23,
                    'end': 1.87,
                    'confidence': 0.95
                }, ...
            ]
        """
        self.load_model()
        
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Archivo de audio no encontrado: {audio_path}")
        
        logger.info(f"🎧 Analizando audio: {audio_path}")
        
        try:
            # Transcribir con word timestamps
            result = self.model.transcribe(
                audio_path,
                language="es",  # Español
                word_timestamps=True,
                verbose=False
            )
            
            # Extraer palabras con timestamps
            word_timestamps = []
            
            for segment in result['segments']:
                if 'words' in segment:
                    for word_data in segment['words']:
                        word_info = {
                            'word': word_data.get('word', '').strip(),
                            'start': word_data.get('start', 0.0),
                            'end': word_data.get('end', 0.0),
                            'confidence': word_data.get('probability', 0.0)
                        }
                        
                        # Filtrar palabras vacías
                        if word_info['word']:
                            word_timestamps.append(word_info)
            
            # Estadísticas de análisis
            total_duration = max([w['end'] for w in word_timestamps]) if word_timestamps else 0
            total_words = len(word_timestamps)
            avg_word_duration = total_duration / total_words if total_words > 0 else 0
            
            logger.info(f"📊 Análisis completado:")
            logger.info(f"   • Duración total: {total_duration:.2f}s")
            logger.info(f"   • Palabras detectadas: {total_words}")
            logger.info(f"   • Duración promedio por palabra: {avg_word_duration:.3f}s")
            logger.info(f"   • Texto transcrito: '{result.get('text', '').strip()}'")
            
            # Validar contra texto esperado si se proporciona
            if expected_text:
                transcribed_text = result.get('text', '').strip().lower()
                expected_clean = expected_text.strip().lower()
                similarity = self._calculate_text_similarity(transcribed_text, expected_clean)
                logger.info(f"   • Similitud con texto esperado: {similarity:.1%}")
                
                if similarity < 0.7:
                    logger.warning(f"⚠️ Baja similitud entre textos:")
                    logger.warning(f"   Esperado: '{expected_clean[:100]}...'")
                    logger.warning(f"   Detectado: '{transcribed_text[:100]}...'")
            
            # Guardar resultados para cache
            self.last_audio_path = audio_path
            self.last_results = word_timestamps
            
            return word_timestamps
            
        except Exception as e:
            logger.error(f"❌ Error analizando audio: {e}")
            raise
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calcula similitud básica entre textos"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def save_timestamps_json(self, word_timestamps: List[Dict], output_path: str):
        """Guarda los timestamps en formato JSON"""
        timestamp_data = {
            'version': '1.0',
            'model': self.model_size,
            'total_words': len(word_timestamps),
            'total_duration': max([w['end'] for w in word_timestamps]) if word_timestamps else 0,
            'words': word_timestamps
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(timestamp_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Timestamps guardados en: {output_path}")
    
    def create_srt_subtitles(self, word_timestamps: List[Dict], output_path: str, 
                           words_per_subtitle: int = 3):
        """
        Genera archivo SRT con subtítulos agrupados
        
        Args:
            word_timestamps: Lista de timestamps de palabras
            output_path: Ruta del archivo SRT de salida
            words_per_subtitle: Número de palabras por subtítulo
        """
        srt_content = []
        subtitle_number = 1
        
        for i in range(0, len(word_timestamps), words_per_subtitle):
            # Agrupar palabras
            word_group = word_timestamps[i:i + words_per_subtitle]
            
            # Calcular tiempos de inicio y fin
            start_time = word_group[0]['start']
            end_time = word_group[-1]['end']
            
            # Texto del subtítulo
            subtitle_text = ' '.join([w['word'] for w in word_group])
            
            # Formato SRT
            start_srt = self._seconds_to_srt_time(start_time)
            end_srt = self._seconds_to_srt_time(end_time)
            
            srt_content.append(f"{subtitle_number}")
            srt_content.append(f"{start_srt} --> {end_srt}")
            srt_content.append(subtitle_text)
            srt_content.append("")  # Línea vacía
            
            subtitle_number += 1
        
        # Guardar archivo SRT
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        
        logger.info(f"📝 Subtítulos SRT guardados en: {output_path}")
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convierte segundos a formato de tiempo SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


class PreciseSubtitleGenerator:
    """Generador de subtítulos con timestamps precisos de Whisper"""
    
    def __init__(self):
        self.extractor = WhisperTimestampExtractor(model_size="base")
        
    def generate_precise_timeline(self, audio_path: str, script_text: str) -> List[Dict]:
        """
        Genera timeline preciso basado en análisis real del audio
        
        Returns:
            Timeline con formato mejorado para subtítulos dinámicos
        """
        # Extraer timestamps reales
        word_timestamps = self.extractor.extract_word_timestamps(audio_path, script_text)
        
        if not word_timestamps:
            logger.warning("⚠️ No se pudieron extraer timestamps, usando fallback")
            return self._create_fallback_timeline(script_text, 30.0)  # Fallback básico
        
        # Convertir a formato compatible con el sistema de video
        precise_timeline = []
        
        for word_data in word_timestamps:
            timeline_entry = {
                'word': word_data['word'].strip().upper(),
                'start': word_data['start'],
                'end': word_data['end'],
                'duration': word_data['end'] - word_data['start'],
                'confidence': word_data.get('confidence', 1.0)
            }
            precise_timeline.append(timeline_entry)
        
        logger.info(f"✅ Timeline preciso generado con {len(precise_timeline)} palabras")
        return precise_timeline
    
    def _create_fallback_timeline(self, script_text: str, duration: float) -> List[Dict]:
        """Timeline de fallback si Whisper falla"""
        words = script_text.split()
        words_per_second = len(words) / duration
        seconds_per_word = duration / len(words) if len(words) > 0 else 0.5
        
        fallback_timeline = []
        for i, word in enumerate(words):
            start_time = i * seconds_per_word
            end_time = (i + 1) * seconds_per_word
            
            timeline_entry = {
                'word': word.upper(),
                'start': start_time,
                'end': end_time,
                'duration': seconds_per_word,
                'confidence': 0.5  # Baja confianza para fallback
            }
            fallback_timeline.append(timeline_entry)
        
        logger.warning(f"⚠️ Usando timeline de fallback con {len(fallback_timeline)} palabras")
        return fallback_timeline