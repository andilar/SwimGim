# main.py - Optimierte Hauptdatei
import arcade
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
            self._check_game_conditions()
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
                return
        
        # Spieler gefressen
        if not self.player.active:
            self.game_finished = True
            self.winner = None
    
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
    
    def restart_game(self):
        """Startet das Spiel neu"""
        self._initialize_swimmers()
        self.danger_manager.reset()
        self.game_finished = False
        self.winner = None

class GameManager:
    """Manager für das gesamte Spiel"""
    
    def __init__(self):
        self.window = None
        self.game_view = None
    
    def start_game(self):
        """Startet das Spiel"""
        self.window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_view = SwimmingGame()
        self.window.show_view(self.game_view)
        arcade.run()

def main():
    """Hauptfunktion"""
    game_manager = GameManager()
    game_manager.start_game()

if __name__ == "__main__":
    main()
    