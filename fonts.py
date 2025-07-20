# fonts.py - 8-Bit Schriftarten Manager
import arcade
import os
from config import *

class FontManager:
    """Manager für 8-Bit Schriftarten"""
    
    # Standard 8-Bit Schriftarten (falls verfügbar)
    FONTS = {
        'title': 'Courier New',      # Fallback für Titel
        'menu': 'Courier New',       # Fallback für Menü
        'game': 'Courier New',       # Fallback für Spiel-UI
        'small': 'Courier New'       # Fallback für kleine Texte
    }
    
    def __init__(self):
        self.fonts_loaded = False
        self._load_fonts()
    
    def _load_fonts(self):
        """Lädt 8-Bit Schriftarten"""
        try:
            # Versuche 8-Bit Schriftarten zu laden
            font_paths = self._get_font_paths()
            
            for font_name, font_path in font_paths.items():
                if os.path.exists(font_path):
                    self.FONTS[font_name] = font_path
                    print(f"✓ {font_name} Schriftart geladen: {font_path}")
                else:
                    print(f"⚠ {font_name} Schriftart nicht gefunden: {font_path}")
            
            self.fonts_loaded = True
            
        except Exception as e:
            print(f"Fehler beim Laden der Schriftarten: {e}")
            print("Verwende Standard-Schriftarten")
            self._use_builtin_fonts()
    
    def _get_font_paths(self):
        """Gibt Pfade zu 8-Bit Schriftarten zurück"""
        # Erstelle einen 'fonts' Ordner in deinem Projektverzeichnis
        fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
        
        return {
            'title': os.path.join(fonts_dir, 'PixeloidSans-Bold.ttf'),
            'menu': os.path.join(fonts_dir, 'PixeloidSans.ttf'),
            'game': os.path.join(fonts_dir, 'PixeloidMono.ttf'),
            'small': os.path.join(fonts_dir, 'PixeloidSans-Bold.ttf')
        }
    
    def _use_builtin_fonts(self):
        """Verwendet eingebaute monospace Schriftarten für 8-Bit Look"""
        self.FONTS = {
            'title': 'Courier New',
            'menu': 'Consolas',
            'game': 'Monaco',
            'small': 'Courier New'
        }
    
    def get_font(self, font_type='game'):
        """Gibt die passende Schriftart zurück"""
        return self.FONTS.get(font_type, 'Courier New')
    
    def create_text(self, text, x, y, font_type='game', size=16, color=arcade.color.WHITE, **kwargs):
        """Erstellt ein Text-Objekt mit 8-Bit Schriftart"""
        font_name = self.get_font(font_type)
        
        # Füge 8-Bit Styling hinzu
        kwargs.setdefault('font_name', font_name)
        kwargs.setdefault('bold', True)  # 8-Bit Texte sind oft fett
        
        return arcade.Text(text, x, y, color, size, **kwargs)
    
    def draw_text(self, text, x, y, font_type='game', size=16, color=arcade.color.WHITE, **kwargs):
        """Zeichnet Text mit 8-Bit Schriftart"""
        font_name = self.get_font(font_type)
        
        # Füge 8-Bit Styling hinzu
        kwargs.setdefault('font_name', font_name)
        kwargs.setdefault('bold', True)
        
        arcade.draw_text(text, x, y, color, size, **kwargs)
    
    def draw_outlined_text(self, text, x, y, font_type='game', size=16, 
                          color=arcade.color.WHITE, outline_color=arcade.color.BLACK, 
                          outline_width=2, **kwargs):
        """Zeichnet Text mit Umrandung für bessere Lesbarkeit"""
        font_name = self.get_font(font_type)
        kwargs.setdefault('font_name', font_name)
        kwargs.setdefault('bold', True)
        
        # Zeichne Umrandung (8 Richtungen)
        for dx in [-outline_width, 0, outline_width]:
            for dy in [-outline_width, 0, outline_width]:
                if dx != 0 or dy != 0:
                    arcade.draw_text(text, x + dx, y + dy, outline_color, size, **kwargs)
        
        # Zeichne Haupttext
        arcade.draw_text(text, x, y, color, size, **kwargs)
    
    def draw_retro_text(self, text, x, y, font_type='game', size=16, 
                       color=arcade.color.WHITE, glow=True, **kwargs):
        """Zeichnet Text im Retro-Stil mit optionalem Glow-Effekt"""
        font_name = self.get_font(font_type)
        kwargs.setdefault('font_name', font_name)
        kwargs.setdefault('bold', True)
        
        if glow:
            # Glow-Effekt durch mehrere Schichten
            glow_color = (*color[:3], 100)  # Transparente Version der Hauptfarbe
            
            for i in range(3, 0, -1):
                arcade.draw_text(text, x, y, glow_color, size + i*2, **kwargs)
        
        # Haupttext
        arcade.draw_text(text, x, y, color, size, **kwargs)

# Globaler Font Manager
font_manager = FontManager()

