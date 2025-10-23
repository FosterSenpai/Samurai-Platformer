# screen_state.py
# Base class for different screen states in the game.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
import pygame

class State():
    def __init__(self, game) -> None:
        self.game = game
        self.prev_state = None
        
    def update(self, delta_time: float, actions: dict) -> None: 
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        pass
    
    def enter_state(self):
        # If state exists in stack, store as prev state
        if len(self.game.screen_state_stack) > 1:
            self.prev_state = self.game.screen_state_stack[-1]
        self.game.screen_state_stack.append(self)
        
    def exit_state(self):
        self.game.screen_state_stack.pop()