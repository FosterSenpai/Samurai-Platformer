# game.py
# Game class that brings all modules together and runs the main gameplay loop.
# Author: Foster Rae
# Created: 18-10-2025
# Last Modified: 18-10-2025
import os, time, pygame
from scripts.config import Config
from scripts.components.player_controller import PlayerController
from scripts.utilities.asset_manager import AssetManager

class Game():
    def __init__(self):
        pygame.init()
        # Screen
        self.GAME_W, self.GAME_H = Config.GAME_W, Config.GAME_H
        self.SCREEN_W, self.SCREEN_H = Config.SCREEN_W, Config.SCREEN_H
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.fps = Config.FPS
        self.screen_state_stack = []
        # Timing
        self.clock = pygame.time.Clock()
        # Others
        self.running, self.playing = True, True
        self.controller = PlayerController()
        
        AssetManager.load_core_assets()
        # TEMPORARY, REMOVE
        AssetManager.load_level_assets('stringstar_fields')
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                pygame.quit()
            self.controller.handle_input(event)
    
    def update(self):
        self.clock.tick(self.fps)
    
    def render(self):
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_W,self.SCREEN_H)), (0,0))
        pygame.display.flip()
        
    def game_loop(self):
        while self.playing:
            self.handle_events()
            self.update()
            self.render()
                
            
                