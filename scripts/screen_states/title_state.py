# title_state.py
# Title screen state for the game.
# Author: Foster Rae
# Created: 23-10-2025
# Last Modified: 23-10-2025
import pygame
from scripts.screen_states.screen_state import State
from scripts.utilities.text import Text
from scripts.utilities.asset_manager import AssetManager

class TitleState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        canvas_w, canvas_h = self.game.GAME_W, self.game.GAME_H
        # UI elements
        big_box_width, big_box_height = int(canvas_w * 0.35), int(canvas_h * 0.8)
        self.ui_big_box = pygame.transform.scale(AssetManager.core_sprites['ui_sprite159'], (big_box_width, big_box_height))
        menu_button_width, menu_button_height = int(big_box_width * 0.7), int(big_box_height * 0.15)
        self.ui_button = pygame.transform.scale(AssetManager.core_sprites['ui_sprite205'], (menu_button_width, menu_button_height))
        self.ui_button_active = AssetManager.core_sprites['ui_sprite206'].copy()
        self.ui_play_button = self.ui_button.copy()
        self.ui_load_button = self.ui_button.copy()
        self.ui_options_button = self.ui_button.copy()
        self.ui_quit_button = self.ui_button.copy()
        # Background
        self.bg0 = AssetManager.core_sprites['bg0']
        self.bg1 = AssetManager.core_sprites['bg1']
        self.bg2 = AssetManager.core_sprites['bg2']
        self.bg0_x, self.bg1_x, self.bg2_x = 0, 0, 0 # Bg x positions for scrolling
        
        # Load and play music
        pygame.mixer.music.load(AssetManager.core_sounds['evening mood'])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1) # Loop

    def update(self, delta_time: float, actions: dict) -> None:
        self.scroll_bg(delta_time)
        self.game.controller.reset_actions()
    
    def render(self, surface: pygame.Surface) -> None:
        self.draw_bg(surface)
        Text.draw_title(surface, "LOFI SAMURAI", surface.get_width() // 2, surface.get_height() // 16)
        self.draw_ui(surface)
        
    def scroll_bg(self, delta_time: float):
        # Scroll speeds
        bg0_speed, bg1_speed, bg2_speed = 10,20,30
        # Scroll bg to left
        self.bg0_x -= bg0_speed * delta_time
        self.bg1_x -= bg1_speed * delta_time
        self.bg2_x -= bg2_speed * delta_time
        # Wrap
        bg_width = self.bg0.get_width()
        if self.bg0_x <= -bg_width:
            self.bg0_x = 0
        if self.bg1_x <= -bg_width:
            self.bg1_x = 0
        if self.bg2_x <= -bg_width:
            self.bg2_x = 0
    
    def draw_bg(self, surface: pygame.Surface):
        # Drawing each image a second time offset to remove scoll seams
        surface.blit(self.bg0, (self.bg0_x, 0))
        surface.blit(self.bg0, (self.bg0_x + self.bg0.get_width(), 0))
        surface.blit(self.bg1, (self.bg1_x, 0))
        surface.blit(self.bg1, (self.bg1_x + self.bg1.get_width(), 0))
        surface.blit(self.bg2, (self.bg2_x, 0))
        surface.blit(self.bg2, (self.bg2_x + self.bg2.get_width(), 0))
        
    def draw_ui(self, surface: pygame.Surface):
        # Big box
        big_box_x = (surface.get_width() - self.ui_big_box.get_width()) // 2
        big_box_y = int(surface.get_height() * 0.15)
        surface.blit(self.ui_big_box, (big_box_x, big_box_y))
        # Buttons
        button_x = big_box_x + (self.ui_big_box.get_width() - self.ui_button.get_width()) // 2
        total_button_height = self.ui_button.get_height() * 4
        spacing = (self.ui_big_box.get_height() - total_button_height) // 5
        button_y = big_box_y + spacing
        surface.blit(self.ui_play_button, (button_x, button_y))
        Text.draw_text(surface, "Play", (27, 34, 54), button_x + self.ui_button.get_width()//2, button_y + self.ui_button.get_height()//2 - 6)
        button_y += self.ui_button.get_height() + spacing
        surface.blit(self.ui_load_button, (button_x, button_y))
        Text.draw_text(surface, "Load", (27, 34, 54), button_x + self.ui_button.get_width()//2, button_y + self.ui_button.get_height()//2 - 6)
        button_y += self.ui_button.get_height() + spacing
        surface.blit(self.ui_options_button, (button_x, button_y))
        Text.draw_text(surface, "Options", (27, 34, 54), button_x + self.ui_button.get_width()//2, button_y + self.ui_button.get_height()//2 - 6)
        button_y += self.ui_button.get_height() + spacing
        surface.blit(self.ui_quit_button, (button_x, button_y))
        Text.draw_text(surface, "Quit", (27, 34, 54), button_x + self.ui_button.get_width()//2, button_y + self.ui_button.get_height()//2 - 6)