# title_state.py
# Title screen state for the game.
# Author: Foster Rae
# Created: 23-10-2025
import pygame
from scripts.screen_states.screen_state import State
from scripts.screen_states.game_state import GameState
from scripts.utilities.text import Text
from scripts.utilities.asset_manager import AssetManager
from scripts.components.ui_components.button import Button

class TitleState(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        canvas_w, canvas_h = self.game.GAME_W, self.game.GAME_H
        
        # UI elements
        # Container config
        big_box_width: int = int(canvas_w * 0.35)
        big_box_height: int = int(canvas_h * 0.8)
        self.ui_big_box: pygame.Surface = pygame.transform.scale(AssetManager.core_sprites['ui_sprite159'], (big_box_width, big_box_height))
        self.big_box_x: int = int((canvas_w - big_box_width) // 2)
        self.big_box_y: int = int(canvas_h * 0.15)
        # Button config
        menu_button_width = int(big_box_width * 0.7)
        menu_button_height = int(big_box_height * 0.15)
        self.ui_button_sprite: pygame.Surface = pygame.transform.scale(AssetManager.core_sprites['ui_sprite205'], (menu_button_width, menu_button_height))
        self.ui_button_sprite_active: pygame.Surface = pygame.transform.scale(AssetManager.core_sprites['ui_sprite206'], (menu_button_width, menu_button_height))
        button_x = self.big_box_x + (big_box_width - self.ui_button_sprite.get_width()) // 2
        total_button_height = self.ui_button_sprite.get_height() * 4
        spacing = (self.ui_big_box.get_height() - total_button_height) // 5
        button_y = self.big_box_y + spacing
        # Buttons
        self.button_play: Button = Button(pos=(button_x, button_y), display_text="Play", callback=self.on_play_clicked,image=self.ui_button_sprite)
        self.button_load: Button = Button(pos=(button_x, button_y + (menu_button_height + spacing)*1), display_text="Load", callback=self.on_load_clicked, image=self.ui_button_sprite)
        self.button_options: Button = Button(pos=(button_x, button_y + (menu_button_height + spacing)*2), display_text="Options", callback=self.on_options_clicked, image=self.ui_button_sprite)
        self.button_quit: Button = Button(pos=(button_x, button_y + (menu_button_height + spacing)*3), display_text="Quit", callback=self.on_quit_clicked, image=self.ui_button_sprite)
        self.buttons: list[Button] = [self.button_play, self.button_load, self.button_options, self.button_quit]
        # Background
        self.bg0: pygame.Surface = AssetManager.core_sprites['bg0']
        self.bg1: pygame.Surface = AssetManager.core_sprites['bg1']
        self.bg2: pygame.Surface = AssetManager.core_sprites['bg2']
        self.bg0_x: float = 0.0 # Bg x positions for scrolling
        self.bg1_x: float = 0.0
        self.bg2_x: float = 0.0
        
    def on_enter(self):
        AssetManager.play_music('Evening Mood', volume=0.5)
        
    def on_resume(self):
        AssetManager.play_music('Evening Mood', volume=0.5)

    def update(self, delta_time: float, actions: dict) -> None:
        # Update background
        self.scroll_bg(delta_time)
        # Update buttons
        mouse_pos = self.game.get_mouse_position()
        mouse_pressed = pygame.mouse.get_pressed()[0] # Left click
        for button in self.buttons:
            button.update(mouse_pos, mouse_pressed)
    
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
        # Big box (looks better without)
        # surface.blit(self.ui_big_box, (self.big_box_x, self.big_box_y))
        # Buttons
        for button in self.buttons:
            button.draw(surface)
        
    def on_play_clicked(self):
        # Creatiing and switching to GameState
        game_state = GameState(self.game)
        game_state.enter_state()
        
        
    def on_load_clicked(self):
        print("Load button clicked, Implement load game logic here.")
        
    def on_options_clicked(self):
        print("Options button clicked, Implement options menu logic here.")
    
    def on_quit_clicked(self):
        self.game.playing = False
        self.game.running = False