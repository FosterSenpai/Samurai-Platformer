# title_state.py
# Title screen state for the game.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
from scripts.screen_states.screen_state import State
from scripts.utilities.text import Text
from scripts.utilities.asset_manager import AssetManager

class TitleState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.bg0 = AssetManager.core_sprites['bg0']
        self.bg1 = AssetManager.core_sprites['bg1']
        self.bg2 = AssetManager.core_sprites['bg2']

    def update(self, delta_time: float, actions: dict) -> None:
        self.game.controller.reset_actions()
    
    def render(self, surface) -> None:
        surface.blit(self.bg0, (0,0))
        surface.blit(self.bg1, (0,0))
        surface.blit(self.bg2, (0,0))
        Text.draw_text(surface, "Title Screen", 'black', 100,30)