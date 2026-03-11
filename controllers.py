"""
Animation controller for managing visualization state
"""

import time

from constants import AnimationSpeed


class AnimationController:
    """Controls animation state and speed"""
    
    def __init__(self):
        self.is_paused = False
        self.is_stopped = False
        self.is_restarting = False
        self.speed = AnimationSpeed.MEDIUM
        self.current_step = 0
        
    def reset(self):
        """Reset controller state"""
        self.is_paused = False
        self.is_stopped = False
        self.is_restarting = False
        self.current_step = 0
    
    def pause(self):
        """Pause animation"""
        self.is_paused = True
    
    def resume(self):
        """Resume animation"""
        self.is_paused = False
    
    def stop(self):
        """Stop animation"""
        self.is_stopped = True
    
    def restart(self):
        """Restart animation from beginning"""
        self.is_restarting = True
        self.is_paused = False
        self.is_stopped = False
        self.current_step = 0
    
    def set_speed(self, speed: AnimationSpeed):
        """Set animation speed"""
        self.speed = speed
    
    def wait(self):
        """Wait for the appropriate time based on speed"""
        if self.speed != AnimationSpeed.INSTANT:
            time.sleep(self.speed.value)
