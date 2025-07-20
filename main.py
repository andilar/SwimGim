import arcade
import arcade.gui
import random

# Konstanten
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Swimming Gim"

# Farben
WATER_COLOR = arcade.color.LIGHT_BLUE
LANE_COLOR = arcade.color.DARK_BLUE
SWIMMER_COLOR = arcade.color.RED
OPPONENT_COLOR = arcade.color.BLUE
BACKGROUND_COLOR = arcade.color.SKY_BLUE

# Schwimmbahn-Einstellungen
LANE_COUNT = 8
LANE_WIDTH = SCREEN_WIDTH // LANE_COUNT
LANE_HEIGHT = SCREEN_HEIGHT - 100

# Schwimmer-Einstellungen
SWIMMER_SIZE = 20
SWIMMER_SPEED = 30  # Pixel pro Schwimmzug
CURRENT_INTERVAL = 1.0  # Sekunden zwischen Gegenstrom-Schüben
CURRENT_PUSHBACK = 15  # Halbe Schwimmzuglänge (SWIMMER_SPEED / 2)

# Ausdauer-Einstellungen
MAX_STAMINA = 5  # Maximale Ausdauer (Schwimmzüge)
STAMINA_RECOVERY_RATE = 1.5  # Ausdauer-Punkte pro Sekunde

