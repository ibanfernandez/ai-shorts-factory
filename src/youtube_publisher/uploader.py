"""
Publicador automático para YouTube usando la API v3.
Maneja subida de videos, optimización SEO y programación.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.http import MediaFileUpload
except ImportError as e:
    logging.warning(f"Google API client no disponible: {e}")

from config.settings import settings

logger = logging.getLogger(__name__)

@dataclass
class VideoMetadata:
    """Metadatos de un video para YouTube."""
    title: str
    description: str
    tags: List[str]
    category_id: str = "24"  # Entertainment
    privacy_status: str = "private"  # "private", "public", "unlisted"
    language: str = "es"
    thumbnail_path: Optional[str] = None
    publish_at: Optional[datetime] = None

@dataclass
class UploadResult:
    """Resultado de una subida a YouTube."""
    success: bool
    video_id: Optional[str] = None
    url: Optional[str] = None
    error_message: Optional[str] = None
    upload_time: Optional[datetime] = None

class YouTubePublisher:
    """Publicador automático para YouTube."""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self):
        """Inicializa el publicador de YouTube."""
        self.credentials_file = settings.PROJECT_ROOT / "config" / "youtube_credentials.json"
        self.token_file = settings.PROJECT_ROOT / "config" / "youtube_token.json"
        self.youtube_service = None
        
        logger.info("YouTubePublisher inicializado")
    
    def authenticate(self) -> bool:
        """
        Autentica con la API de YouTube.
        
        Returns:
            bool: True si la autenticación es exitosa
        """
        try:
            creds = None
            
            # Cargar token existente
            if self.token_file.exists():
                creds = Credentials.from_authorized_user_file(str(self.token_file), self.SCOPES)
            
            # Si no hay credenciales válidas, obtener nuevas
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not self.credentials_file.exists():
                        logger.error("Archivo de credenciales no encontrado. Descárgalo desde Google Cloud Console.")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_file), self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Guardar credenciales
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())
            
            # Crear servicio de YouTube
            self.youtube_service = build('youtube', 'v3', credentials=creds)
            logger.info("Autenticación exitosa con YouTube API")
            return True
            
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            return False
    
    def upload_video(self, video_path: str, metadata: VideoMetadata) -> UploadResult:
        """
        Sube un video a YouTube.
        
        Args:
            video_path: Ruta del archivo de video
            metadata: Metadatos del video
        
        Returns:
            UploadResult: Resultado de la subida
        """
        if not self.youtube_service:
            if not self.authenticate():
                return UploadResult(
                    success=False,
                    error_message="Error de autenticación"
                )
        
        try:
            # Validar archivo
            if not os.path.exists(video_path):
                return UploadResult(
                    success=False,
                    error_message=f"Archivo no encontrado: {video_path}"
                )
            
            # Preparar metadatos del video
            body = {
                'snippet': {
                    'title': metadata.title[:100],  # YouTube limit
                    'description': self._optimize_description(metadata.description),
                    'tags': metadata.tags[:500],  # YouTube limit
                    'categoryId': metadata.category_id,
                    'defaultLanguage': metadata.language
                },
                'status': {
                    'privacyStatus': metadata.privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Añadir programación si está especificada
            if metadata.publish_at and metadata.privacy_status == "private":
                body['status']['publishAt'] = metadata.publish_at.isoformat() + 'Z'
            
            # Preparar upload
            media = MediaFileUpload(
                video_path,
                chunksize=-1,  # Upload en una sola vez
                resumable=True
            )
            
            # Realizar upload
            insert_request = self.youtube_service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = self._resumable_upload(insert_request)
            
            if response:
                video_id = response['id']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                logger.info(f"Video subido exitosamente: {video_url}")
                
                # Subir thumbnail si existe
                if metadata.thumbnail_path and os.path.exists(metadata.thumbnail_path):
                    self._upload_thumbnail(video_id, metadata.thumbnail_path)
                
                return UploadResult(
                    success=True,
                    video_id=video_id,
                    url=video_url,
                    upload_time=datetime.now()
                )
            else:
                return UploadResult(
                    success=False,
                    error_message="Error desconocido en upload"
                )
                
        except HttpError as e:
            error_msg = f"Error HTTP: {e.resp.status} - {e.content.decode()}"
            logger.error(error_msg)
            return UploadResult(success=False, error_message=error_msg)
        
        except Exception as e:
            error_msg = f"Error general: {str(e)}"
            logger.error(error_msg)
            return UploadResult(success=False, error_message=error_msg)
    
    def _resumable_upload(self, insert_request) -> Optional[Dict[str, Any]]:
        """Maneja la subida resumible del video."""
        
        response = None
        error = None
        retry = 0
        max_retries = 3
        
        while response is None:
            try:
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        return response
                    else:
                        raise Exception(f"Upload falló: {response}")
                        
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    # Errores recuperables
                    error = f"Error recuperable: {e.resp.status}"
                    retry += 1
                    if retry > max_retries:
                        break
                else:
                    # Error no recuperable
                    raise e
            
            except Exception as e:
                error = f"Error inesperado: {str(e)}"
                break
        
        if error:
            logger.error(f"Upload falló después de {retry} reintentos: {error}")
        
        return None
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """Sube un thumbnail para el video."""
        
        try:
            media = MediaFileUpload(thumbnail_path)
            
            request = self.youtube_service.thumbnails().set(
                videoId=video_id,
                media_body=media
            )
            
            response = request.execute()
            logger.info(f"Thumbnail subido para video {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error subiendo thumbnail: {e}")
            return False
    
    def _optimize_description(self, description: str) -> str:
        """Optimiza la descripción para SEO."""
        
        # Límite de YouTube: 5000 caracteres
        if len(description) > 4800:
            description = description[:4800] + "..."
        
        # Añadir elementos SEO estándar
        seo_footer = """

