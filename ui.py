# ui.py - 8-Bit Benutzeroberfläche
import arcade
from config import *
from fonts import draw_8bit_text, draw_pixel_text, create_8bit_text, ASCIIArt

class GameUI:
    """Klasse für die 8-Bit Spiel-Benutzeroberfläche"""
    
    def __init__(self):
        self.stamina_text = None
        self.regen_text = None
        self.win_text = None
        self.restart_text = None
        self.lane_numbers = []
        self._create_text_objects()
    
    def _create_text_objects(self):
        """Erstellt alle Text-Objekte mit 8-Bit Schriftarten"""
        try:
            # Ausdauer-Texte mit 8-Bit Schrift
            self.stamina_text = create_8bit_text("", STAMINA_BAR_X, STAMINA_BAR_Y + 18, 
                                               'game', 16, arcade.color.WHITE)
            self.regen_text = create_8bit_text("", STAMINA_BAR_X, STAMINA_BAR_Y - 22, 
                                             'small', 12, arcade.color.CYAN)
            
            # Gewinn-Texte
            self.win_text = create_8bit_text("", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, 
                                           'title', 24, arcade.color.GREEN, anchor_x="center")
            self.restart_text = create_8bit_text("", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, 
                                               'menu', 18, arcade.color.WHITE, anchor_x="center")
            
            # Bahnnummern mit 8-Bit Schrift
            for i in range(LANE_COUNT):
                x = i * LANE_WIDTH + LANE_WIDTH // 2
                text = create_8bit_text(f"[{i+1}]", x - 15, 25, 'small', 14, arcade.color.WHITE)
                self.lane_numbers.append(text)
        except:
            # Fallback falls Text-Objekte nicht unterstützt werden
            pass
    
    def update_texts(self, player, game_finished, winner):
        """Update aller Text-Objekte mit 8-Bit Styling"""
        if not self.stamina_text:
            return
        
        # Ausdauer-Texte mit 8-Bit Format
        self.stamina_text.text = f"AUSDAUER: {player.stamina_float:04.1f}/{MAX_STAMINA}"
        self.regen_text.text = f"+{STAMINA_RECOVERY_RATE}/s"
        
        # Gewinn-Texte
        if game_finished:
            if winner is None:
                self.win_text.text = "GEFRESSEN!"
                self.win_text.color = arcade.color.RED
            elif winner.is_player:
                self.win_text.text = "VICTORY!"
                self.win_text.color = arcade.color.GREEN
            else:
                self.win_text.text = "DEFEAT!"
                self.win_text.color = arcade.color.RED
            self.restart_text.text = "R = RESTART"
    
    def draw_stamina_bar(self, player):
        """Zeichnet den 8-Bit Ausdauerbalken"""
        self._draw_pixel_stamina_background()
        self._draw_pixel_stamina_fill(player)
        self._draw_stamina_texts()
        self._draw_stamina_segments(player)
    
    def _draw_pixel_stamina_background(self):
        """Zeichnet pixeligen Hintergrund des Ausdauerbalkens"""
        # Doppelter pixeliger Rahmen
        outer_rect = arcade.XYWH(STAMINA_BAR_X - 4, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2 - 4, 
                                STAMINA_BAR_WIDTH + 8, STAMINA_BAR_HEIGHT + 8)
        arcade.draw_rect_filled(outer_rect, arcade.color.BLACK)
        
        # Äußerer Rahmen
        ASCIIArt.draw_pixel_border(STAMINA_BAR_X - 2, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2 - 2, 
                                  STAMINA_BAR_WIDTH + 4, STAMINA_BAR_HEIGHT + 4, 
                                  arcade.color.WHITE, 2)
        
        # Innerer Hintergrund
        background_rect = arcade.XYWH(STAMINA_BAR_X, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2, 
                                     STAMINA_BAR_WIDTH, STAMINA_BAR_HEIGHT)
        arcade.draw_rect_filled(background_rect, arcade.color.DARK_GRAY)
        
        # Innerer Rahmen
        ASCIIArt.draw_pixel_border(STAMINA_BAR_X, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2, 
                                  STAMINA_BAR_WIDTH, STAMINA_BAR_HEIGHT, 
                                  arcade.color.GRAY, 1)
    
    def _draw_pixel_stamina_fill(self, player):
        """Zeichnet die pixelige Ausdauer-Füllung"""
        if player.stamina_float > 0:
            stamina_percentage = player.stamina_float / MAX_STAMINA
            stamina_width = (STAMINA_BAR_WIDTH - 4) * stamina_percentage
            
            # 8-Bit Farb-Gradient
            if stamina_percentage > 0.6:
                color = arcade.color.GREEN
            elif stamina_percentage > 0.4:
                color = arcade.color.YELLOW  
            elif stamina_percentage > 0.2:
                color = arcade.color.ORANGE
            else:
                color = arcade.color.RED
            
            # Pixelige Füllung
            fill_rect = arcade.XYWH(STAMINA_BAR_X + 2, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2 + 2, 
                                   stamina_width, STAMINA_BAR_HEIGHT - 4)
            arcade.draw_rect_filled(fill_rect, color)
            
            # 8-Bit Glitzer-Effekt bei voller Ausdauer
            if stamina_percentage > 0.9:
                import random, time
                for i in range(3):
                    spark_x = STAMINA_BAR_X + 2 + random.randint(0, int(stamina_width))
                    spark_y = STAMINA_BAR_Y + random.randint(-8, 8)
                    if int(time.time() * 10 + i) % 2:
                        arcade.draw_rectangle_filled(spark_x, spark_y, 2, 2, arcade.color.WHITE)
    
    def _draw_stamina_segments(self, player):
        """Zeichnet 8-Bit Segmente für bessere Lesbarkeit"""
        # Zeichne Trennlinien für jede Ausdauer-Einheit
        segment_width = (STAMINA_BAR_WIDTH - 4) / MAX_STAMINA
        
        for i in range(1, MAX_STAMINA):
            segment_x = STAMINA_BAR_X + 2 + i * segment_width
            arcade.draw_line(segment_x, STAMINA_BAR_Y - STAMINA_BAR_HEIGHT//2 + 2,
                           segment_x, STAMINA_BAR_Y + STAMINA_BAR_HEIGHT//2 - 2,
                           arcade.color.BLACK, 1)
    
    def _draw_stamina_texts(self):
        """Zeichnet 8-Bit Ausdauer-Texte"""
        if self.stamina_text:
            self.stamina_text.draw()
            self.regen_text.draw()
        else:
            # Fallback mit Standard-Schriften
            draw_8bit_text(f"AUSDAUER: {MAX_STAMINA}", STAMINA_BAR_X, STAMINA_BAR_Y + 18,
                          'game', 16, arcade.color.WHITE)
            draw_8bit_text(f"+{STAMINA_RECOVERY_RATE}/s", STAMINA_BAR_X, STAMINA_BAR_Y - 22,
                          'small', 12, arcade.color.CYAN)
    
    def draw_lane_numbers(self):
        """Zeichnet 8-Bit Bahnnummern"""
        if self.lane_numbers:
            for lane_text in self.lane_numbers:
                lane_text.draw()
        else:
            # Fallback mit pixeligen Bahnnummern
            for i in range(LANE_COUNT):
                x = i * LANE_WIDTH + LANE_WIDTH // 2
                draw_pixel_text(f"[{i+1}]", x - 15, 25, 14, arcade.color.WHITE, 
                               outline=True, anchor_x="center")
    
    def draw_game_over(self, game_finished, winner):
        """Zeichnet 8-Bit Game-Over-Nachrichten"""
        if not game_finished:
            return
        
        # 8-Bit Game-Over Box
        self._draw_game_over_box()
        
        if self.win_text:
            self.win_text.draw()
            self.restart_text.draw()
        else:
            # Fallback mit 8-Bit Styling
            self._draw_game_over_fallback(winner)
    
    def _draw_game_over_box(self):
        """Zeichnet pixelige Game-Over Box"""
        box_width, box_height = 400, 150
        box_x = SCREEN_WIDTH // 2 - box_width // 2
        box_y = SCREEN_HEIGHT // 2 - box_height // 2
        
        # Box-Hintergrund
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                   box_width, box_height, 
                                   (*arcade.color.DARK_BLUE[:3], 220))
        
        # Pixeliger Rahmen
        ASCIIArt.draw_pixel_border(box_x, box_y, box_width, box_height, 
                                  arcade.color.WHITE, 3)
        ASCIIArt.draw_pixel_border(box_x + 6, box_y + 6, box_width - 12, box_height - 12, 
                                  arcade.color.YELLOW, 1)
    
    def _draw_game_over_fallback(self, winner):
        """Fallback für Game-Over ohne Text-Objekte"""
        if winner is None:
            draw_pixel_text("GEFRESSEN!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                           24, arcade.color.RED, outline=True, anchor_x="center")
        elif winner.is_player:
            draw_pixel_text("VICTORY!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                           24, arcade.color.GREEN, outline=True, anchor_x="center")
        else:
            draw_pixel_text("DEFEAT!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                           24, arcade.color.RED, outline=True, anchor_x="center")
        
        draw_pixel_text("R = RESTART", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                       18, arcade.color.WHITE, outline=True, anchor_x="center")

class LaneRenderer:
    """Klasse für das 8-Bit Zeichnen der Schwimmbahnen"""
    
    @staticmethod
    def draw_lanes():
        """Zeichnet die 8 Schwimmbahnen im 8-Bit Stil"""
        LaneRenderer._draw_pixel_water_background()
        LaneRenderer._draw_pixel_lane_lines()
        LaneRenderer._draw_pixel_boundaries()
        LaneRenderer._draw_pixel_goal_line()
    
    @staticmethod
    def _draw_pixel_water_background():
        """Zeichnet pixeligen Wasser-Hintergrund"""
        # Haupt-Wasser-Bereich
        water_rect = arcade.XYWH(0, 50, SCREEN_WIDTH, LANE_HEIGHT)
        arcade.draw_rect_filled(water_rect, WATER_COLOR)
        
        # 8-Bit Wasser-Textur
        import time, random
        texture_time = time.time()
        
        for y in range(50, 50 + LANE_HEIGHT, 8):
            for x in range(0, SCREEN_WIDTH, 16):
                if (x + y + int(texture_time * 10)) % 32 < 16:
                    water_pixel = arcade.XYWH(x, y, 8, 8)
                    darker_water = tuple(max(0, c - 20) for c in WATER_COLOR[:3])
                    arcade.draw_rect_filled(water_pixel, darker_water)
    
    @staticmethod
    def _draw_pixel_lane_lines():
        """Zeichnet pixelige Bahnlinien"""
        for i in range(LANE_COUNT + 1):
            x = i * LANE_WIDTH
            
            # Pixelige Linie (gestrichelt für 8-Bit Look)
            for y in range(50, SCREEN_HEIGHT - 50, 16):
                if y % 32 < 16:  # Gestrichelter Effekt
                    line_segment = arcade.XYWH(x - 1, y, 3, 12)
                    arcade.draw_rect_filled(line_segment, LANE_COLOR)
    
    @staticmethod
    def _draw_pixel_boundaries():
        """Zeichnet pixelige Begrenzungen"""
        # Untere Begrenzung
        bottom_rect = arcade.XYWH(0, 45, SCREEN_WIDTH, 10)
        arcade.draw_rect_filled(bottom_rect, LANE_COLOR)
        
        # Obere Begrenzung
        top_rect = arcade.XYWH(0, SCREEN_HEIGHT - 55, SCREEN_WIDTH, 10)
        arcade.draw_rect_filled(top_rect, LANE_COLOR)
        
        # Pixelige Ecken
        corner_size = 8
        corner_positions = [
            (0, 45), (SCREEN_WIDTH - corner_size, 45),
            (0, SCREEN_HEIGHT - 55), (SCREEN_WIDTH - corner_size, SCREEN_HEIGHT - 55)
        ]
        
        for corner_x, corner_y in corner_positions:
            corner_rect = arcade.XYWH(corner_x, corner_y, corner_size, corner_size)
            arcade.draw_rect_filled(corner_rect, arcade.color.DARK_BLUE)
    
    @staticmethod
    def _draw_pixel_goal_line():
        """Zeichnet pixelige Ziellinie"""
        goal_y = SCREEN_HEIGHT - 70
        
        # Animierte Ziellinie
        import time
        blink_time = time.time()
        
        # Haupt-Ziellinie
        goal_rect = arcade.XYWH(0, goal_y - 2, SCREEN_WIDTH, 4)
        arcade.draw_rect_filled(goal_rect, arcade.color.YELLOW)
        
        # Blinkende Pixel-Akzente
        for x in range(0, SCREEN_WIDTH, 20):
            if int(blink_time * 4 + x / 10) % 2:
                pixel_rect = arcade.XYWH(x, goal_y - 4, 8, 8)
                arcade.draw_rect_filled(pixel_rect, arcade.color.WHITE)
        
        # "ZIEL" Text
        draw_pixel_text("ZIEL", SCREEN_WIDTH // 2, goal_y + 10, 
                       12, arcade.color.YELLOW, outline=True, anchor_x="center")

class PixelHUD:
    """8-Bit Head-Up Display für zusätzliche Informationen"""
    
    def __init__(self):
        self.show_debug = False
        self.fps_counter = 0
        self.frame_time = 0
    
    def update(self, delta_time):
        """Update HUD-Informationen"""
        self.frame_time = delta_time
        self.fps_counter = int(1 / delta_time) if delta_time > 0 else 0
    
    def draw_debug_info(self, player, swimmers, dangers):
        """Zeichnet Debug-Informationen im 8-Bit Stil"""
        if not self.show_debug:
            return
        
        debug_y = SCREEN_HEIGHT - 50
        
        # Debug-Box
        debug_box = arcade.XYWH(SCREEN_WIDTH - 200, debug_y - 80, 190, 70)
        arcade.draw_rect_filled(debug_box, (*arcade.color.BLACK[:3], 180))
        ASCIIArt.draw_pixel_border(SCREEN_WIDTH - 200, debug_y - 80, 190, 70, 
                                  arcade.color.GREEN, 1)
        
        # Debug-Texte
        draw_8bit_text(f"FPS: {self.fps_counter:03d}", SCREEN_WIDTH - 190, debug_y - 20,
                      'small', 10, arcade.color.GREEN)
        draw_8bit_text(f"SWIMMER: {len(swimmers)}", SCREEN_WIDTH - 190, debug_y - 35,
                      'small', 10, arcade.color.WHITE)
        draw_8bit_text(f"SHARKS: {len(dangers)}", SCREEN_WIDTH - 190, debug_y - 50,
                      'small', 10, arcade.color.RED)
        draw_8bit_text(f"POS: {int(player.y)}", SCREEN_WIDTH - 190, debug_y - 65,
                      'small', 10, arcade.color.CYAN)
    
    def draw_mini_map(self, swimmers, dangers):
        """Zeichnet eine pixelige Mini-Map"""
        map_x, map_y = SCREEN_WIDTH - 120, SCREEN_HEIGHT - 150
        map_width, map_height = 100, 80
        
        # Mini-Map Hintergrund
        map_rect = arcade.XYWH(map_x, map_y, map_width, map_height)
        arcade.draw_rect_filled(map_rect, (*arcade.color.DARK_BLUE[:3], 150))
        ASCIIArt.draw_pixel_border(map_x, map_y, map_width, map_height, 
                                  arcade.color.WHITE, 2)
        
        # Mini-Map Titel
        draw_pixel_text("MAP", map_x + map_width // 2, map_y + map_height + 10,
                       10, arcade.color.WHITE, outline=False, anchor_x="center")
        
        # Schwimmer auf Mini-Map
        for swimmer in swimmers:
            if swimmer.active:
                mini_x = map_x + (swimmer.lane * map_width // LANE_COUNT) + map_width // (LANE_COUNT * 2)
                mini_y = map_y + (swimmer.y / SCREEN_HEIGHT) * map_height
                
                color = arcade.color.RED if swimmer.is_player else arcade.color.BLUE
                arcade.draw_rectangle_filled(mini_x, mini_y, 3, 3, color)
        
        # Haie auf Mini-Map
        for danger in dangers:
            if danger.active:
                mini_x = map_x + (danger.x / SCREEN_WIDTH) * map_width
                mini_y = map_y + (danger.y / SCREEN_HEIGHT) * map_height
                arcade.draw_rectangle_filled(mini_x, mini_y, 2, 2, arcade.color.GRAY)
    
    def toggle_debug(self):
        """Schaltet Debug-Modus um"""
        self.show_debug = not self.show_debug

class RetroEffects:
    """8-Bit Spezialeffekte"""
    
    @staticmethod
    def draw_scan_lines():
        """Zeichnet CRT-artige Scan-Linien"""
        for y in range(0, SCREEN_HEIGHT, 4):
            scan_line = arcade.XYWH(0, y, SCREEN_WIDTH, 1)
            arcade.draw_rect_filled(scan_line, (*arcade.color.BLACK[:3], 30))
    
    @staticmethod
    def draw_screen_border():
        """Zeichnet einen pixeligen Bildschirmrahmen"""
        border_width = 8
        
        # Äußerer Rahmen
        ASCIIArt.draw_pixel_border(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 
                                  arcade.color.DARK_GRAY, border_width)
        
        # Innerer Rahmen
        ASCIIArt.draw_pixel_border(border_width, border_width, 
                                  SCREEN_WIDTH - border_width * 2, 
                                  SCREEN_HEIGHT - border_width * 2,
                                  arcade.color.WHITE, 2)
        
        # Ecken-Details
        corner_size = 16
        corner_positions = [
            (border_width, SCREEN_HEIGHT - border_width - corner_size),
            (SCREEN_WIDTH - border_width - corner_size, SCREEN_HEIGHT - border_width - corner_size),
            (border_width, border_width),
            (SCREEN_WIDTH - border_width - corner_size, border_width)
        ]
        
        for corner_x, corner_y in corner_positions:
            arcade.draw_rectangle_filled(corner_x + corner_size//2, corner_y + corner_size//2,
                                       corner_size, corner_size, arcade.color.GRAY)
    
    @staticmethod
    def draw_pixel_splash(x, y, color=arcade.color.WHITE, size=5):
        """Zeichnet einen pixeligen Spritzer-Effekt"""
        import random
        
        for i in range(size):
            splash_x = x + random.randint(-8, 8)
            splash_y = y + random.randint(-8, 8)
            pixel_size = random.randint(1, 3)
            
            splash_color = tuple(max(0, c + random.randint(-50, 50)) for c in color[:3])
            arcade.draw_rectangle_filled(splash_x, splash_y, pixel_size, pixel_size, splash_color)
    
    @staticmethod
    def draw_glitch_effect(x, y, width, height, intensity=0.1):
        """Zeichnet einen 8-Bit Glitch-Effekt"""
        import random, time
        
        if random.random() < intensity:
            glitch_height = random.randint(2, 8)
            glitch_y = y + random.randint(0, height - glitch_height)
            
            # Farbverschiebung
            colors = [arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE]
            color = random.choice(colors)
            
            glitch_rect = arcade.XYWH(x, glitch_y, width, glitch_height)
            arcade.draw_rect_filled(glitch_rect, (*color[:3], 100))

# Globale UI-Instanz
pixel_hud = PixelHUD()# ui.py - Benutzeroberfläche
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
        # self._draw_stamina_texts()
    
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
        