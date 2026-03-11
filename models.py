"""
Data models for Page Replacement Visualizer
"""

from dataclasses import dataclass
from typing import List


@dataclass
class PageFaultResult:
    """Stores the results of a page replacement algorithm execution"""
    algorithm_name: str
    total_faults: int
    total_hits: int
    fault_ratio: float
    hit_ratio: float
    frame_states: List[List[int]]  # State of frames at each step
    fault_indicators: List[bool]  # True if fault occurred at step i
    execution_time: float  # In milliseconds
