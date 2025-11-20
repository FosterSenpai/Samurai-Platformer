# player_controller.py
# Component to handle player input and control the Player entity.
# Author: Foster Rae
# Created: 17-10-2025
# Last Modified: 17-10-2025
import pygame
from scripts.config import Config
from scripts.entities.player import Player

class PlayerController:
    """Controller for the player to handle inputs and apply forces.
    Also used for other inputs like menus so initialized with no player.  
    make sure to assign player before gameplay start.
    """
    def __init__(self) -> None:
        self.player: Player | None = None
        # Action states
        self.actions = {
            'left': False,
            'right': False,
            'up': False,
            'down': False,
            'dash': False,
            'escape': False,
        }

    def handle_input(self, event: pygame.Event) -> None:
        """Handle key events, updates controller action states to trigger
        functionality.
        Args:
            event (pygame.Event): The pygame event to handle.
        """
        # Activate actions on keydown
        if event.type == pygame.KEYDOWN:
            if event.key == Config.PLAYER_LEFT:
                self.actions['left'] = True
            if event.key == Config.PLAYER_RIGHT:
                self.actions['right'] = True
            if event.key == Config.PLAYER_JUMP:
                self.actions['jump'] = True
            if event.key == Config.PLAYER_DASH:
                self.actions['dash'] = True
            if event.key == pygame.K_ESCAPE:
                self.actions['escape'] = True
        # Deactivate actions on keyup
        if event.type == pygame.KEYUP:
            if event.key == Config.PLAYER_LEFT:
                self.actions['left'] = False
            if event.key == Config.PLAYER_RIGHT:
                self.actions['right'] = False
            if event.key == Config.PLAYER_JUMP:
                self.actions['jump'] = False
            if event.key == Config.PLAYER_DASH:
                self.actions['dash'] = False
            if event.key == pygame.K_ESCAPE:
                self.actions['escape'] = False
                
    def reset_actions(self) -> None:
        """Reset all action states to False."""
        for action in self.actions:
            self.actions[action] = False