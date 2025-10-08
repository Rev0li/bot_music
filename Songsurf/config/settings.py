"""
Configuration globale de Songsurf
"""

class Settings:
    # UI
    THEME = "dark"  # dark/light/system
    COLOR_SCHEME = "blue"
    
    # Chrome Extension
    WS_PORT = 8765
    
    # Paths
    DEFAULT_DOWNLOAD_FOLDER = "~/Music/Downloads"
    DEFAULT_ORGANIZED_FOLDER = "~/Music/Library"

settings = Settings()
