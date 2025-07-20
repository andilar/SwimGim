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

# Gefahren-Einstellungen
SHARK_SPEED = 80  # Hai-Geschwindigkeit (Pixel pro Sekunde)
SHARK_SPAWN_MIN = 5.0  # Minimum Sekunden zwischen Hai-Spawns
SHARK_SPAWN_MAX = 15.0  # Maximum Sekunden zwischen Hai-Spawns
SHARK_SIZE = 30  # Größe des Hais

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
        self.active = True  # Schwimmer ist aktiv
        
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
        # Zeichne nur aktive Schwimmer
        if not self.active:
            return
            
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

class Danger:
    """Basisklasse für alle Gefahren"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True
        
    def update(self, delta_time, swimmers):
        """Update-Methode für Gefahren"""
        pass
        
    def draw(self):
        """Zeichnet die Gefahr"""
        pass

class Shark(Danger):
    """Hai-Klasse - schwimmt von der Seite rein und verfolgt Schwimmer"""
    def __init__(self, target_swimmer):
        # Starte von einer zufälligen Seite
        from_left = random.choice([True, False])
        start_x = -SHARK_SIZE if from_left else SCREEN_WIDTH + SHARK_SIZE
        start_y = target_swimmer.y
        
        super().__init__(start_x, start_y)
        self.target = target_swimmer
        self.from_left = from_left
        self.has_caught = False
        self.is_diving = False
        self.dive_timer = 0
        self.dive_duration = 2.0  # Sekunden zum Abtauchen
        
    def update(self, delta_time, swimmers):
        """Hai bewegt sich auf Ziel zu oder taucht ab"""
        if not self.active:
            return
            
        if self.is_diving:
            # Hai taucht ab
            self.dive_timer += delta_time
            self.y -= 100 * delta_time  # Taucht nach unten ab
            
            # Entferne Hai nach Abtauch-Zeit oder wenn er unten ist
            if self.dive_timer >= self.dive_duration or self.y < 30:
                self.active = False
            return
            
        if self.has_caught:
            return
            
        # Normale Hai-Bewegung
        if self.from_left:
            self.x += SHARK_SPEED * delta_time
        else:
            self.x -= SHARK_SPEED * delta_time
            
        # Verfolge den Schwimmer auch vertikal (langsamer)
        if self.target.y > self.y:
            self.y += SHARK_SPEED * 0.3 * delta_time
        elif self.target.y < self.y:
            self.y -= SHARK_SPEED * 0.3 * delta_time
            
        # Prüfe Kollision mit Ziel-Schwimmer
        distance = ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2) ** 0.5
        if distance < SHARK_SIZE and not self.has_caught:
            self.catch_swimmer()
            
        # Entferne Hai wenn er den Bildschirm verlassen hat (ohne zu fangen)
        if (self.from_left and self.x > SCREEN_WIDTH + SHARK_SIZE) or \
           (not self.from_left and self.x < -SHARK_SIZE):
            self.active = False
            
    def catch_swimmer(self):
        """Hai fängt Schwimmer und beginnt abzutauchen"""
        self.has_caught = True
        self.is_diving = True
        self.dive_timer = 0
        
        # Schwimmer wird aus dem Spiel entfernt (gefressen)
        if self.target.is_player:
            # Spieler wurde gefressen - Spiel vorbei
            self.target.y = -100  # Verstecke unter dem Spielfeld
            self.target.active = False  # Markiere als inaktiv
        else:
            # KI-Gegner wird komplett entfernt
            self.target.y = -100  # Verstecke unter dem Spielfeld
            self.target.active = False  # Markiere als inaktiv
        
    def draw(self):
        """Zeichnet den Hai"""
        if not self.active:
            return
            
        # Transparenz während des Abtauchens
        alpha = 255
        if self.is_diving:
            alpha = int(255 * (1 - self.dive_timer / self.dive_duration))
            alpha = max(50, alpha)  # Mindest-Transparenz
            
        # Hai-Körper (grau) - mit Transparenz
        body_color = (*arcade.color.DARK_GRAY[:3], alpha)
        arcade.draw_ellipse_filled(self.x, self.y, SHARK_SIZE * 1.5, SHARK_SIZE // 2, body_color)
        
        # Hai-Kopf (dunkler) - in Bewegungsrichtung
        head_x = self.x + (SHARK_SIZE//3 if self.from_left else -SHARK_SIZE//3)
        head_color = (*arcade.color.GRAY[:3], alpha)
        arcade.draw_ellipse_filled(head_x, self.y, SHARK_SIZE//2, SHARK_SIZE//3, head_color)
        
        # Zähne (weiß) - zeigen in Bewegungsrichtung
        tooth_color = (*arcade.color.WHITE[:3], alpha)
        for i in range(3):
            tooth_x = head_x + (5 if self.from_left else -5)
            tooth_y = self.y - 5 + i * 5
            arcade.draw_triangle_filled(tooth_x, tooth_y, 
                                      tooth_x + (3 if self.from_left else -3), tooth_y + 3,
                                      tooth_x + (3 if self.from_left else -3), tooth_y - 3,
                                      tooth_color)
        
        # Hai-Schwanzflosse - hinten am Körper
        fin_x = self.x + (-SHARK_SIZE//2 if self.from_left else SHARK_SIZE//2)
        fin_color = (*arcade.color.DARK_GRAY[:3], alpha)
        arcade.draw_triangle_filled(fin_x, self.y,
                                  fin_x + (-SHARK_SIZE//3 if self.from_left else SHARK_SIZE//3), self.y + SHARK_SIZE//4,
                                  fin_x + (-SHARK_SIZE//3 if self.from_left else SHARK_SIZE//3), self.y - SHARK_SIZE//4,
                                  fin_color)
        
        # Luftblasen während des Abtauchens
        if self.is_diving:
            import time
            for i in range(3):
                bubble_x = self.x + random.randint(-10, 10)
                bubble_y = self.y + 20 + i * 8
                bubble_size = random.randint(2, 5)
                arcade.draw_circle_filled(bubble_x, bubble_y, bubble_size, arcade.color.LIGHT_BLUE)

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
        
        # Gefahren zurücksetzen
        self.dangers = []
        self.shark_spawn_timer = 0
        self.next_shark_spawn = random.uniform(SHARK_SPAWN_MIN, SHARK_SPAWN_MAX)
        
        # Gefahren-System
        self.dangers = []
        self.shark_spawn_timer = 0
        self.next_shark_spawn = random.uniform(SHARK_SPAWN_MIN, SHARK_SPAWN_MAX)
        
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
                    
            # Prüfen ob der Spieler noch aktiv ist (nicht gefressen)
            if not self.player.active:
                self.game_finished = True
                self.winner = None  # Kein Gewinner - Spieler wurde gefressen
                    
            # Gefahren-System updaten
            self.update_dangers(delta_time)
            
            # Text-Updates für bessere Performance
            self.update_text_objects()
    
    def update_text_objects(self):
        """Update alle Text-Objekte"""
        # Prüfe ob Text-Objekte existieren
        if not hasattr(self, 'stamina_text'):
            return
            
        # Ausdauer-Texte
        self.stamina_text.text = f"Ausdauer: {self.player.stamina_float:.1f}/{MAX_STAMINA}"
        self.regen_text.text = f"Regeneration: +{STAMINA_RECOVERY_RATE}/s"
        
        # Gewinn-Texte
        if self.game_finished:
            if self.winner is None:
                # Spieler wurde gefressen
                self.win_text.text = "Du wurdest gefressen!"
                self.win_text.color = arcade.color.RED
            elif self.winner.is_player:
                self.win_text.text = "Du hast gewonnen!"
                self.win_text.color = arcade.color.GREEN
            else:
                self.win_text.text = "Du hast verloren!"
                self.win_text.color = arcade.color.RED
            self.restart_text.text = "Drücke R zum Neustarten"
    
    def update_dangers(self, delta_time):
        """Update für alle Gefahren"""
        # Hai-Spawn Timer
        self.shark_spawn_timer += delta_time
        if self.shark_spawn_timer >= self.next_shark_spawn:
            self.spawn_shark()
            self.shark_spawn_timer = 0
            self.next_shark_spawn = random.uniform(SHARK_SPAWN_MIN, SHARK_SPAWN_MAX)
            
        # Update alle aktiven Gefahren
        for danger in self.dangers[:]:  # Copy list to avoid modification during iteration
            danger.update(delta_time, self.swimmers)
            if not danger.active:
                self.dangers.remove(danger)
                
    def spawn_shark(self):
        """Spawnt einen neuen Hai"""
        # Wähle zufälligen Schwimmer als Ziel (bevorzuge Schwimmer weiter oben)
        active_swimmers = [s for s in self.swimmers if s.y > 100 and s.active]  # Nur aktive Schwimmer die schon etwas geschwommen sind
        if active_swimmers:
            # Wahrscheinlichkeit basierend auf Position - weiter vorne = wahrscheinlicher
            weights = [s.y for s in active_swimmers]
            target = random.choices(active_swimmers, weights=weights)[0]
            shark = Shark(target)
            self.dangers.append(shark)
    
    def on_draw(self):
        """Zeichnet das Spiel"""
        self.clear()
        
        # Schwimmbahnen zeichnen
        self.draw_lanes()
        
        # Alle Schwimmer zeichnen
        for swimmer in self.swimmers:
            swimmer.draw()
            
        # Alle Gefahren zeichnen
        for danger in self.dangers:
            danger.draw()
        
        # UI-Informationen zeichnen
        self.draw_ui()
        
        # Gewinn-Nachricht anzeigen
        if self.game_finished:
            if hasattr(self, 'win_text'):
                self.win_text.draw()
                self.restart_text.draw()
            else:
                # Fallback für Gewinn-Nachrichten
                if self.winner is None:
                    # Spieler wurde gefressen
                    arcade.draw_text("Du wurdest gefressen!", 
                                   SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                                   arcade.color.RED, 24, anchor_x="center")
                elif self.winner.is_player:
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
        
        # Bahnnummern mit Text-Objekten (falls vorhanden)
        if hasattr(self, 'lane_numbers'):
            for lane_text in self.lane_numbers:
                lane_text.draw()
        else:
            # Fallback: normale Text-Darstellung
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
        
        # Ausdauer-Text über dem Balken - mit Text-Objekt (falls vorhanden)
        if hasattr(self, 'stamina_text'):
            self.stamina_text.draw()
        else:
            arcade.draw_text(f"Ausdauer: {self.player.stamina_float:.1f}/{MAX_STAMINA}", 
                            bar_x, bar_y + 18, arcade.color.WHITE, 16)
        
        # Regenerations-Rate unter dem Balken - mit Text-Objekt (falls vorhanden)
        if hasattr(self, 'regen_text'):
            self.regen_text.draw()
        else:
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
    