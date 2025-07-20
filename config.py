# config.py - Zentrale Konfiguration
import arcade.color

# Bildschirm-Einstellungen
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
CURRENT_PUSHBACK = 15  # Halbe Schwimmzuglänge

# Ausdauer-Einstellungen
MAX_STAMINA = 5  # Maximale Ausdauer (Schwimmzüge)
STAMINA_RECOVERY_RATE = 1.5  # Ausdauer-Punkte pro Sekunde

# Gefahren-Einstellungen
SHARK_SPEED = 80  # Hai-Geschwindigkeit (Pixel pro Sekunde)
SHARK_SPAWN_MIN = 5.0  # Minimum Sekunden zwischen Hai-Spawns
SHARK_SPAWN_MAX = 15.0  # Maximum Sekunden zwischen Hai-Spawns
SHARK_SIZE = 30  # Größe des Hais

# Animation-Einstellungen
ANIMATION_SPEED = 1.5  # Schwimm-Animation Geschwindigkeit
ARM_REACH_OVER = 8  # Arm-Reichweite über Wasser
ARM_REACH_UNDER = 6  # Arm-Reichweite unter Wasser
ARM_HEIGHT_OVER = 5  # Arm-Höhe über Wasser
ARM_HEIGHT_UNDER = 3  # Arm-Höhe unter Wasser

# UI-Einstellungen
STAMINA_BAR_X = 10
STAMINA_BAR_Y = SCREEN_HEIGHT - 65
STAMINA_BAR_WIDTH = 250
STAMINA_BAR_HEIGHT = 25
