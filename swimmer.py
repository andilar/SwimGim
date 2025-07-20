# swimmer.py - Schwimmer-Klasse
import arcade
import random
import math
from config import *

class Swimmer:
    """Klasse für Schwimmer (Spieler und KI-Gegner)"""
    
    def __init__(self, x, y, lane, is_player=True):
        self.x = x
        self.y = y
        self.lane = lane
        self.strokes = 0
        self.is_player = is_player
        self.swim_timer = 0
        self.swim_speed = random.uniform(0.8, 1.2) if not is_player else 1.0
        self.current_timer = 0
        self.animation_timer = 0
        self.stroke_phase = 0
        self.active = True
        
        # Ausdauer nur für Spieler
        if self.is_player:
            self.stamina = MAX_STAMINA
            self.stamina_float = float(MAX_STAMINA)
    
    def swim_stroke(self):
        """Führt einen Schwimmzug aus"""
        if self.is_player:
            if self.stamina_float >= 1.0:
                self.y += SWIMMER_SPEED
                self.strokes += 1
                self.stamina_float -= 1.0
                self.stamina = int(self.stamina_float)
        else:
            self.y += SWIMMER_SPEED
            self.strokes += 1
    
    def apply_current(self):
        """Wendet Gegenstrom an"""
        self.y -= CURRENT_PUSHBACK
        if self.y < 50:
            self.y = 50
    
    def update(self, delta_time):
        """Update-Methode für Animation und Logik"""
        self._update_animation(delta_time)
        self._update_stamina(delta_time)
        self._update_current(delta_time)
        self._update_ai_swimming(delta_time)
    
    def _update_animation(self, delta_time):
        """Update der Schwimm-Animation"""
        self.animation_timer += delta_time * ANIMATION_SPEED
        self.stroke_phase = (self.animation_timer % 2.0) / 2.0
    
    def _update_stamina(self, delta_time):
        """Update der Ausdauer (nur Spieler)"""
        if self.is_player and self.stamina_float < MAX_STAMINA:
            self.stamina_float += STAMINA_RECOVERY_RATE * delta_time
            if self.stamina_float > MAX_STAMINA:
                self.stamina_float = MAX_STAMINA
            self.stamina = int(self.stamina_float)
    
    def _update_current(self, delta_time):
        """Update des Gegenstroms"""
        self.current_timer += delta_time
        if self.current_timer >= CURRENT_INTERVAL:
            self.apply_current()
            self.current_timer = 0
    
    def _update_ai_swimming(self, delta_time):
        """Update für KI-Schwimmen"""
        if not self.is_player and self.y < SCREEN_HEIGHT - 70:
            self.swim_timer += delta_time
            if self.swim_timer >= (1.0 / self.swim_speed):
                self.swim_stroke()
                self.swim_timer = 0
    
    def draw(self):
        """Zeichnet den Schwimmer"""
        if not self.active:
            return
        
        color = SWIMMER_COLOR if self.is_player else OPPONENT_COLOR
        head_color = arcade.color.PINK if self.is_player else arcade.color.LIGHT_GRAY
        
        self._draw_body(color)
        self._draw_head(head_color)
        self._draw_arms(color)
        self._draw_legs(color)
    
    def _draw_body(self, color):
        """Zeichnet den Körper"""
        arcade.draw_ellipse_filled(self.x, self.y, SWIMMER_SIZE, SWIMMER_SIZE//2, color)
    
    def _draw_head(self, color):
        """Zeichnet den Kopf"""
        arcade.draw_circle_filled(self.x, self.y + 5, SWIMMER_SIZE//4, color)
    
    def _draw_arms(self, color):
        """Zeichnet die Arme mit Kraul-Animation"""
        left_arm_x, left_arm_y, left_arm_color = self._calculate_arm_position(True, color)
        right_arm_x, right_arm_y, right_arm_color = self._calculate_arm_position(False, color)
        
        # Arme zeichnen
        arcade.draw_line(self.x - 3, self.y, left_arm_x, left_arm_y, left_arm_color, 3)
        arcade.draw_line(self.x + 3, self.y, right_arm_x, right_arm_y, right_arm_color, 3)
        
        # Hände
        arcade.draw_circle_filled(left_arm_x, left_arm_y, 2, color)
        arcade.draw_circle_filled(right_arm_x, right_arm_y, 2, color)
    
    def _calculate_arm_position(self, is_left, color):
        """Berechnet Arm-Position und Farbe"""
        phase_offset = 0 if is_left else 0.5
        phase = (self.stroke_phase + phase_offset) * math.pi * 2
        x_offset = -3 if is_left else 3
        
        # Über/Unter Wasser Berechnung
        if math.sin(phase) > 0:  # Über Wasser
            arm_x = self.x + x_offset + math.cos(phase) * ARM_REACH_OVER
            arm_y = self.y + 2 + math.sin(phase) * ARM_HEIGHT_OVER
            arm_color = color
        else:  # Unter Wasser
            arm_x = self.x + x_offset + math.cos(phase) * ARM_REACH_UNDER
            arm_y = self.y - 1 + math.sin(phase) * ARM_HEIGHT_UNDER
            arm_color = tuple(max(0, c - 50) for c in color[:3]) + (255,)
        
        return arm_x, arm_y, arm_color
    
    def _draw_legs(self, color):
        """Zeichnet die Beine"""
        leg_kick = math.sin(self.stroke_phase * math.pi * 4) * 0.3
        
        # Bein-Positionen berechnen
        left_leg_x = self.x - 3 + math.cos(leg_kick) * 6
        left_leg_y = self.y - 8 + math.sin(leg_kick) * 3
        
        right_leg_x = self.x + 3 + math.cos(leg_kick + math.pi) * 6
        right_leg_y = self.y - 8 + math.sin(leg_kick + math.pi) * 3
        
        # Beine zeichnen
        arcade.draw_line(self.x - 3, self.y - 5, left_leg_x, left_leg_y, color, 3)
        arcade.draw_line(self.x + 3, self.y - 5, right_leg_x, right_leg_y, color, 3)
        
        # Füße
        arcade.draw_circle_filled(left_leg_x, left_leg_y, 2, color)
        arcade.draw_circle_filled(right_leg_x, right_leg_y, 2, color)
        