class Swimmer:
    def __init__(self, x, y, lane, is_player=True):
        self.x = x
        self.y = y
        self.lane = lane
        self.strokes = 0  # Anzahl der Schwimmzüge
        self.is_player = is_player
        self.swim_timer = 0  # Timer für automatisches Schwimmen
        self.swim_speed = random.uniform(0.8, 1.2) if not is_player else 1.0  # Verschiedene Geschwindigkeiten
        self.current_timer = 0  # Timer für Gegenstrom
        self.animation_timer = 0  # Timer für Schwimmanimation
        self.stroke_phase = 0  # Phase der Schwimmbewegung (0-1)
        
        # Ausdauer nur für Spieler
        if self.is_player:
            self.stamina = MAX_STAMINA
            # Kontinuierliche Ausdauer als Float für flüssige Regeneration
            self.stamina_float = float(MAX_STAMINA)
        
    def swim_stroke(self):
        """Führt einen Schwimmzug aus"""
        if self.is_player:
            # Prüfe Ausdauer für Spieler (mindestens 1 Punkt nötig)
            if self.stamina_float >= 1.0:
                self.y += SWIMMER_SPEED
                self.strokes += 1
                self.stamina_float -= 1.0
                self.stamina = int(self.stamina_float)  # Update integer version
            # Wenn keine Ausdauer, passiert nichts
        else:
            # KI-Gegner haben unbegrenzte Ausdauer
            self.y += SWIMMER_SPEED
            self.strokes += 1
        
    def apply_current(self):
        """Wendet Gegenstrom an - schiebt zurück"""
        self.y -= CURRENT_PUSHBACK
        # Schwimmer kann nicht unter die Startlinie fallen
        if self.y < 50:
            self.y = 50
        
    def update(self, delta_time):
        """Update für KI-Schwimmer"""
        # Animation der Schwimmbewegung
        self.animation_timer += delta_time * 3  # Geschwindigkeit der Animation
        self.stroke_phase = (self.animation_timer % 2.0) / 2.0  # 0-1 Zyklus
        
        # Kontinuierliche Ausdauer-Erholung für Spieler
        if self.is_player and self.stamina_float < MAX_STAMINA:
            self.stamina_float += STAMINA_RECOVERY_RATE * delta_time
            # Begrenze auf Maximum
            if self.stamina_float > MAX_STAMINA:
                self.stamina_float = MAX_STAMINA
            self.stamina = int(self.stamina_float)  # Update integer version
        
        # Gegenstrom-Timer für alle Schwimmer
        self.current_timer += delta_time
        if self.current_timer >= CURRENT_INTERVAL:
            self.apply_current()
            self.current_timer = 0
        
        if not self.is_player and self.y < SCREEN_HEIGHT - 70:
            self.swim_timer += delta_time
            # Gegner schwimmen automatisch mit unterschiedlichen Geschwindigkeiten
            if self.swim_timer >= (1.0 / self.swim_speed):
                self.swim_stroke()
                self.swim_timer = 0
        
    def draw(self):
        """Zeichnet den Schwimmer mit animierten Armen und Beinen"""
        color = SWIMMER_COLOR if self.is_player else OPPONENT_COLOR
        head_color = arcade.color.PINK if self.is_player else arcade.color.LIGHT_GRAY
        
        # Körper (Oval)
        arcade.draw_ellipse_filled(self.x, self.y, SWIMMER_SIZE, SWIMMER_SIZE//2, color)
        
        # Kopf
        arcade.draw_circle_filled(self.x, self.y + 5, SWIMMER_SIZE//4, head_color)
        
        # Berechne Arm-Positionen basierend auf Animation
        import math
        
        # Linker Arm (wechselt zwischen vor und zurück)
        left_arm_angle = math.sin(self.stroke_phase * math.pi * 2) * 0.8
        left_arm_x = self.x - 8 + math.cos(left_arm_angle) * 10
        left_arm_y = self.y + math.sin(left_arm_angle) * 5
        
        # Rechter Arm (um 180° phasenverschoben)
        right_arm_angle = math.sin((self.stroke_phase + 0.5) * math.pi * 2) * 0.8
        right_arm_x = self.x + 8 + math.cos(right_arm_angle) * 10
        right_arm_y = self.y + math.sin(right_arm_angle) * 5
        
        # Arme zeichnen
        arcade.draw_line(self.x - 5, self.y, left_arm_x, left_arm_y, color, 3)
        arcade.draw_line(self.x + 5, self.y, right_arm_x, right_arm_y, color, 3)
        
        # Hände
        arcade.draw_circle_filled(left_arm_x, left_arm_y, 2, color)
        arcade.draw_circle_filled(right_arm_x, right_arm_y, 2, color)
        
        # Beine (alternierend kickend)
        leg_kick = math.sin(self.stroke_phase * math.pi * 4) * 0.3  # Schnellere Beinbewegung
        
        # Linkes Bein
        left_leg_x = self.x - 3 + math.cos(leg_kick) * 6
        left_leg_y = self.y - 8 + math.sin(leg_kick) * 3
        
        # Rechtes Bein (phasenverschoben)
        right_leg_x = self.x + 3 + math.cos(leg_kick + math.pi) * 6
        right_leg_y = self.y - 8 + math.sin(leg_kick + math.pi) * 3
        
        # Beine zeichnen
        arcade.draw_line(self.x - 3, self.y - 5, left_leg_x, left_leg_y, color, 3)
        arcade.draw_line(self.x + 3, self.y - 5, right_leg_x, right_leg_y, color, 3)
        
        # Füße
        arcade.draw_circle_filled(left_leg_x, left_leg_y, 2, color)
        arcade.draw_circle_filled(right_leg_x, right_leg_y, 2, color)

class SwimmingGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(BACKGROUND_COLOR)
        
        # Alle Schwimmer initialisieren
        self.swimmers = []
        
        # Spieler-Schwimmer in der 4. Bahn von links
        player_lane = 3
        player_x = player_lane * LANE_WIDTH + LANE_WIDTH // 2
        player_y = 50
        self.player = Swimmer(player_x, player_y, player_lane, is_player=True)
        self.swimmers.append(self.player)
        
        # Gegner in den anderen Bahnen
        for lane in range(LANE_COUNT):
            if lane != player_lane:  # Nicht in der Spieler-Bahn
                opponent_x = lane * LANE_WIDTH + LANE_WIDTH // 2
                opponent_y = 50
                opponent = Swimmer(opponent_x, opponent_y, lane, is_player=False)
                self.swimmers.append(opponent)
        
        self.game_finished = False
        self.winner = None
        
    def on_update(self, delta_time):
        """Update-Methode für Animationen"""
        if not self.game_finished:
            # Alle Schwimmer updaten
            for swimmer in self.swimmers:
                swimmer.update(delta_time)
                
                # Prüfen ob jemand das Ziel erreicht hat
                if swimmer.y >= SCREEN_HEIGHT - 70:
                    self.game_finished = True
                    self.winner = swimmer
    
    def on_draw(self):
        """Zeichnet das Spiel"""
        self.clear()
        
        # Schwimmbahnen zeichnen
        self.draw_lanes()
        
        # Alle Schwimmer zeichnen
        for swimmer in self.swimmers:
            swimmer.draw()
        
        # UI-Informationen zeichnen
        self.draw_ui()
        
        # Gewinn-Nachricht anzeigen
        if self.game_finished:
            if self.winner.is_player:
                arcade.draw_text("Du hast gewonnen!", 
                               SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                               arcade.color.GREEN, 24, anchor_x="center")
            else:
                arcade.draw_text("Du hast verloren!", 
                               SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                               arcade.color.RED, 24, anchor_x="center")
            arcade.draw_text("Drücke R zum Neustarten", 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                           arcade.color.WHITE, 20, anchor_x="center")
    
    def draw_lanes(self):
        """Zeichnet die 8 Schwimmbahnen"""
        # Wasser-Hintergrund
        water_rect = arcade.XYWH(0, 50, SCREEN_WIDTH, LANE_HEIGHT)
        arcade.draw_rect_filled(water_rect, WATER_COLOR)
        
        # Bahnlinien zeichnen (vertikal)
        for i in range(LANE_COUNT + 1):
            x = i * LANE_WIDTH
            arcade.draw_line(x, 50, x, SCREEN_HEIGHT - 50, LANE_COLOR, 3)
        
        # Obere und untere Begrenzungen
        arcade.draw_line(0, 50, SCREEN_WIDTH, 50, LANE_COLOR, 5)
        arcade.draw_line(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, SCREEN_HEIGHT - 50, LANE_COLOR, 5)
        
        # Zielbereich markieren (oben)
        goal_y = SCREEN_HEIGHT - 70
        arcade.draw_line(0, goal_y, SCREEN_WIDTH, goal_y, arcade.color.YELLOW, 4)
        
        # Bahnnummern
        for i in range(LANE_COUNT):
            x = i * LANE_WIDTH + LANE_WIDTH // 2
            arcade.draw_text(f"{i+1}", x - 10, 25, arcade.color.WHITE, 16)
    
    def draw_ui(self):
        """Zeichnet die Benutzeroberfläche"""
        # Nur noch der Ausdauerbalken
        self.draw_stamina_bar()
    
    def draw_stamina_bar(self):
        """Zeichnet den Ausdauerbalken"""
        bar_x = 10
        bar_y = SCREEN_HEIGHT - 65  # Mehr Abstand vom oberen Text
        bar_width = 250  # Breiterer Balken
        bar_height = 25  # Höherer Balken
        
        # Schwarzer Hintergrund für bessere Lesbarkeit
        shadow_rect = arcade.XYWH(bar_x - 2, bar_y - bar_height//2 - 2, bar_width + 4, bar_height + 4)
        arcade.draw_rect_filled(shadow_rect, arcade.color.BLACK)
        
        # Hintergrund-Rechteck (dunkelgrau)
        background_rect = arcade.XYWH(bar_x, bar_y - bar_height//2, bar_width, bar_height)
        arcade.draw_rect_filled(background_rect, arcade.color.DARK_GRAY)
        
        # Rahmen (weiß, dicker)
        arcade.draw_rect_outline(background_rect, arcade.color.WHITE, 3)
        
        # Ausdauer-Balken (grün bis rot je nach Level)
        if self.player.stamina_float > 0:
            stamina_percentage = self.player.stamina_float / MAX_STAMINA
            stamina_width = (bar_width - 6) * stamina_percentage
            
            # Farbe basierend auf Ausdauer
            if stamina_percentage > 0.6:
                color = arcade.color.GREEN
            elif stamina_percentage > 0.2:
                color = arcade.color.ORANGE  # Besser sichtbar als Gelb
            else:
                color = arcade.color.RED
            
            stamina_rect = arcade.XYWH(bar_x + 3, bar_y - bar_height//2 + 3, stamina_width, bar_height - 6)
            arcade.draw_rect_filled(stamina_rect, color)
        
        # Ausdauer-Text über dem Balken
        arcade.draw_text(f"Ausdauer: {self.player.stamina_float:.1f}/{MAX_STAMINA}", 
                        bar_x, bar_y + 18, arcade.color.WHITE, 16)
        
        # Regenerations-Rate unter dem Balken
        arcade.draw_text(f"Regeneration: +{STAMINA_RECOVERY_RATE}/s", 
                        bar_x, bar_y - 22, arcade.color.CYAN, 14)
    
    def on_key_press(self, key, modifiers):
        """Behandelt Tasteneingaben"""
        if key == arcade.key.SPACE and not self.game_finished:
            # Schwimmzug ausführen
            self.player.swim_stroke()
                
        elif key == arcade.key.R and self.game_finished:
            # Spiel neustarten
            self.restart_game()
    
    def restart_game(self):
        """Startet das Spiel neu"""
        # Alle Schwimmer zurücksetzen
        self.swimmers = []
        
        # Spieler-Schwimmer in der 4. Bahn von links
        player_lane = 3
        player_x = player_lane * LANE_WIDTH + LANE_WIDTH // 2
        player_y = 50
        self.player = Swimmer(player_x, player_y, player_lane, is_player=True)
        self.swimmers.append(self.player)
        
        # Gegner in den anderen Bahnen
        for lane in range(LANE_COUNT):
            if lane != player_lane:  # Nicht in der Spieler-Bahn
                opponent_x = lane * LANE_WIDTH + LANE_WIDTH // 2
                opponent_y = 50
                opponent = Swimmer(opponent_x, opponent_y, lane, is_player=False)
                self.swimmers.append(opponent)
        
        self.game_finished = False
        self.winner = None

def main():
    """Hauptfunktion"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = SwimmingGame()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()