"""
AI Shorts Factory - Web Interface (Versión Simplificada)
Interfaz web moderna para generar y gestionar videos automáticamente
"""

from flask import Flask, render_template, request, jsonify, send_file, url_for
import os
import json
import asyncio
import threading
import time
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List

# Importar nuestros módulos
from main import YouTubeAutomation
from src.content_generator.ai_generator import ContentRequest, ContentGenerator
from config.settings import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai-shorts-factory-secret-key'

# Base de datos simple en memoria para el progreso
generation_progress = {}
video_library = []
generation_tasks = {}

class WebAutomation:
    """Wrapper para la automatización con progreso"""
    
    def __init__(self):
        self.automation = YouTubeAutomation()
    
    async def generate_video_with_progress(self, topic: str, content_type: str, session_id: str):
        """Genera video con actualizaciones de progreso"""
        try:
            # Inicializar progreso
            generation_progress[session_id] = {
                'step': 'Iniciando generación...',
                'progress': 0,
                'status': 'running',
                'start_time': datetime.now().isoformat(),
                'topic': topic,
                'content_type': content_type
            }
            
            # Paso 1: Generar contenido
            generation_progress[session_id].update({
                'step': 'Generando contenido con IA...',
                'progress': 20
            })
            
            request = ContentRequest(
                content_type=content_type,
                topic=topic,
                target_duration=45
            )
            
            # Paso 2: Crear video
            generation_progress[session_id].update({
                'step': 'Creando video...',
                'progress': 40
            })
            
            result = await self.automation.create_and_publish_video(request)
            
            # Paso 3: Finalizando
            generation_progress[session_id].update({
                'step': 'Finalizando...',
                'progress': 90
            })
            
            # Completado
            generation_progress[session_id].update({
                'step': 'Video generado exitosamente',
                'progress': 100,
                'status': 'completed',
                'result': result,
                'end_time': datetime.now().isoformat()
            })
            
            # Agregar a la biblioteca
            video_info = {
                'id': len(video_library) + 1,
                'title': result.get('title', topic),
                'topic': topic,
                'content_type': content_type,
                'video_path': result.get('video_path', ''),
                'thumbnail_path': result.get('thumbnail_path', ''),
                'duration': result.get('duration', 0),
                'seo_score': result.get('seo_score', 0),
                'created_at': datetime.now().isoformat(),
                'status': 'completed'
            }
            video_library.append(video_info)
            
            return result
            
        except Exception as e:
            logger.error(f"Error en generación: {e}")
            generation_progress[session_id].update({
                'step': f'Error: {str(e)}',
                'progress': 0,
                'status': 'error',
                'error': str(e),
                'end_time': datetime.now().isoformat()
            })
            raise

web_automation = WebAutomation()

# Temas predefinidos por categoría
TOPICS_DATABASE = {
    "TOP_5": {
        "Espacio y Ciencia": [
            "planetas más extraños del universo",
            "agujeros negros más peligrosos",
            "galaxias más lejanas descubiertas",
            "asteroides que casi destruyen la Tierra",
            "descubrimientos espaciales más recientes"
        ],
        "Misterios y Paranormal": [
            "lugares más misteriosos del mundo",
            "civilizaciones perdidas más fascinantes",
            "misterios sin resolver de la historia",
            "fenómenos paranormales más documentados",
            "lugares abandonados más escalofriantes"
        ],
        "Naturaleza y Animales": [
            "animales más raros del planeta",
            "criaturas marinas más profundas",
            "animales más peligrosos del mundo",
            "especies que creíamos extintas",
            "animales con superpoderes reales"
        ],
        "Tecnología y Futuro": [
            "tecnologías que cambiarán el mundo",
            "inventos más revolucionarios",
            "robots más avanzados del mundo",
            "coches del futuro más increíbles",
            "inteligencias artificiales más potentes"
        ],
        "Historia y Cultura": [
            "batallas más épicas de la historia",
            "emperadores más poderosos",
            "inventos que cambiaron la humanidad",
            "construcciones más imposibles",
            "tesoros perdidos más valiosos"
        ]
    },
    "CURIOSIDADES": [
        "datos sorprendentes sobre el cerebro humano",
        "misterios de las pirámides de Egipto",
        "secretos ocultos de la naturaleza",
        "curiosidades sobre los océanos",
        "fenómenos naturales más extraños",
        "datos curiosos sobre el espacio",
        "misterios de la física cuántica",
        "curiosidades sobre los dinosaurios",
        "secretos del cuerpo humano",
        "datos raros sobre el tiempo"
    ]
}

@app.route('/')
def index():
    """Página principal"""
    return render_template('simple_index.html')

@app.route('/api/topics')
def get_topics():
    """API para obtener temas disponibles"""
    return jsonify(TOPICS_DATABASE)

@app.route('/api/library')
def get_video_library():
    """API para obtener la biblioteca de videos"""
    return jsonify(video_library)

