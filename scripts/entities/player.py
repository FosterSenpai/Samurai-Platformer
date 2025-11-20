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
        self.pixels_per_meter: float = 96.0
        self.gravity: float = 9.8 * self.pixels_per_meter # 9.8 m/s²
        self.speed: float = 1.0 * self.pixels_per_meter # 1 m/s
        self.jump_height_meters: float = 0.7
        self.jump_strength: float = (2.0 * self.gravity * self.jump_height_meters* self.pixels_per_meter) ** 0.5 # v = sqrt(2gh)
        
        self.is_on_ground: bool = False
        self.is_on_wall: bool = False
        self.is_hanging: bool = False
        
        # Blinking effect
        self.blink_count: int = 0
        self.max_blinks: int = 0
        self.blink_interval: float = 0.15
        self.blink_timer: float = 0.0
        self.alpha: int = 255
        self.blink(10) # Blink on spawn for effect
        
    def update(self, delta_time: float, actions: dict) -> None:
        self.handle_input(actions)
        self.update_blink(delta_time)
        
        # Apply gravity
        self.velocity_y += self.gravity * delta_time
        # Update position
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        # Apply dampening to horizontal movement
        self.velocity_x *= 0.9
        # Update position
        self.rect.center = (int(self.x), int(self.y))
        
        # Update animation
        self.update_animation(delta_time)
        
        # TEMP: fake ground at y=200
        if self.y >= 200:
            self.y = 200
            self.velocity_y = 0.0
            self.is_on_ground = True
        else:
            self.is_on_ground = False
    
    def handle_input(self, actions: dict) -> None:
        # Horizontal movement
        if actions.get('left'):
            self.velocity_x = -self.speed
            self.facing_right = False
            if self.is_on_ground:
                self.change_state('walk')
        elif actions.get('right'):
            self.velocity_x = self.speed
            self.facing_right = True
            if self.is_on_ground:
                self.change_state('walk')
        else:
            if self.is_on_ground and self.state == 'walk':
                self.change_state('idle')
            
        # Jumping
        if actions.get('jump') and self.is_on_ground:
            self.velocity_y = -self.jump_strength
            self.change_state('jump')
            
        # Attacks
        if actions.get('quick_attack'):
            if self.state == 'attack_1':
                self.change_state('attack_2')
            elif self.state == 'attack_2':
                self.change_state('attack_3')
            elif self.state != 'attack_3':
                self.change_state('attack_1')
            # TODO: Do some logic for combo timeing, reset if too long
        elif actions.get('special_attack'):
            self.change_state('special_attack')

                
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
        self.image = self.current_animation_frames[self.frame_index].copy()
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_alpha(self.alpha)
            
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
    
    def update_blink(self, delta_time: float) -> None:
        if self.max_blinks > 0:
            self.blink_timer += delta_time
            # Toggle alpha
            if self.blink_timer >= self.blink_interval:
                self.blink_timer = 0.0
                self.blink_count += 1
                self.alpha = 190 if self.alpha == 255 else 255
                # Stop after max blinks
                if self.blink_count >= self.max_blinks:
                    self.max_blinks = 0
                    self.blink_count = 0
                    self.image.set_alpha(255)
                    
    def blink(self, num_blinks: int) -> None:
        self.max_blinks = num_blinks
        self.blink_count = 0
        self.blink_timer = 0.0