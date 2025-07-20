# dangers.py - Gefahren-Klassen
import arcade
import random
from config import *

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
        self.from_left = random.choice([True, False])
        start_x = -SHARK_SIZE if self.from_left else SCREEN_WIDTH + SHARK_SIZE
        start_y = target_swimmer.y
        
        super().__init__(start_x, start_y)
        self.target = target_swimmer
        self.has_caught = False
        self.is_diving = False
        self.dive_timer = 0
        self.dive_duration = 2.0
    
    def update(self, delta_time, swimmers):
        """Hai-Update-Logik"""
        if not self.active:
            return
        
        if self.is_diving:
            self._update_diving(delta_time)
        elif not self.has_caught:
            self._update_hunting(delta_time)
    
    def _update_diving(self, delta_time):
        """Update für abtauchenden Hai"""
        self.dive_timer += delta_time
        self.y -= 100 * delta_time
        
        if self.dive_timer >= self.dive_duration or self.y < 30:
            self.active = False
    
    def _update_hunting(self, delta_time):
        """Update für jagenden Hai"""
        # Horizontale Bewegung
        if self.from_left:
            self.x += SHARK_SPEED * delta_time
        else:
            self.x -= SHARK_SPEED * delta_time
        
        # Vertikale Verfolgung
        if self.target.y > self.y:
            self.y += SHARK_SPEED * 0.3 * delta_time
        elif self.target.y < self.y:
            self.y -= SHARK_SPEED * 0.3 * delta_time
        
        # Kollisionsprüfung
        distance = ((self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2) ** 0.5
        if distance < SHARK_SIZE:
            self.catch_swimmer()
        
        # Bildschirm verlassen
        if ((self.from_left and self.x > SCREEN_WIDTH + SHARK_SIZE) or
            (not self.from_left and self.x < -SHARK_SIZE)):
            self.active = False
    
    def catch_swimmer(self):
        """Hai fängt Schwimmer"""
        self.has_caught = True
        self.is_diving = True
        self.dive_timer = 0
        
        # Schwimmer entfernen
        self.target.y = -100
        self.target.active = False
    
    def draw(self):
        """Zeichnet den Hai"""
        if not self.active:
            return
        
        alpha = self._calculate_alpha()
        self._draw_shark_body(alpha)
        self._draw_shark_details(alpha)
        
        if self.is_diving:
            self._draw_bubbles()
    
    def _calculate_alpha(self):
        """Berechnet Transparenz für abtauchenden Hai"""
        if self.is_diving:
            alpha = int(255 * (1 - self.dive_timer / self.dive_duration))
            return max(50, alpha)
        return 255
    
    def _draw_shark_body(self, alpha):
        """Zeichnet Hai-Körper"""
        body_color = (*arcade.color.DARK_GRAY[:3], alpha)
        arcade.draw_ellipse_filled(self.x, self.y, SHARK_SIZE * 1.5, SHARK_SIZE // 2, body_color)
    
    def _draw_shark_details(self, alpha):
        """Zeichnet Hai-Details (Kopf, Zähne, Flosse)"""
        # Kopf
        head_x = self.x + (SHARK_SIZE//3 if self.from_left else -SHARK_SIZE//3)
        head_color = (*arcade.color.GRAY[:3], alpha)
        arcade.draw_ellipse_filled(head_x, self.y, SHARK_SIZE//2, SHARK_SIZE//3, head_color)
        
        # Zähne
        tooth_color = (*arcade.color.WHITE[:3], alpha)
        for i in range(3):
            tooth_x = head_x + (5 if self.from_left else -5)
            tooth_y = self.y - 5 + i * 5
            arcade.draw_triangle_filled(
                tooth_x, tooth_y,
                tooth_x + (3 if self.from_left else -3), tooth_y + 3,
                tooth_x + (3 if self.from_left else -3), tooth_y - 3,
                tooth_color
            )
        
        # Schwanzflosse
        fin_x = self.x + (-SHARK_SIZE//2 if self.from_left else SHARK_SIZE//2)
        fin_color = (*arcade.color.DARK_GRAY[:3], alpha)
        arcade.draw_triangle_filled(
            fin_x, self.y,
            fin_x + (-SHARK_SIZE//3 if self.from_left else SHARK_SIZE//3), self.y + SHARK_SIZE//4,
            fin_x + (-SHARK_SIZE//3 if self.from_left else SHARK_SIZE//3), self.y - SHARK_SIZE//4,
            fin_color
        )
    
    def _draw_bubbles(self):
        """Zeichnet Luftblasen beim Abtauchen"""
        for i in range(3):
            bubble_x = self.x + random.randint(-10, 10)
            bubble_y = self.y + 20 + i * 8
            bubble_size = random.randint(2, 5)
            arcade.draw_circle_filled(bubble_x, bubble_y, bubble_size, arcade.color.LIGHT_BLUE)

class DangerManager:
    """Manager für alle Gefahren"""
    
    def __init__(self):
        self.dangers = []
        self.shark_spawn_timer = 0
        self.next_shark_spawn = random.uniform(SHARK_SPAWN_MIN, SHARK_SPAWN_MAX)
    
    def update(self, delta_time, swimmers):
        """Update aller Gefahren"""
        self._update_spawn_timer(delta_time, swimmers)
        self._update_dangers(delta_time, swimmers)
    
    def _update_spawn_timer(self, delta_time, swimmers):
        """Update des Spawn-Timers"""
        self.shark_spawn_timer += delta_time
        if self.shark_spawn_timer >= self.next_shark_spawn:
            self.spawn_shark(swimmers)
            self.shark_spawn_timer = 0
            self.next_shark_spawn = random.uniform(SHARK_SPAWN_MIN, SHARK_SPAWN_MAX)
    
    def _update_dangers(self, delta_time, swimmers):
        """Update aller aktiven Gefahren"""
        for danger in self.dangers[:]:
            danger.update(delta_time, swimmers)
            if not danger.active:
                self.dangers.remove(danger)
    
    def spawn_shark(self, swimmers):
        """Spawnt einen neuen Hai"""
        active_swimmers = [s for s in swimmers if s.y > 100 and s.active]
        if active_swimmers:
            weights = [s.y for s in active_swimmers]
            target = random.choices(active_swimmers, weights=weights)[0]
            shark = Shark(target)
            self.dangers.append(shark)
    
    def draw_all(self):
        """Zeichnet alle Gefahren"""
        for danger in self.dangers:
            danger.draw()
    
    def reset(self):
        """Setzt alle Gefahren zurück"""
        self.dangers = []
        self.shark_spawn_timer = 0
        self.next_shark_spawn = random.uniform(SHARK_SPAWN_MIN, SHARK_SPAWN_MAX)
        