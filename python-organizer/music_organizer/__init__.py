"""
Music Organizer - Package principal
Organise automatiquement les fichiers MP3 avec métadonnées
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .parser import MetadataParser
from .organizer import MusicOrganizer
from .monitor import DownloadMonitor

try:
    from .auto_saver import AutoSaver
    __all__ = ['MetadataParser', 'MusicOrganizer', 'DownloadMonitor', 'AutoSaver']
except ImportError:
    __all__ = ['MetadataParser', 'MusicOrganizer', 'DownloadMonitor']
