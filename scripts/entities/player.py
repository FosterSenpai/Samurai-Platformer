# player.py
# The class for the player entity, handles player stats and rendering.
# Author: Foster Rae
# Created: 18-10-2025
# Last Modified: 18-10-2025
import pygame
from scripts.utilities.asset_manager import AssetManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        
        # Position, taking as floats for calculations, will probably need to be ints for rendering
        self.x: float = float(x)
        self.y: float = float(y)
        
        # Animation
        self.state: str = 'idle'
        self.frame_index: int = 0
        self.animation_timer: float = 0.0
        self.animation_speed: float = 0.1 # seconds per frame
        self.facing_right: bool = True
        
        # Frames
        self.current_animation_frames: list[pygame.Surface] = AssetManager.player_animations[self.state]
        self.image: pygame.Surface = self.current_animation_frames[self.frame_index]
        self.rect: pygame.Rect = self.image.get_rect(center=(self.x, self.y))
        
        # Player Physics
        self.velocity_y: float = 0.0
        self.velocity_x: float = 0.0
        self.gravity: float = 96 * 9.8 # Character is 96 pixels tall, ill say hes 1 meter, so gravity = 9.8 m/s²
        self.speed: float = 150.0 # pixels per second
        self.jump_strength: float = 350.0
        
        self.is_on_ground: bool = True
        self.is_on_wall: bool = False
        self.is_hanging: bool = False
        
    def update(self, delta_time: float, actions: dict) -> None:
        self.handle_input(actions)
        
        # Apply gravity
        #self.velocity_y += self.gravity * delta_time
        # Update position
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        # Apply dampening to horizontal movement
        self.velocity_x *= 0.9
        # Update position
        self.rect.center = (int(self.x), int(self.y))
        
        # Update animation
        self.update_animation(delta_time)
    
    def handle_input(self, actions: dict) -> None:
        if actions.get('left'):
            self.velocity_x = -self.speed
            self.facing_right = False
            self.change_state('walk')
        elif actions.get('right'):
            self.velocity_x = self.speed
            self.facing_right = True
            self.change_state('walk')
        elif actions.get('jump') and self.is_on_ground:
            self.velocity_y = -self.jump_strength
            self.change_state('jump')
        else:
            if self.is_on_ground:
                self.change_state('idle')
                
    def change_state(self, new_state: str) -> None:
        if new_state != self.state:
            self.state = new_state
            self.frame_index = 0
            self.animation_timer = 0.0
            self.current_animation_frames = AssetManager.player_animations[self.state]
            self.image = self.current_animation_frames[self.frame_index]
                
    def update_animation(self, delta_time: float) -> None:
        # Increment frame index
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(AssetManager.player_animations[self.state])
            
        # Update current image
        self.image = self.current_animation_frames[self.frame_index]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)