# menu.py - Startbildschirm und Menüs
import arcade
import math
from config import *

class MenuView(arcade.View):
    """Startbildschirm des Spiels"""
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(BACKGROUND_COLOR)
        
        # Animation
        self.animation_timer = 0
        self.wave_offset = 0
        
        # Text-Objekte für bessere Performance
        self.title_text = None
        self.subtitle_text = None
        self.start_text = None
        self.controls_text = None
        self.credits_text = None
        
        self._create_text_objects()
    
    def _create_text_objects(self):
        """Erstellt Text-Objekte"""
        try:
            # Titel
            self.title_text = arcade.Text("SWIMMING GIM", 
                                        SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                                        arcade.color.WHITE, 48, 
                                        font_name="arial", anchor_x="center")
            
            # Untertitel
            self.subtitle_text = arcade.Text("Das ultimative Schwimmrennen", 
                                           SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200,
                                           arcade.color.LIGHT_BLUE, 20, 
                                           anchor_x="center")
            
            # Start-Anweisung
            self.start_text = arcade.Text("Drücke ENTER zum Starten", 
                                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                                        arcade.color.YELLOW, 24, 
                                        anchor_x="center")
            
            # Steuerung
            self.controls_text = arcade.Text("LEERTASTE = Schwimmen  |  R = Neustart", 
                                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                                           arcade.color.WHITE, 16, 
                                           anchor_x="center")
            
            # Credits
            self.credits_text = arcade.Text("Erstellt mit Python Arcade", 
                                          SCREEN_WIDTH // 2, 50,
                                          arcade.color.GRAY, 14, 
                                          anchor_x="center")
        except:
            # Fallback falls Text-Objekte nicht funktionieren
            pass
    
    def on_update(self, delta_time):
        """Update für Animationen"""
        self.animation_timer += delta_time
        self.wave_offset = math.sin(self.animation_timer * 2) * 10
    
    def on_draw(self):
        """Zeichnet den Startbildschirm"""
        self.clear()
        
        # Hintergrund-Elemente
        self._draw_animated_background()
        self._draw_preview_lanes()
        self._draw_animated_swimmers()
        
        # Text-Elemente
        self._draw_texts()
        
        # Dekorative Elemente
        self._draw_sharks()
        self._draw_bubbles()
    
    def _draw_animated_background(self):
        """Zeichnet animierten Wasser-Hintergrund"""
        # Wasser-Schichten für Tiefeneffekt
        for i in range(3):
            alpha = 100 - (i * 30)
            water_color = (*WATER_COLOR[:3], alpha)
            
            # Wellenförmige Wasserschichten
            for x in range(0, SCREEN_WIDTH, 20):
                wave_height = math.sin((x + self.animation_timer * 50 + i * 30) * 0.02) * 15
                rect_height = 80 + wave_height
                y_pos = SCREEN_HEIGHT // 2 + (i * 40) + wave_height
                
                water_rect = arcade.XYWH(x, y_pos - rect_height//2, 20, rect_height)
                arcade.draw_rect_filled(water_rect, water_color)
    
    def _draw_preview_lanes(self):
        """Zeichnet eine Vorschau der Schwimmbahnen"""
        preview_y = SCREEN_HEIGHT // 2 + 100
        preview_height = 100
        
        # Mini-Bahnen
        for i in range(4):  # Nur 4 Bahnen für Preview
            x = 100 + i * 100
            lane_rect = arcade.XYWH(x, preview_y, 80, preview_height)
            arcade.draw_rect_outline(lane_rect, LANE_COLOR, 2)
            
            # Bahnnummer
            arcade.draw_text(f"{i+1}", x + 35, preview_y + 40, 
                           arcade.color.WHITE, 16, anchor_x="center")
    
    def _draw_animated_swimmers(self):
        """Zeichnet animierte Mini-Schwimmer"""
        for i in range(3):
            # Position mit Animation
            x = 150 + i * 100 + math.sin(self.animation_timer * 3 + i) * 20
            y = SCREEN_HEIGHT // 2 + 100 + math.cos(self.animation_timer * 2 + i) * 10
            
            # Schwimmer-Farben
            colors = [SWIMMER_COLOR, OPPONENT_COLOR, arcade.color.GREEN]
            color = colors[i % len(colors)]
            
            # Mini-Schwimmer zeichnen
            arcade.draw_circle_filled(x, y, 8, color)
            arcade.draw_circle_filled(x, y + 3, 4, arcade.color.PINK)
            
            # Animierte Arme (vereinfacht)
            arm_angle = math.sin(self.animation_timer * 4 + i) * 0.5
            arm_x = x + math.cos(arm_angle) * 6
            arm_y = y + math.sin(arm_angle) * 3
            arcade.draw_line(x, y, arm_x, arm_y, color, 2)
    
    def _draw_texts(self):
        """Zeichnet alle Text-Elemente"""
        if self.title_text:
            # Animierter Titel
            self.title_text.y = SCREEN_HEIGHT - 150 + self.wave_offset
            self.title_text.draw()
            
            self.subtitle_text.draw()
            
            # Blinkender Start-Text
            if math.sin(self.animation_timer * 3) > 0:
                self.start_text.draw()
            
            self.controls_text.draw()
            self.credits_text.draw()
        else:
            # Fallback ohne Text-Objekte
            self._draw_texts_fallback()
    
    def _draw_texts_fallback(self):
        """Fallback für Text-Darstellung"""
        # Titel
        title_y = SCREEN_HEIGHT - 150 + self.wave_offset
        arcade.draw_text("SWIMMING GIM", SCREEN_WIDTH // 2, title_y,
                        arcade.color.WHITE, 48, anchor_x="center")
        
        # Untertitel
        arcade.draw_text("Das ultimative Schwimmrennen", 
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200,
                        arcade.color.LIGHT_BLUE, 20, anchor_x="center")
        
        # Blinkender Start-Text
        if math.sin(self.animation_timer * 3) > 0:
            arcade.draw_text("Drücke ENTER zum Starten", 
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                            arcade.color.YELLOW, 24, anchor_x="center")
        
        # Steuerung
        arcade.draw_text("LEERTASTE = Schwimmen  |  R = Neustart", 
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                        arcade.color.WHITE, 16, anchor_x="center")
        
        # Credits
        arcade.draw_text("Erstellt mit Python Arcade", 
                        SCREEN_WIDTH // 2, 50,
                        arcade.color.GRAY, 14, anchor_x="center")
    
    def _draw_sharks(self):
        """Zeichnet dekorative Haie"""
        for i in range(2):
            # Haie schwimmen langsam durch das Menü
            x = (self.animation_timer * 30 + i * 200) % (SCREEN_WIDTH + 100) - 50
            y = 200 + i * 150 + math.sin(self.animation_timer + i) * 20
            
            # Mini-Hai
            arcade.draw_ellipse_filled(x, y, 40, 15, arcade.color.DARK_GRAY)
            arcade.draw_triangle_filled(x - 15, y, x - 25, y + 8, x - 25, y - 8, 
                                      arcade.color.DARK_GRAY)
            
            # Zähne
            for j in range(2):
                tooth_x = x + 15
                tooth_y = y - 3 + j * 6
                arcade.draw_triangle_filled(tooth_x, tooth_y, 
                                          tooth_x + 3, tooth_y + 2,
                                          tooth_x + 3, tooth_y - 2,
                                          arcade.color.WHITE)
    
    def _draw_bubbles(self):
        """Zeichnet animierte Luftblasen"""
        for i in range(10):
            # Blasen steigen auf
            x = (i * 60 + self.animation_timer * 20) % SCREEN_WIDTH
            y = (self.animation_timer * 50 + i * 30) % SCREEN_HEIGHT
            size = 3 + math.sin(self.animation_timer * 2 + i) * 2
            
            # Transparente Blase
            bubble_color = (*arcade.color.LIGHT_BLUE[:3], 150)
            arcade.draw_circle_filled(x, y, max(1, size), bubble_color)
    
    def on_key_press(self, key, modifiers):
        """Behandelt Tasteneingaben"""
        if key == arcade.key.ENTER:
            # Wechsel zum Spiel
            from main import SwimmingGame  # Import hier um Zirkelbezug zu vermeiden
            game_view = SwimmingGame()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            # Spiel beenden
            self.window.close()

class PauseView(arcade.View):
    """Pause-Bildschirm"""
    
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        arcade.set_background_color((0, 0, 0, 150))  # Halbtransparent
    
    def on_draw(self):
        """Zeichnet den Pause-Bildschirm"""
        # Zeichne das Spiel im Hintergrund (eingefroren)
        self.game_view.on_draw()
        
        # Dunkle Überlagerung
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                                   SCREEN_WIDTH, SCREEN_HEIGHT, 
                                   (0, 0, 0, 150))
        
        # Pause-Text
        arcade.draw_text("PAUSE", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                        arcade.color.WHITE, 48, anchor_x="center")
        
        arcade.draw_text("Drücke P um fortzusetzen", 
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                        arcade.color.YELLOW, 20, anchor_x="center")
        
        arcade.draw_text("Drücke ESC für Hauptmenü", 
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                        arcade.color.WHITE, 16, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        """Behandelt Tasteneingaben im Pause-Menü"""
        if key == arcade.key.P:
            # Zurück zum Spiel
            self.window.show_view(self.game_view)
        elif key == arcade.key.ESCAPE:
            # Zurück zum Hauptmenü
            menu_view = MenuView()
            self.window.show_view(menu_view)

class GameOverView(arcade.View):
    """Game-Over-Bildschirm mit Statistiken"""
    
    def __init__(self, winner, player_strokes, survived_time):
        super().__init__()
        arcade.set_background_color(BACKGROUND_COLOR)
        
        self.winner = winner
        self.player_strokes = player_strokes
        self.survived_time = survived_time
        self.animation_timer = 0
    
    def on_update(self, delta_time):
        """Update für Animationen"""
        self.animation_timer += delta_time
    
    def on_draw(self):
        """Zeichnet den Game-Over-Bildschirm"""
        self.clear()
        
        # Hintergrund-Effekt
        self._draw_background_effect()
        
        # Titel
        if self.winner is None:
            title = "GAME OVER"
            subtitle = "Du wurdest gefressen!"
            title_color = arcade.color.RED
        elif self.winner.is_player:
            title = "SIEG!"
            subtitle = "Du hast gewonnen!"
            title_color = arcade.color.GREEN
        else:
            title = "NIEDERLAGE"
            subtitle = "Besser beim nächsten Mal!"
            title_color = arcade.color.ORANGE
        
        # Animierter Titel
        title_y = SCREEN_HEIGHT - 150 + math.sin(self.animation_timer * 2) * 10
        arcade.draw_text(title, SCREEN_WIDTH // 2, title_y,
                        title_color, 48, anchor_x="center")
        
        arcade.draw_text(subtitle, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200,
                        arcade.color.WHITE, 24, anchor_x="center")
        
        # Statistiken
        self._draw_statistics()
        
        # Optionen
        arcade.draw_text("R - Nochmal spielen", SCREEN_WIDTH // 2, 120,
                        arcade.color.YELLOW, 20, anchor_x="center")
        
        arcade.draw_text("ESC - Hauptmenü", SCREEN_WIDTH // 2, 80,
                        arcade.color.WHITE, 18, anchor_x="center")
    
    def _draw_background_effect(self):
        """Zeichnet Hintergrund-Effekt je nach Ergebnis"""
        if self.winner is None:
            # Hai-Silhouetten für Game Over
            for i in range(3):
                x = SCREEN_WIDTH // 2 + math.sin(self.animation_timer + i) * 100
                y = SCREEN_HEIGHT // 2 + math.cos(self.animation_timer * 0.5 + i) * 50
                arcade.draw_ellipse_filled(x, y, 60, 20, (100, 100, 100, 100))
        elif self.winner.is_player:
            # Goldene Partikel für Sieg
            for i in range(20):
                x = (i * 30 + self.animation_timer * 50) % SCREEN_WIDTH
                y = SCREEN_HEIGHT // 2 + math.sin(self.animation_timer * 3 + i) * 100
                size = 3 + math.sin(self.animation_timer * 4 + i) * 2
                arcade.draw_circle_filled(x, y, size, arcade.color.GOLD)
    
    def _draw_statistics(self):
        """Zeichnet Spiel-Statistiken"""
        stats_y = SCREEN_HEIGHT // 2
        
        arcade.draw_text("STATISTIKEN", SCREEN_WIDTH // 2, stats_y + 50,
                        arcade.color.CYAN, 20, anchor_x="center")
        
        arcade.draw_text(f"Schwimmzüge: {self.player_strokes}", 
                        SCREEN_WIDTH // 2, stats_y,
                        arcade.color.WHITE, 16, anchor_x="center")
        
        arcade.draw_text(f"Überlebenszeit: {self.survived_time:.1f}s", 
                        SCREEN_WIDTH // 2, stats_y - 30,
                        arcade.color.WHITE, 16, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        """Behandelt Tasteneingaben"""
        if key == arcade.key.R:
            # Neues Spiel
            from main import SwimmingGame
            game_view = SwimmingGame()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            # Hauptmenü
            menu_view = MenuView()
            self.window.show_view(menu_view)
            