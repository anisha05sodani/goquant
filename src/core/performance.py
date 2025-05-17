from dataclasses import dataclass
from typing import List, Dict
import time
import statistics
from collections import deque

@dataclass
class PerformanceMetrics:
    processing_times: deque
    ui_update_times: deque
    ws_latency: deque
    total_ticks: int
    errors: int
    
    def __init__(self, window_size: int = 100):
        self.processing_times = deque(maxlen=window_size)
        self.ui_update_times = deque(maxlen=window_size)
        self.ws_latency = deque(maxlen=window_size)
        self.total_ticks = 0
        self.errors = 0
    
    def add_processing_time(self, time_ms: float):
        self.processing_times.append(time_ms)
        self.total_ticks += 1
    
    def add_ui_update_time(self, time_ms: float):
        self.ui_update_times.append(time_ms)
    
    def add_ws_latency(self, latency_ms: float):
        self.ws_latency.append(latency_ms)
    
    def increment_errors(self):
        self.errors += 1
    
    def get_statistics(self) -> Dict[str, float]:
        """Calculate performance statistics"""
        stats = {
            'avg_processing_time': statistics.mean(self.processing_times) if self.processing_times else 0,
            'max_processing_time': max(self.processing_times) if self.processing_times else 0,
            'avg_ui_update_time': statistics.mean(self.ui_update_times) if self.ui_update_times else 0,
            'avg_ws_latency': statistics.mean(self.ws_latency) if self.ws_latency else 0,
            'error_rate': self.errors / self.total_ticks if self.total_ticks > 0 else 0
        }
        return stats

class PerformanceAnalyzer:
    def __init__(self, window_size: int = 100):
        self.metrics = PerformanceMetrics(window_size)
        self.start_time = time.time()
    
    def start_processing(self) -> float:
        """Start timing a processing operation"""
        return time.time()
    
    def end_processing(self, start_time: float):
        """End timing a processing operation"""
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        self.metrics.add_processing_time(processing_time)
    
    def start_ui_update(self) -> float:
        """Start timing a UI update"""
        return time.time()
    
    def end_ui_update(self, start_time: float):
        """End timing a UI update"""
        ui_time = (time.time() - start_time) * 1000  # Convert to ms
        self.metrics.add_ui_update_time(ui_time)
    
    def record_ws_latency(self, latency_ms: float):
        """Record WebSocket latency"""
        self.metrics.add_ws_latency(latency_ms)
    
    def record_error(self):
        """Record an error occurrence"""
        self.metrics.increment_errors()
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""
        stats = self.metrics.get_statistics()
        uptime = time.time() - self.start_time
        
        return {
            'statistics': stats,
            'uptime_seconds': uptime,
            'ticks_per_second': self.metrics.total_ticks / uptime if uptime > 0 else 0,
            'total_ticks': self.metrics.total_ticks,
            'total_errors': self.metrics.errors
        } 