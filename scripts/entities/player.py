# player.py
# The class for the player entity, handles player stats and rendering.
# Author: Foster Rae
# Created: 18-10-2025
# Last Modified: 18-10-2025
from typing import Optional
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
        self.previous_state: str = 'idle'
        self.is_one_shot_animation: bool = False
        self.hold_final_frame: bool = False
        self.frame_index: int = 0
        self.animation_timer: float = 0.0
        self.animation_speed: float = 0.05 # seconds per frame
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
        self.air_control: float = 0.7 # 70% control in air
        self.jump_height_meters: float = 0.7
        self.jump_strength: float = (2.0 * self.gravity * self.jump_height_meters* self.pixels_per_meter) ** 0.5 # v = sqrt(2gh)
        
        self.is_on_ground: bool = False
        self.is_on_wall: bool = False
        self.is_hanging: bool = False
        
        # Combo system
        self.can_combo: bool = False
        self.attack_buffer: Optional[str] = None # Buffer for next attack input
        
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
        
        self.check_ground_collision()
        
        # Update position
        self.rect.center = (int(self.x), int(self.y))
        
        self.update_jump(delta_time)
        
        
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
        # Attacks
        if actions.get('quick_attack'):
            # queue next attack if pressed during quick attack
            if self.state in ['attack 1', 'attack 2']: # chaining attacks
                self.attack_buffer = 'next_attack' # just a flag
                actions['quick_attack'] = False # need to reset to avoid triggers
            elif self.state != 'attack 3': # first attack
                self.change_state('attack 1')
                actions['quick_attack'] = False
        elif actions.get('special_attack'):
            self.change_state('special attack')
            actions['special_attack'] = False
            
        # Dont interrupt one-shot animations
        if self.is_one_shot_animation:
            return
            
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
            self.change_state('jump start')
            
    def update_jump(self, delta_time: float) -> None:
        if not self.is_on_ground:
            # Run through 'jump start' frames, hold final frame
            # at apex of jump switch to 'jump transition' play through then change to 'fall' and hold final frame
            if self.state == 'jump start':
                # Change to 'jump transition' if at final frame and y vel is near 0
                if self.frame_index >= len(self.current_animation_frames) - 1 and abs(self.velocity_y) < 30:
                    self.change_state('jump transition')
            elif self.state == 'jump transition':
                # Change to 'fall' if at final frame
                if self.frame_index >= len(self.current_animation_frames) - 1:
                    self.change_state('jump fall')
        else:
            # Landed
            if self.state in ['jump start', 'jump transition', 'jump fall']:
                if abs(self.velocity_x) > 10:
                    self.change_state('walk')
                else:
                    self.change_state('idle')
    
    def check_ground_collision(self) -> None:
        # Should maybe check if bottom pixels overlap any environment tiles in a sprite group or something
        # TEMP, setting on ground if y >= 200
        if self.y >= 200:
            self.is_on_ground = True
        else:
            self.is_on_ground = False
                
    def change_state(self, new_state: str) -> None:
        if new_state != self.state:
            # Storing previous state to revert back to after one-shot animations
            if not self.is_one_shot_animation:
                self.previous_state = self.state
            # Change state and reset animation stuff
            self.state = new_state
            self.frame_index = 0
            self.animation_timer = 0.0
            self.current_animation_frames = AssetManager.player_animations[self.state]
            self.image = self.current_animation_frames[self.frame_index]
            
            # Reset combo system
            self.can_combo = False
            self.attack_buffer = None
            
            # Update one-shot flag
            if self.state in ['attack 1', 'attack 2', 'attack 3', 'special attack']: # one-shot animations
                self.is_one_shot_animation = True
            elif self.state in ['jump start', 'jump fall']: # hold final frame animations
                self.is_one_shot_animation = False
                self.hold_final_frame = True
            else:
                self.is_one_shot_animation = False
                self.hold_final_frame = False
                
    def update_animation(self, delta_time: float) -> None:
        # Hold final frame animations
        if self.hold_final_frame and self.frame_index >= len(self.current_animation_frames) - 1:
            self.frame_index = len(self.current_animation_frames) - 1
        else:
            # Increment frame index
            self.animation_timer += delta_time
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.frame_index += 1
                
            # Enable combo window in last 20% of attack animation
                if self.state in ['attack 1', 'attack 2']:
                    combo_window_frame = int(len(self.current_animation_frames) * 0.8)
                    if self.frame_index >= combo_window_frame:
                        self.can_combo = True
                
            # Check if animation finished
            if self.frame_index >= len(self.current_animation_frames):
                if self.is_one_shot_animation:
                    if self.attack_buffer == 'next_attack':
                        # Chain to next attack
                        if self.state == 'attack 1':
                            self.change_state('attack 2')
                        elif self.state == 'attack 2':
                            self.change_state('attack 3')
                    else:
                        # Revert to previous state
                        self.change_state(self.previous_state)
                        self.frame_index = 0
                else:
                    # Loop animation
                    self.frame_index = 0
            
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