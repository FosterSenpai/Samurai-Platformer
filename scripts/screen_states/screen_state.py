# screen_state.py
# Base class for different screen states in the game.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
import pygame
from scripts.utilities.asset_manager import AssetManager

class State():
    def __init__(self, game) -> None:
        self.game = game
        
    def update(self, delta_time: float, actions: dict) -> None: 
        """Override with custom update logic."""
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Override with custom render logic."""
        pass
    
    def enter_state(self):
        """Push this state onto the game's state stack."""
        self.game.screen_state_stack.append(self)
        self.on_enter()
        
    def on_enter(self):
        """Override to add custom behavior on entering state."""
        pass
    
    def on_resume(self):
        """Override to add custom behavior on resuming state."""
        pass
        
    def exit_state(self):
        """Pop this state from the game's state stack."""
        self.game.screen_state_stack.pop()
        if self.game.screen_state_stack:
            self.game.screen_state_stack[-1].on_resume()