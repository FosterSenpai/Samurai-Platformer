# config.py
# Configuration file holding all game settings.
# Author: Foster Rae
# Created: 17-10-2025
# Last Modified: 17-10-2025
import pygame
import json

class Config:
    # Display settings
    GAME_W, GAME_H = 640, 360
    SCREEN_W, SCREEN_H = 1280, 720
    FPS = 60

    # Control settings
    PLAYER_LEFT = pygame.K_a
    PLAYER_RIGHT = pygame.K_d
    PLAYER_JUMP = pygame.K_SPACE
    PLAYER_DOWN = pygame.K_s
    PLAYER_DASH = pygame.K_LSHIFT
    
    @staticmethod
    def load_settings():
        """Load settings from a JSON file."""
        with open('config.json', 'r') as f:
            settings = json.load(f)
        Config.update_control_settings(settings.get('controls', {}))
        Config.update_display_settings(settings.get('display', {}))

    @staticmethod
    def update_display_settings(new_settings):
        """Update the display settings, used for settings menu changes.
        Args:
            new_settings (dict): A dictionary with new display settings.
        """
        # Getting new display settings
        Config.SCREEN_W = new_settings.get('screen_width', Config.SCREEN_W)
        Config.SCREEN_H = new_settings.get('screen_height', Config.SCREEN_H)
        Config.FPS = new_settings.get('fps', Config.FPS)

    @staticmethod
    def update_control_settings(new_settings):
        """Update the control settings, used for settings menu changes.
        Args:
            new_settings (dict): A dictionary with new control settings.
        """
        # Getting new control settings
        Config.PLAYER_LEFT = new_settings.get('move_left', Config.PLAYER_LEFT)
        Config.PLAYER_RIGHT = new_settings.get('move_right', Config.PLAYER_RIGHT)
        Config.PLAYER_JUMP = new_settings.get('jump', Config.PLAYER_JUMP)
        Config.PLAYER_DOWN = new_settings.get('down', Config.PLAYER_DOWN)
        Config.PLAYER_DASH = new_settings.get('dash', Config.PLAYER_DASH)

    @staticmethod
    def reset_to_defaults():
        """Reset all settings to their default values."""
        # Display settings
        Config.GAME_W, Config.GAME_H = 640, 360
        Config.SCREEN_W, Config.SCREEN_H = 1280, 720
        Config.FPS = 60

        # Control settings
        Config.PLAYER_LEFT = pygame.K_a
        Config.PLAYER_RIGHT = pygame.K_d
        Config.PLAYER_JUMP = pygame.K_SPACE
        Config.PLAYER_DOWN = pygame.K_s
        Config.PLAYER_DASH = pygame.K_LSHIFT
        
    @staticmethod
    def save_settings():
        """Save current settings to a JSON file."""
        settings = {
            'display': {
                'screen_width': Config.SCREEN_W,
                'screen_height': Config.SCREEN_H,
                'fps': Config.FPS
            },
            'controls': {
                'move_left': Config.PLAYER_LEFT,
                'move_right': Config.PLAYER_RIGHT,
                'jump': Config.PLAYER_JUMP,
                'down': Config.PLAYER_DOWN,
                'dash': Config.PLAYER_DASH
            }
        }
        
        with open('config.json', 'w') as f:
            json.dump(settings, f, indent=4)