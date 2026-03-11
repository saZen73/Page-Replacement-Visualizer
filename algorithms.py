"""
Page replacement algorithm implementations
"""

import time
from typing import List
from collections import deque

from models import PageFaultResult


class PageReplacementAlgorithm:
    """Base class for page replacement algorithms"""
    
    def __init__(self, pages: List[int], num_frames: int):
        """
        Initialize algorithm with page reference string and frame count.
        
        Args:
            pages: List of page references
            num_frames: Number of available frames
        """
        self.pages = pages
        self.num_frames = num_frames
        self.num_pages = len(pages)
        
    def execute(self) -> PageFaultResult:
        """
        Execute the algorithm and return results.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def _calculate_metrics(self, faults: int, hits: int, exec_time: float,
                          frame_states: List[List[int]], 
                          fault_indicators: List[bool]) -> PageFaultResult:
        """Calculate and return performance metrics"""
        total = self.num_pages
        fault_ratio = faults / total if total > 0 else 0
        hit_ratio = hits / total if total > 0 else 0
        
        return PageFaultResult(
            algorithm_name=self.__class__.__name__,
            total_faults=faults,
            total_hits=hits,
            fault_ratio=fault_ratio,
            hit_ratio=hit_ratio,
            frame_states=frame_states,
            fault_indicators=fault_indicators,
            execution_time=exec_time
        )


class FIFOAlgorithm(PageReplacementAlgorithm):
    """First In First Out (FIFO) page replacement algorithm"""
    
    def execute(self) -> PageFaultResult:
        """Execute FIFO algorithm"""
        start_time = time.time()
        
        frames = deque(maxlen=self.num_frames)
        frame_states = []
        fault_indicators = []
        page_faults = 0
        
        for page in self.pages:
            if page not in frames:
                # Page fault occurs
                if len(frames) >= self.num_frames:
                    frames.popleft()  # Remove oldest page
                frames.append(page)
                page_faults += 1
                fault_indicators.append(True)
            else:
                # Page hit
                fault_indicators.append(False)
            
            # Store current frame state
            frame_states.append(list(frames))
        
        exec_time = (time.time() - start_time) * 1000  # Convert to ms
        hits = self.num_pages - page_faults
        
        return self._calculate_metrics(page_faults, hits, exec_time, 
                                       frame_states, fault_indicators)


class LRUAlgorithm(PageReplacementAlgorithm):
    """Least Recently Used (LRU) page replacement algorithm"""
    
    def execute(self) -> PageFaultResult:
        """Execute LRU algorithm"""
        start_time = time.time()
        
        frames = []  # Stores pages in order of usage (most recent at end)
        frame_states = []
        fault_indicators = []
        page_faults = 0
        
        for page in self.pages:
            if page in frames:
                # Page hit - move to end (most recently used)
                frames.remove(page)
                frames.append(page)
                fault_indicators.append(False)
            else:
                # Page fault
                if len(frames) >= self.num_frames:
                    frames.pop(0)  # Remove least recently used (first element)
                frames.append(page)
                page_faults += 1
                fault_indicators.append(True)
            
            # Store current frame state
            frame_states.append(list(frames))
        
        exec_time = (time.time() - start_time) * 1000
        hits = self.num_pages - page_faults
        
        return self._calculate_metrics(page_faults, hits, exec_time, 
                                       frame_states, fault_indicators)


class OptimalAlgorithm(PageReplacementAlgorithm):
    """Optimal page replacement algorithm"""
    
    def execute(self) -> PageFaultResult:
        """Execute Optimal algorithm"""
        start_time = time.time()
        
        frames = []
        frame_states = []
        fault_indicators = []
        page_faults = 0
        
        for i, page in enumerate(self.pages):
            if page in frames:
                # Page hit
                fault_indicators.append(False)
            else:
                # Page fault
                if len(frames) >= self.num_frames:
                    # Find page to replace
                    replace_idx = self._find_optimal_replacement(frames, i)
                    frames[replace_idx] = page
                else:
                    frames.append(page)
                page_faults += 1
                fault_indicators.append(True)
            
            # Store current frame state
            frame_states.append(list(frames))
        
        exec_time = (time.time() - start_time) * 1000
        hits = self.num_pages - page_faults
        
        return self._calculate_metrics(page_faults, hits, exec_time, 
                                       frame_states, fault_indicators)
    
    def _find_optimal_replacement(self, frames: List[int], current_idx: int) -> int:
        """
        Find the optimal page to replace.
        
        Returns the index in frames of the page that will be used
        furthest in the future (or not at all).
        """
        future_pages = self.pages[current_idx + 1:]
        farthest_use = -1
        replace_idx = 0
        
        for idx, frame_page in enumerate(frames):
            try:
                # Find next use of this page
                next_use = future_pages.index(frame_page)
            except ValueError:
                # Page not used again - optimal choice
                return idx
            
            if next_use > farthest_use:
                farthest_use = next_use
                replace_idx = idx
        
        return replace_idx
