"""
YouTube Publisher Module
Publicación automática de videos en YouTube.
"""

from .uploader import YouTubePublisher, VideoScheduler

# Alias para compatibilidad
YouTubeUploader = YouTubePublisher

__all__ = ['YouTubePublisher', 'YouTubeUploader', 'VideoScheduler']