# Convenience Funktionen
def draw_8bit_text(text, x, y, font_type='game', size=16, color=arcade.color.WHITE, **kwargs):
    """Schnelle Funktion zum Zeichnen von 8-Bit Text"""
    return font_manager.draw_text(text, x, y, font_type, size, color, **kwargs)

def draw_pixel_text(text, x, y, size=16, color=arcade.color.WHITE, outline=True, **kwargs):
    """Zeichnet pixeligen Text mit optionaler Umrandung"""
    if outline:
        font_manager.draw_outlined_text(text, x, y, 'game', size, color, **kwargs)
    else:
        font_manager.draw_text(text, x, y, 'game', size, color, **kwargs)

def draw_title_text(text, x, y, size=48, color=arcade.color.WHITE, retro=True, **kwargs):
    """Zeichnet großen Titel-Text im 8-Bit Stil"""
    if retro:
        font_manager.draw_retro_text(text, x, y, 'title', size, color, **kwargs)
    else:
        font_manager.draw_text(text, x, y, 'title', size, color, **kwargs)

def create_8bit_text(text, x, y, font_type='game', size=16, color=arcade.color.WHITE, **kwargs):
    """Erstellt 8-Bit Text-Objekt für bessere Performance"""
    return font_manager.create_text(text, x, y, font_type, size, color, **kwargs)

# ASCII Art Generator für 8-Bit Look
class ASCIIArt:
    """Klasse für ASCII Art im 8-Bit Stil"""
    
    @staticmethod
    def draw_pixel_border(x, y, width, height, color=arcade.color.WHITE, thickness=2):
        """Zeichnet einen pixeligen Rahmen"""
        # Ecken
        corner_size = thickness * 2
        
        # Obere Linie
        arcade.draw_rectangle_filled(x + width//2, y + height - thickness//2, 
                                   width - corner_size, thickness, color)
        # Untere Linie  
        arcade.draw_rectangle_filled(x + width//2, y + thickness//2, 
                                   width - corner_size, thickness, color)
        # Linke Linie
        arcade.draw_rectangle_filled(x + thickness//2, y + height//2, 
                                   thickness, height - corner_size, color)
        # Rechte Linie
        arcade.draw_rectangle_filled(x + width - thickness//2, y + height//2, 
                                   thickness, height - corner_size, color)
        
        # Ecken
        corner_positions = [
            (x, y + height - corner_size),  # Links oben
            (x + width - corner_size, y + height - corner_size),  # Rechts oben
            (x, y),  # Links unten
            (x + width - corner_size, y)   # Rechts unten
        ]
        
        for corner_x, corner_y in corner_positions:
            arcade.draw_rectangle_filled(corner_x + corner_size//2, corner_y + corner_size//2,
                                       corner_size, corner_size, color)
    
    @staticmethod
    def draw_pixel_button(x, y, width, height, text, pressed=False,
                         bg_color=arcade.color.DARK_GRAY, 
                         text_color=arcade.color.WHITE):
        """Zeichnet einen pixeligen Button"""
        offset = 2 if pressed else 0
        
        # Button-Hintergrund
        arcade.draw_rectangle_filled(x + width//2 + offset, y + height//2 - offset, 
                                   width, height, bg_color)
        
        # Button-Rahmen
        border_color = arcade.color.LIGHT_GRAY if not pressed else arcade.color.BLACK
        ASCIIArt.draw_pixel_border(x + offset, y - offset, width, height, border_color)
        
        # Button-Text
        text_x = x + width//2 + offset
        text_y = y + height//2 - offset
        draw_pixel_text(text, text_x, text_y, 14, text_color, outline=False, anchor_x="center")

# Installationsanleitung für Schriftarten
def print_font_installation_guide():
    """Gibt Anweisungen zur Installation von 8-Bit Schriftarten aus"""
    print("\n" + "="*60)
    print("🎮 8-BIT SCHRIFTARTEN INSTALLATIONSANLEITUNG")
    print("="*60)
    print("\n1. Erstelle einen 'fonts' Ordner in deinem Projektverzeichnis")
    print("\n2. Lade kostenlose 8-Bit Schriftarten herunter:")
    print("   • Google Fonts: https://fonts.google.com")
    print("     - Suche nach 'pixel', 'mono', '8-bit'")
    print("     - Empfohlen: Press Start 2P, VT323, Share Tech Mono")
    print("\n   • DaFont: https://www.dafont.com/bitmap.php")
    print("     - Viele kostenlose Pixel-Schriftarten")
    print("\n   • 1001Fonts: https://www.1001fonts.com/pixel-fonts.html")
    print("     - Große Auswahl an 8-Bit Fonts")
    print("\n3. Benenne die .ttf Dateien um:")
    print("   • PixeloidSans-Bold.ttf (für Titel)")
    print("   • PixeloidSans.ttf (für Menüs)")  
    print("   • PixeloidMono.ttf (für Spiel-UI)")
    print("\n4. Platziere sie im 'fonts/' Ordner")
    print("\n5. Starte das Spiel neu")
    print("\n" + "="*60)

# Automatisch Anleitung anzeigen wenn keine Schriftarten gefunden
if not font_manager.fonts_loaded:
    print_font_installation_guide()
    