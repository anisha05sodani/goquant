from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, 
                            QComboBox, QPushButton, QLabel)
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any

class PerformancePlot(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackground('w')
        self.showGrid(x=True, y=True)
        self.setLabel('left', 'Value')
        self.setLabel('bottom', 'Time')
        
    def update_data(self, data: pd.DataFrame, x_col: str, y_col: str):
        self.clear()
        self.plot(data[x_col], data[y_col], pen='b')
        
class TradingVisualization(QWidget):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Time range selection
        time_range_layout = QHBoxLayout()
        self.time_range_combo = QComboBox()
        self.time_range_combo.addItems(['1h', '4h', '1d', '1w', '1m'])
        self.time_range_combo.currentTextChanged.connect(self._update_plots)
        time_range_layout.addWidget(QLabel("Time Range:"))
        time_range_layout.addWidget(self.time_range_combo)
        layout.addLayout(time_range_layout)
        
        # Create tab widget for different plots
        self.tab_widget = QTabWidget()
        
        # Performance metrics tab
        self.performance_tab = QWidget()
        performance_layout = QVBoxLayout(self.performance_tab)
        self.processing_time_plot = PerformancePlot()
        self.ui_update_plot = PerformancePlot()
        self.ws_latency_plot = PerformancePlot()
        performance_layout.addWidget(self.processing_time_plot)
        performance_layout.addWidget(self.ui_update_plot)
        performance_layout.addWidget(self.ws_latency_plot)
        self.tab_widget.addTab(self.performance_tab, "Performance")
        
        # Trading metrics tab
        self.trading_tab = QWidget()
        trading_layout = QVBoxLayout(self.trading_tab)
        self.slippage_plot = PerformancePlot()
        self.impact_plot = PerformancePlot()
        self.cost_plot = PerformancePlot()
        trading_layout.addWidget(self.slippage_plot)
        trading_layout.addWidget(self.impact_plot)
        trading_layout.addWidget(self.cost_plot)
        self.tab_widget.addTab(self.trading_tab, "Trading")
        
        # Orderbook metrics tab
        self.orderbook_tab = QWidget()
        orderbook_layout = QVBoxLayout(self.orderbook_tab)
        self.spread_plot = PerformancePlot()
        self.depth_plot = PerformancePlot()
        self.volume_plot = PerformancePlot()
        orderbook_layout.addWidget(self.spread_plot)
        orderbook_layout.addWidget(self.depth_plot)
        orderbook_layout.addWidget(self.volume_plot)
        self.tab_widget.addTab(self.orderbook_tab, "Orderbook")
        
        layout.addWidget(self.tab_widget)
        
    def _update_plots(self):
        """Update all plots with new data"""
        time_range = self.time_range_combo.currentText()
        end_time = datetime.now()
        
        # Calculate start time based on selected range
        if time_range == '1h':
            start_time = end_time - timedelta(hours=1)
        elif time_range == '4h':
            start_time = end_time - timedelta(hours=4)
        elif time_range == '1d':
            start_time = end_time - timedelta(days=1)
        elif time_range == '1w':
            start_time = end_time - timedelta(weeks=1)
        else:  # 1m
            start_time = end_time - timedelta(days=30)
        
        # Get historical data
        data = self.storage.get_historical_data(start_time, end_time)
        
        # Update performance plots
        self.processing_time_plot.update_data(
            data['performance'], 'timestamp', 'avg_processing_time'
        )
        self.ui_update_plot.update_data(
            data['performance'], 'timestamp', 'avg_ui_update_time'
        )
        self.ws_latency_plot.update_data(
            data['performance'], 'timestamp', 'avg_ws_latency'
        )
        
        # Update trading plots
        self.slippage_plot.update_data(
            data['trading'], 'timestamp', 'slippage'
        )
        self.impact_plot.update_data(
            data['trading'], 'timestamp', 'impact'
        )
        self.cost_plot.update_data(
            data['trading'], 'timestamp', 'net_cost'
        )
        
        # Update orderbook plots
        self.spread_plot.update_data(
            data['orderbook'], 'timestamp', 'spread'
        )
        self.depth_plot.update_data(
            data['orderbook'], 'timestamp', 'depth'
        )
        self.volume_plot.update_data(
            data['orderbook'], 'timestamp', 'volume'
        ) 