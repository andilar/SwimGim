# ui.py - Benutzeroberfläche
import arcade
from config import *

class GameUI:
    """Klasse für die Spiel-Benutzeroberfläche"""
    
    def __init__(self):
        self.stamina_text = None
        self.regen_text = None
        self.win_text = None
        self.restart_text = None
        self.lane_numbers = []
        self._create_text_objects()
    
    def _create_text_objects(self):
        """Erstellt alle Text-Objekte für bessere Performance"""
        try:
            # Ausdauer-Texte
            self.stamina_text = arcade.Text("", STAMINA_BAR_X, STAMINA_BAR_Y + 18, 
                                          arcade.color.WHITE, 16)
            self.regen_text = arcade.Text("", STAMINA_BAR_X, STAMINA_BAR_Y - 22, 
                                        arcade.color.CYAN, 14)
            
            # Gewinn-Texte
            self.win_text = arcade.Text("", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, 
                                      arcade.color.GREEN, 24, anchor_x="center")
            self.restart_text = arcade.Text("", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, 
                                          arcade.color.WHITE, 20, anchor_x="center")
            
            # Bahnnummern
            for i in range(LANE_COUNT):
                x = i * LANE_WIDTH + LANE_WIDTH // 2
                text = arcade.Text(f"{i+1}", x - 10, 25, arcade.color.WHITE, 16)
                self.lane_numbers.append(text)
        except:
            # Fallback falls Text-Objekte nicht unterstützt werden
            pass
    
    def update_texts(self, player, game_finished, winner):
        """Update aller Text-Objekte"""
        if not self.stamina_text:
            return
        
        # Ausdauer-Texte
        self.stamina_text.text = f"Ausdauer: {player.stamina_float:.1f}/{MAX_STAMINA}"
        self.regen_text.text = f"Regeneration: +{STAMINA_RECOVERY_RATE}/s"
        
        # Gewinn-Texte
        if game_finished:
            if winner is None:
                self.win_text.text = "Du wurdest gefressen!"
                self.win_text.color = arcade.color.RED
            elif winner.is_player:
                self.win_text.text = "Du hast gewonnen!"
                self.win_text.color = arcade.color.GREEN
            else:
                self.win_text.text = "Du hast verloren!"
                self.win_text.color = arcade.color.RED
            self.restart_text.text = "Drücke R zum Neustarten"
    
    def draw_stamina_bar(self, player):
        """Zeichnet den Ausdauerbalken"""
        self._draw_stamina_background()
        self._draw_stamina_fill(player)
        self._draw_stamina_texts()
    
    def _draw_stamina_background(self):
        """Zeichnet Hintergrund des Ausdauerbalkens"""
        # Schatten
        shadow_rect = arcade.XYWH(STAMINA_BAR_X - 2, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2 - 2, 
                                 STAMINA_BAR_WIDTH + 4, STAMINA_BAR_HEIGHT + 4)
        arcade.draw_rect_filled(shadow_rect, arcade.color.BLACK)
        
        # Hintergrund
        background_rect = arcade.XYWH(STAMINA_BAR_X, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2, 
                                     STAMINA_BAR_WIDTH, STAMINA_BAR_HEIGHT)
        arcade.draw_rect_filled(background_rect, arcade.color.DARK_GRAY)
        
        # Rahmen
        arcade.draw_rect_outline(background_rect, arcade.color.WHITE, 3)
    
    def _draw_stamina_fill(self, player):
        """Zeichnet die Ausdauer-Füllung"""
        if player.stamina_float > 0:
            stamina_percentage = player.stamina_float / MAX_STAMINA
            stamina_width = (STAMINA_BAR_WIDTH - 6) * stamina_percentage
            
            # Farbe basierend auf Ausdauer
            if stamina_percentage > 0.6:
                color = arcade.color.GREEN
            elif stamina_percentage > 0.2:
                color = arcade.color.ORANGE
            else:
                color = arcade.color.RED
            
            stamina_rect = arcade.XYWH(STAMINA_BAR_X + 3, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2, 
                                      stamina_width, STAMINA_BAR_HEIGHT - 4)
            arcade.draw_rect_filled(stamina_rect, color)
    
    def _draw_stamina_texts(self):
        """Zeichnet Ausdauer-Texte"""
        if self.stamina_text:
            self.stamina_text.draw()
            self.regen_text.draw()
    
    def draw_lane_numbers(self):
        """Zeichnet Bahnnummern"""
        if self.lane_numbers:
            for lane_text in self.lane_numbers:
                lane_text.draw()
        else:
            # Fallback
            for i in range(LANE_COUNT):
                x = i * LANE_WIDTH + LANE_WIDTH // 2
                arcade.draw_text(f"{i+1}", x - 10, 25, arcade.color.WHITE, 16)
    
    def draw_game_over(self, game_finished, winner):
        """Zeichnet Game-Over-Nachrichten"""
        if not game_finished:
            return
        
        if self.win_text:
            self.win_text.draw()
            self.restart_text.draw()
        else:
            # Fallback
            self._draw_game_over_fallback(winner)
    
    def _draw_game_over_fallback(self, winner):
        """Fallback für Game-Over ohne Text-Objekte"""
        if winner is None:
            arcade.draw_text("Du wurdest gefressen!", 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                           arcade.color.RED, 24, anchor_x="center")
        elif winner.is_player:
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

class LaneRenderer:
    """Klasse für das Zeichnen der Schwimmbahnen"""
    
    @staticmethod
    def draw_lanes():
        """Zeichnet die 8 Schwimmbahnen"""
        LaneRenderer._draw_water_background()
        LaneRenderer._draw_lane_lines()
        LaneRenderer._draw_boundaries()
        LaneRenderer._draw_goal_line()
    
    @staticmethod
    def _draw_water_background():
        """Zeichnet Wasser-Hintergrund"""
        water_rect = arcade.XYWH(0, 50, SCREEN_WIDTH, LANE_HEIGHT)
        arcade.draw_rect_filled(water_rect, WATER_COLOR)
    
    @staticmethod
    def _draw_lane_lines():
        """Zeichnet Bahnlinien"""
        for i in range(LANE_COUNT + 1):
            x = i * LANE_WIDTH
            arcade.draw_line(x, 50, x, SCREEN_HEIGHT - 50, LANE_COLOR, 3)
    
    @staticmethod
    def _draw_boundaries():
        """Zeichnet obere und untere Begrenzungen"""
        arcade.draw_line(0, 50, SCREEN_WIDTH, 50, LANE_COLOR, 5)
        arcade.draw_line(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, SCREEN_HEIGHT - 50, LANE_COLOR, 5)
    
    @staticmethod
    def _draw_goal_line():
        """Zeichnet Ziellinie"""
        goal_y = SCREEN_HEIGHT - 70
        arcade.draw_line(0, goal_y, SCREEN_WIDTH, goal_y, arcade.color.YELLOW, 4)
        