@app.route('/api/generate', methods=['POST'])
def generate_video():
    """API para iniciar generación de video"""
    data = request.json
    topic = data.get('topic', '').strip()
    content_type = data.get('content_type', 'TOP_5')
    session_id = data.get('session_id', f'session_{int(time.time())}')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # Verificar si ya hay una generación en curso
    if session_id in generation_tasks and generation_tasks[session_id].is_alive():
        return jsonify({'error': 'Generation already in progress'}), 409
    
    # Iniciar generación en hilo separado
    def run_generation():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(
                web_automation.generate_video_with_progress(topic, content_type, session_id)
            )
        except Exception as e:
            logger.error(f"Error en generación: {e}")
        finally:
            loop.close()
    
    thread = threading.Thread(target=run_generation)
    thread.daemon = True
    thread.start()
    
    generation_tasks[session_id] = thread
    
    return jsonify({'status': 'started', 'session_id': session_id})

@app.route('/api/progress/<session_id>')
def get_progress(session_id):
    """API para obtener progreso de generación"""
    progress = generation_progress.get(session_id, {'status': 'not_found'})
    return jsonify(progress)

@app.route('/api/video/<int:video_id>')
def serve_video(video_id):
    """Servir archivo de video"""
    video = next((v for v in video_library if v['id'] == video_id), None)
    if not video or not video.get('video_path'):
        return jsonify({'error': 'Video not found'}), 404
    
    video_path = Path(video['video_path'])
    if not video_path.exists():
        return jsonify({'error': 'Video file not found'}), 404
    
    return send_file(video_path, as_attachment=False)

@app.route('/api/thumbnail/<int:video_id>')
def serve_thumbnail(video_id):
    """Servir archivo de thumbnail"""
    video = next((v for v in video_library if v['id'] == video_id), None)
    if not video or not video.get('thumbnail_path'):
        return jsonify({'error': 'Thumbnail not found'}), 404
    
    thumbnail_path = Path(video['thumbnail_path'])
    if not thumbnail_path.exists():
        return jsonify({'error': 'Thumbnail file not found'}), 404
    
    return send_file(thumbnail_path, as_attachment=False)

@app.route('/api/delete/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    """Eliminar video de la biblioteca"""
    global video_library
    video = next((v for v in video_library if v['id'] == video_id), None)
    
    if not video:
        return jsonify({'error': 'Video not found'}), 404
    
    # Eliminar archivos físicos
    try:
        if video.get('video_path') and Path(video['video_path']).exists():
            Path(video['video_path']).unlink()
        if video.get('thumbnail_path') and Path(video['thumbnail_path']).exists():
            Path(video['thumbnail_path']).unlink()
    except Exception as e:
        logger.warning(f"Error eliminando archivos: {e}")
    
    # Eliminar de la biblioteca
    video_library = [v for v in video_library if v['id'] != video_id]
    
    return jsonify({'status': 'deleted'})

@app.route('/api/status')
def get_status():
    """API para obtener estado general"""
    active_generations = sum(1 for task in generation_tasks.values() if task.is_alive())
    
    return jsonify({
        'active_generations': active_generations,
        'total_videos': len(video_library),
        'available_topics': sum(len(topics) if isinstance(topics, list) else sum(len(t) for t in topics.values()) 
                               for topics in TOPICS_DATABASE.values())
    })

# Cargar biblioteca existente al iniciar
def load_existing_videos():
    """Cargar videos existentes desde el directorio de salida"""
    output_dir = Path("output/videos")
    if not output_dir.exists():
        return
    
    for video_file in output_dir.glob("*.mp4"):
        # Buscar thumbnail correspondiente
        thumbnail_file = None
        for thumb in output_dir.glob(f"thumbnail*{video_file.stem}*.jpg"):
            thumbnail_file = thumb
            break
        
        # Extraer información del nombre del archivo
        name_parts = video_file.stem.replace('short_', '').split('_')
        content_type = name_parts[0] if name_parts else 'TOP_5'
        topic = ' '.join(name_parts[1:]) if len(name_parts) > 1 else video_file.stem
        
        video_info = {
            'id': len(video_library) + 1,
            'title': topic.replace('_', ' ').title(),
            'topic': topic.replace('_', ' '),
            'content_type': content_type,
            'video_path': str(video_file),
            'thumbnail_path': str(thumbnail_file) if thumbnail_file else '',
            'duration': 0,  # Se podría calcular con ffprobe
            'seo_score': 85,  # Valor por defecto
            'created_at': datetime.fromtimestamp(video_file.stat().st_mtime).isoformat(),
            'status': 'completed'
        }
        video_library.append(video_info)

if __name__ == '__main__':
    # Cargar videos existentes
    load_existing_videos()
    
    # Crear directorio de templates si no existe
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    logger.info("🚀 Iniciando AI Shorts Factory Web Interface...")
    logger.info(f"📚 Videos cargados: {len(video_library)}")
    
    # Ejecutar la aplicación (sin SocketIO para compatibilidad)
    app.run(debug=True, host='0.0.0.0', port=5000)