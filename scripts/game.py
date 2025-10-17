import os, time, pygame
from scripts.config import Config
from scripts.components.player_controller import PlayerController
class Game():
    def __init__(self):
        pygame.init()
        self.GAME_W, self.GAME_H = Config.GAME_W, Config.GAME_H
        self.SCREEN_W, self.SCREEN_H = Config.SCREEN_W, Config.SCREEN_H
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.running, self.playing = False, False
        self.controller = PlayerController()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                pygame.quit()
            self.controller.handle_input(event)
    
    def update(self):
        # Update game state here
        pass
    
    def render(self):
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_W,self.SCREEN_H)), (0,0))
        pygame.display.flip()
        
    def run(self):
        pass
                
            
                