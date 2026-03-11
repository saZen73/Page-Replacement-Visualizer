"""
Constants and configuration for Page Replacement Visualizer
"""

from enum import Enum


class AnimationSpeed(Enum):
    """Animation speed presets"""
    SLOW = 1.5
    MEDIUM = 0.7
    FAST = 0.3
    INSTANT = 0.0


# Color scheme
COLORS = {
    'primary': '#2b2d42',
    'secondary': '#8d99ae',
    'accent': '#ef233c',
    'success': '#06a77d',
    'warning': '#f77f00',
    'background': '#f0f4f7',
    'card': '#ffffff',
    'text': '#2b2d42',
    'hit': '#06a77d',
    'fault': '#ef233c',
}

# Font configuration
FONT_FAMILY = "Segoe UI"

# Application limits
MAX_FRAMES = 10
MAX_PAGES = 50
