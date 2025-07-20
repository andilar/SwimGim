import arcade
import arcade.gui

# Konstanten
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Swimming Gim"

# Farben
WATER_COLOR = arcade.color.LIGHT_BLUE
LANE_COLOR = arcade.color.DARK_BLUE
SWIMMER_COLOR = arcade.color.RED
BACKGROUND_COLOR = arcade.color.SKY_BLUE

# Schwimmbahn-Einstellungen
LANE_COUNT = 8
LANE_HEIGHT = SCREEN_HEIGHT // LANE_COUNT
LANE_WIDTH = SCREEN_WIDTH - 100

# Schwimmer-Einstellungen
SWIMMER_SIZE = 20
SWIMMER_SPEED = 30  # Pixel pro Schwimmzug

class Swimmer:
    def __init__(self, x, y, lane):
        self.x = x
        self.y = y
        self.lane = lane
        self.strokes = 0  # Anzahl der Schwimmzüge
        
    def swim_stroke(self):
        """Führt einen Schwimmzug aus"""
        self.x += SWIMMER_SPEED
        self.strokes += 1
        
    def draw(self):
        """Zeichnet den Schwimmer"""
        arcade.draw_circle_filled(self.x, self.y, SWIMMER_SIZE//2, SWIMMER_COLOR)
        # Schwimmer-Details (Kopf und Körper)
        arcade.draw_circle_filled(self.x, self.y, SWIMMER_SIZE//3, arcade.color.PINK)

class SwimmingGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(BACKGROUND_COLOR)
        
        # Schwimmer initialisieren (startet in der 4. Bahn von links)
        start_x = 50
        start_lane = 3  # 4. Bahn von links (0-indexiert)
        start_y = SCREEN_HEIGHT - (start_lane * LANE_HEIGHT) - LANE_HEIGHT // 2
        
        self.swimmer = Swimmer(start_x, start_y, start_lane)
        self.game_finished = False
        
    def on_draw(self):
        """Zeichnet das Spiel"""
        self.clear()
        
        # Schwimmbahnen zeichnen
        self.draw_lanes()
        
        # Schwimmer zeichnen
        self.swimmer.draw()
        
        # UI-Informationen zeichnen
        self.draw_ui()
        
        # Gewinn-Nachricht anzeigen
        if self.game_finished:
            arcade.draw_text("Ziel erreicht! Drücke R zum Neustarten", 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                           arcade.color.RED, 30, anchor_x="center")
    
    def draw_lanes(self):
        """Zeichnet die 8 Schwimmbahnen"""
        # Wasser-Hintergrund
        water_rect = arcade.XYWH(50, 0, LANE_WIDTH, SCREEN_HEIGHT)
        arcade.draw_rect_filled(water_rect, WATER_COLOR)
        
        # Bahnlinien zeichnen
        for i in range(LANE_COUNT + 1):
            y = i * LANE_HEIGHT
            arcade.draw_line(50, y, SCREEN_WIDTH - 50, y, LANE_COLOR, 3)
        
        # Seitliche Begrenzungen
        arcade.draw_line(50, 0, 50, SCREEN_HEIGHT, LANE_COLOR, 5)
        arcade.draw_line(SCREEN_WIDTH - 50, 0, SCREEN_WIDTH - 50, SCREEN_HEIGHT, LANE_COLOR, 5)
        
        # Zielbereich markieren
        goal_x = SCREEN_WIDTH - 70
        arcade.draw_line(goal_x, 0, goal_x, SCREEN_HEIGHT, arcade.color.YELLOW, 4)
        
        # Bahnnummern
        for i in range(LANE_COUNT):
            y = SCREEN_HEIGHT - (i * LANE_HEIGHT) - LANE_HEIGHT // 2
            arcade.draw_text(f"{i+1}", 25, y - 10, arcade.color.WHITE, 16)
    
    def draw_ui(self):
        """Zeichnet die Benutzeroberfläche"""
        # Schwimmzug-Zähler
        arcade.draw_text(f"Schwimmzüge: {self.swimmer.strokes}", 
                        10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18)
        
        # Anweisungen
        arcade.draw_text("Drücke LEERTASTE zum Schwimmen", 
                        10, SCREEN_HEIGHT - 55, arcade.color.WHITE, 14)
        
        # Bahn-Anzeige
        arcade.draw_text(f"Bahn: {self.swimmer.lane + 1}", 
                        10, SCREEN_HEIGHT - 80, arcade.color.WHITE, 14)
    
    def on_key_press(self, key, modifiers):
        """Behandelt Tasteneingaben"""
        if key == arcade.key.SPACE and not self.game_finished:
            # Schwimmzug ausführen
            self.swimmer.swim_stroke()
            
            # Prüfen ob Ziel erreicht
            if self.swimmer.x >= SCREEN_WIDTH - 70:
                self.game_finished = True
                
        elif key == arcade.key.R and self.game_finished:
            # Spiel neustarten
            self.restart_game()
    
    def restart_game(self):
        """Startet das Spiel neu"""
        start_x = 50
        start_lane = 3  # 4. Bahn von links
        start_y = SCREEN_HEIGHT - (start_lane * LANE_HEIGHT) - LANE_HEIGHT // 2
        
        self.swimmer = Swimmer(start_x, start_y, start_lane)
        self.game_finished = False

def main():
    """Hauptfunktion"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = SwimmingGame()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
    