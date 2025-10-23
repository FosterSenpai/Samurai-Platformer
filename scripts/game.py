# game.py
# Game class that brings all modules together and runs the main gameplay loop.
# Author: Foster Rae
# Created: 18-10-2025
# Last Modified: 23-10-2025
import os, time, pygame
from scripts.config import Config
from scripts.components.player_controller import PlayerController
from scripts.utilities.asset_manager import AssetManager
from scripts.screen_states.title_state import TitleState
class Game():
    def __init__(self):
        pygame.init()
        AssetManager.load_core_assets()
        # Screen
        self.GAME_W, self.GAME_H = Config.GAME_W, Config.GAME_H
        self.SCREEN_W, self.SCREEN_H = Config.SCREEN_W, Config.SCREEN_H
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.fps = Config.FPS
        self.screen_state_stack = []
        # Timing
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        # Others
        self.running, self.playing = True, True
        self.controller = PlayerController()
        
        self.load_states()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            self.controller.handle_input(event)
    
    def update(self):
        self.dt = self.clock.tick(self.fps) / 1000.0
        self.screen_state_stack[-1].update(self.dt, self.controller.actions)
    
    def render(self):
        self.screen_state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_W,self.SCREEN_H)), (0,0))
        pygame.display.flip()
        
    def game_loop(self):
        while self.playing:
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()
            
    def load_states(self):
        # Load title screen first
        self.title_screen = TitleState(self)
        self.screen_state_stack.append(self.title_screen)
                
            
                