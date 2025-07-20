# main.py - Optimierte Hauptdatei mit Menü-System
import arcade
import time
from config import *
from swimmer import Swimmer
from dangers import DangerManager
from ui import GameUI, LaneRenderer

class SwimmingGame(arcade.View):
    """Hauptspiel-Klasse"""
    
    def __init__(self):
        super().__init__()
        arcade.set_background_color(BACKGROUND_COLOR)
        
        # Komponenten initialisieren
        self.swimmers = []
        self.player = None
        self.danger_manager = DangerManager()
        self.ui = GameUI()
        
        # Spiel-Status
        self.game_finished = False
        self.winner = None
        self.start_time = time.time()
        
        # Spiel initialisieren
        self._initialize_swimmers()
    
    def _initialize_swimmers(self):
        """Initialisiert alle Schwimmer"""
        self.swimmers = []
        
        # Spieler in der 4. Bahn von links
        player_lane = 3
        player_x = player_lane * LANE_WIDTH + LANE_WIDTH // 2
        player_y = 50
        self.player = Swimmer(player_x, player_y, player_lane, is_player=True)
        self.swimmers.append(self.player)
        
        # KI-Gegner in den anderen Bahnen
        for lane in range(LANE_COUNT):
            if lane != player_lane:
                opponent_x = lane * LANE_WIDTH + LANE_WIDTH // 2
                opponent_y = 50
                opponent = Swimmer(opponent_x, opponent_y, lane, is_player=False)
                self.swimmers.append(opponent)
    
    def on_update(self, delta_time):
        """Update-Methode für Spiellogik"""
        if not self.game_finished:
            self._update_swimmers(delta_time)
            
            # Prüfe Game-Over-Bedingungen
            if self._check_game_conditions():
                self._handle_game_over()
            
            self.danger_manager.update(delta_time, self.swimmers)
        
        # UI immer updaten
        self.ui.update_texts(self.player, self.game_finished, self.winner)
    
    def _update_swimmers(self, delta_time):
        """Update aller Schwimmer"""
        for swimmer in self.swimmers:
            swimmer.update(delta_time)
    
    def _check_game_conditions(self):
        """Prüft Gewinn-/Verlust-Bedingungen"""
        # Zielbereich erreicht
        for swimmer in self.swimmers:
            if swimmer.y >= SCREEN_HEIGHT - 70:
                self.game_finished = True
                self.winner = swimmer
                return True
        
        # Spieler gefressen
        if not self.player.active:
            self.game_finished = True
            self.winner = None
            return True
        
        return False
    
    def _handle_game_over(self):
        """Behandelt Game-Over"""
        # Berechne Statistiken
        survived_time = time.time() - self.start_time
        
        # Wechsel zum Game-Over-Bildschirm nach kurzer Verzögerung
        def show_game_over():
            from menu import GameOverView
            game_over_view = GameOverView(
                self.winner, 
                self.player.strokes, 
                survived_time
            )
            self.window.show_view(game_over_view)
        
        # Verzögerung für dramatischen Effekt
        arcade.schedule(show_game_over, 2.0)
    
    def on_draw(self):
        """Zeichnet das komplette Spiel"""
        self.clear()
        
        # Spielfeld zeichnen
        LaneRenderer.draw_lanes()
        self.ui.draw_lane_numbers()
        
        # Spielelemente zeichnen
        self._draw_swimmers()
        self.danger_manager.draw_all()
        
        # UI zeichnen
        self.ui.draw_stamina_bar(self.player)
        
        # Game-Over-Text nur wenn Spiel beendet (vor automatischem Wechsel)
        if self.game_finished:
            self.ui.draw_game_over(self.game_finished, self.winner)
    
    def _draw_swimmers(self):
        """Zeichnet alle Schwimmer"""
        for swimmer in self.swimmers:
            swimmer.draw()
    
    def on_key_press(self, key, modifiers):
        """Behandelt Tasteneingaben"""
        if key == arcade.key.SPACE and not self.game_finished:
            self.player.swim_stroke()
        elif key == arcade.key.R and self.game_finished:
            self.restart_game()
        elif key == arcade.key.P and not self.game_finished:
            # Pause
            from menu import PauseView
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        elif key == arcade.key.ESCAPE:
            # Zurück zum Hauptmenü
            from menu import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)
    
    def restart_game(self):
        """Startet das Spiel neu"""
        self._initialize_swimmers()
        self.danger_manager.reset()
        self.game_finished = False
        self.winner = None
        self.start_time = time.time()

class GameManager:
    """Manager für das gesamte Spiel"""
    
    def __init__(self):
        self.window = None
    
    def start_game(self):
        """Startet das Spiel mit Hauptmenü"""
        self.window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Starte mit dem Hauptmenü
        from menu import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
        
        arcade.run()

def main():
    """Hauptfunktion"""
    game_manager = GameManager()
    game_manager.start_game()

if __name__ == "__main__":
    main()
    