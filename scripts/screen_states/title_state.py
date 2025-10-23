# title_state.py
# Title screen state for the game.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
from scripts.screen_states.screen_state import State
from scripts.utilities.text import Text

class TitleState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        
    def update(self, delta_time: float, actions: dict) -> None:
        self.game.controller.reset_actions()
    
    def render(self, surface) -> None:
        surface.fill((255,255,255))
        Text.draw_text(surface, "Title Screen", 'black', 100,30)