🔔 ¡SUSCRÍBETE para más contenido increíble!
👍 Dale LIKE si te gustó el video
💬 COMENTA qué te pareció más interesante
🔄 COMPARTE con tus amigos

#Top10 #Curiosidades #Español #Interesante #Viral #Educativo

📧 Contacto: [tu-email@ejemplo.com]
🌐 Síguenos en redes sociales

⚠️ Derechos de autor: Todas las imágenes y clips utilizados pertenecen a sus respectivos propietarios.
"""
        
        # Solo añadir si hay espacio
        if len(description) + len(seo_footer) <= 5000:
            description += seo_footer
        
        return description
    
    def schedule_video(self, video_path: str, metadata: VideoMetadata, 
                      publish_time: datetime) -> UploadResult:
        """
        Programa un video para publicación posterior.
        
        Args:
            video_path: Ruta del video
            metadata: Metadatos del video
            publish_time: Cuándo publicar
        
        Returns:
            UploadResult: Resultado de la programación
        """
        # Establecer como privado inicialmente
        metadata.privacy_status = "private"
        metadata.publish_at = publish_time
        
        return self.upload_video(video_path, metadata)
    
    def get_video_analytics(self, video_id: str) -> Optional[Dict]:
        """
        Obtiene analíticas básicas de un video.
        
        Args:
            video_id: ID del video de YouTube
        
        Returns:
            Dict: Datos de analíticas o None si hay error
        """
        if not self.youtube_service:
            if not self.authenticate():
                return None
        
        try:
            request = self.youtube_service.videos().list(
                part="statistics,snippet",
                id=video_id
            )
            
            response = request.execute()
            
            if response['items']:
                item = response['items'][0]
                return {
                    'video_id': video_id,
                    'title': item['snippet']['title'],
                    'published_at': item['snippet']['publishedAt'],
                    'view_count': int(item['statistics'].get('viewCount', 0)),
                    'like_count': int(item['statistics'].get('likeCount', 0)),
                    'comment_count': int(item['statistics'].get('commentCount', 0)),
                    'retrieved_at': datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo analíticas: {e}")
            return None
    
    def get_channel_info(self) -> Optional[Dict]:
        """Obtiene información básica del canal."""
        
        if not self.youtube_service:
            if not self.authenticate():
                return None
        
        try:
            request = self.youtube_service.channels().list(
                part="snippet,statistics",
                mine=True
            )
            
            response = request.execute()
            
            if response['items']:
                channel = response['items'][0]
                return {
                    'channel_id': channel['id'],
                    'title': channel['snippet']['title'],
                    'subscriber_count': int(channel['statistics'].get('subscriberCount', 0)),
                    'video_count': int(channel['statistics'].get('videoCount', 0)),
                    'view_count': int(channel['statistics'].get('viewCount', 0))
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo info del canal: {e}")
            return None

class VideoScheduler:
    """Programador de videos para publicación automática."""
    
    def __init__(self):
        """Inicializa el programador."""
        self.schedule_file = settings.DATA_DIR / "video_schedule.json"
        self.publisher = YouTubePublisher()
        
    def add_to_schedule(self, video_path: str, metadata: VideoMetadata, 
                       publish_time: datetime) -> bool:
        """Añade un video a la programación."""
        
        try:
            # Cargar programación existente
            schedule = self._load_schedule()
            
            # Añadir nuevo video
            schedule.append({
                'video_path': video_path,
                'metadata': {
                    'title': metadata.title,
                    'description': metadata.description,
                    'tags': metadata.tags,
                    'category_id': metadata.category_id,
                    'privacy_status': metadata.privacy_status,
                    'thumbnail_path': metadata.thumbnail_path
                },
                'publish_time': publish_time.isoformat(),
                'status': 'scheduled',
                'created_at': datetime.now().isoformat()
            })
            
            # Guardar programación
            self._save_schedule(schedule)
            logger.info(f"Video programado para {publish_time}")
            return True
            
        except Exception as e:
            logger.error(f"Error programando video: {e}")
            return False
    
    def process_scheduled_videos(self) -> int:
        """Procesa videos programados que deben publicarse ahora."""
        
        processed = 0
        now = datetime.now()
        
        try:
            schedule = self._load_schedule()
            updated_schedule = []
            
            for item in schedule:
                publish_time = datetime.fromisoformat(item['publish_time'])
                
                if item['status'] == 'scheduled' and publish_time <= now:
                    # Tiempo de publicar
                    metadata = VideoMetadata(**item['metadata'])
                    result = self.publisher.upload_video(item['video_path'], metadata)
                    
                    if result.success:
                        item['status'] = 'published'
                        item['video_id'] = result.video_id
                        item['published_at'] = datetime.now().isoformat()
                        processed += 1
                        logger.info(f"Video publicado: {result.url}")
                    else:
                        item['status'] = 'failed'
                        item['error'] = result.error_message
                        logger.error(f"Error publicando video: {result.error_message}")
                
                updated_schedule.append(item)
            
            # Guardar programación actualizada
            self._save_schedule(updated_schedule)
            
        except Exception as e:
            logger.error(f"Error procesando videos programados: {e}")
        
        return processed
    
    def _load_schedule(self) -> List[Dict]:
        """Carga la programación desde archivo."""
        
        if self.schedule_file.exists():
            try:
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error cargando programación: {e}")
        
        return []
    
    def _save_schedule(self, schedule: List[Dict]) -> None:
        """Guarda la programación en archivo."""
        
        try:
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(schedule, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando programación: {e}")

# Función de utilidad para upload rápido
def quick_upload(video_path: str, title: str, description: str, 
                tags: List[str], privacy: str = "private") -> UploadResult:
    """
    Sube un video rápidamente con configuración básica.
    
    Args:
        video_path: Ruta del video
        title: Título del video
        description: Descripción
        tags: Lista de tags
        privacy: Estado de privacidad
    
    Returns:
        UploadResult: Resultado de la subida
    """
    publisher = YouTubePublisher()
    
    metadata = VideoMetadata(
        title=title,
        description=description,
        tags=tags,
        privacy_status=privacy
    )
    
    return publisher.upload_video(video_path, metadata)

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Ejemplo de uso
    publisher = YouTubePublisher()
    
    if publisher.authenticate():
        # Obtener info del canal
        channel_info = publisher.get_channel_info()
        if channel_info:
            print(f"Canal: {channel_info['title']}")
            print(f"Suscriptores: {channel_info['subscriber_count']}")
        
        # Ejemplo de metadata
        metadata = VideoMetadata(
            title="TOP 10 Prueba de Automatización",
            description="Video de prueba generado automáticamente",
            tags=["test", "automatización", "top10"],
            privacy_status="private"
        )
        
        # Nota: Descomenta para realizar upload real
        # result = publisher.upload_video("path/to/video.mp4", metadata)
        # print(f"Upload exitoso: {result.success}")
    else:
        print("Error en autenticación. Verifica tus credenciales.")