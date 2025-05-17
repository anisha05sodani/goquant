from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox,
                            QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from models.market_impact import AlmgrenChrissModel, MarketImpactParams
from models.slippage import SlippageEstimator
from models.maker_taker import MakerTakerPredictor
import time
from core.performance import PerformanceAnalyzer
from core.logger import TradingLogger
from config.settings import TradingConfig
from .visualization import TradingVisualization
from core.storage import TradingDataStorage

class MainWindow(QMainWindow):
    # Define signals for async updates
    update_metrics = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoQuant Trading Simulator")
        self.setMinimumSize(1200, 800)
        
        # Initialize models
        self.market_impact_model = None
        self.slippage_estimator = SlippageEstimator()
        self.maker_taker_predictor = MakerTakerPredictor()
        
        # Performance tracking
        self.last_update_time = time.time()
        self.processing_times = []
        
        # Initialize components
        self.config = TradingConfig()
        self.logger = TradingLogger()
        self.performance_analyzer = PerformanceAnalyzer(
            window_size=self.config.performance_window
        )
        
        # Initialize storage and visualization
        self.storage = TradingDataStorage()
        self.visualization = TradingVisualization(self.storage)
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Create left panel (Input Parameters)
        left_panel = self._create_input_panel()
        
        # Create right panel (Output Parameters)
        right_panel = self._create_output_panel()
        
        # Add panels to main layout
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)
        
        # Add visualization to main layout
        layout.addWidget(self.visualization)
        
    def _create_input_panel(self) -> QWidget:
        panel = QGroupBox("Input Parameters")
        layout = QVBoxLayout(panel)
        
        # Exchange selection
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItem("OKX")
        layout.addWidget(QLabel("Exchange:"))
        layout.addWidget(self.exchange_combo)
        
        # Asset selection
        self.asset_combo = QComboBox()
        self.asset_combo.addItem("BTC-USDT-SWAP")
        layout.addWidget(QLabel("Asset:"))
        layout.addWidget(self.asset_combo)
        
        # Order type
        self.order_type_combo = QComboBox()
        self.order_type_combo.addItem("market")
        layout.addWidget(QLabel("Order Type:"))
        layout.addWidget(self.order_type_combo)
        
        # Quantity input
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity (USD)")
        self.quantity_input.setText("100")  # Default value
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.quantity_input)
        
        # Volatility input
        self.volatility_input = QLineEdit()
        self.volatility_input.setPlaceholderText("Volatility")
        self.volatility_input.setText("0.02")  # Default value
        layout.addWidget(QLabel("Volatility:"))
        layout.addWidget(self.volatility_input)
        
        # Fee tier selection
        self.fee_tier_combo = QComboBox()
        self.fee_tier_combo.addItems(["Tier 1", "Tier 2", "Tier 3"])
        layout.addWidget(QLabel("Fee Tier:"))
        layout.addWidget(self.fee_tier_combo)
        
        # Add start/stop button
        self.control_button = QPushButton("Start Simulation")
        layout.addWidget(self.control_button)
        
        layout.addStretch()
        return panel
        
    def _create_output_panel(self) -> QWidget:
        panel = QGroupBox("Output Parameters")
        layout = QVBoxLayout(panel)
        
        # Create output labels
        self.slippage_label = QLabel("Expected Slippage: --")
        self.fees_label = QLabel("Expected Fees: --")
        self.impact_label = QLabel("Market Impact: --")
        self.net_cost_label = QLabel("Net Cost: --")
        self.maker_taker_label = QLabel("Maker/Taker: --")
        self.latency_label = QLabel("Internal Latency: --")
        
        # Add labels to layout
        layout.addWidget(self.slippage_label)
        layout.addWidget(self.fees_label)
        layout.addWidget(self.impact_label)
        layout.addWidget(self.net_cost_label)
        layout.addWidget(self.maker_taker_label)
        layout.addWidget(self.latency_label)
        
        # Add performance metrics
        performance_group = QGroupBox("Performance Metrics")
        perf_layout = QVBoxLayout(performance_group)
        
        self.avg_processing_time = QLabel("Avg Processing Time: --")
        self.avg_ui_update_time = QLabel("Avg UI Update Time: --")
        self.total_ticks = QLabel("Total Ticks Processed: 0")
        
        perf_layout.addWidget(self.avg_processing_time)
        perf_layout.addWidget(self.avg_ui_update_time)
        perf_layout.addWidget(self.total_ticks)
        
        layout.addWidget(performance_group)
        layout.addStretch()
        
        return panel
        
    def _connect_signals(self):
        """Connect UI signals to slots"""
        self.control_button.clicked.connect(self._toggle_simulation)
        self.update_metrics.connect(self._update_metrics)
        
    def _toggle_simulation(self):
        """Toggle simulation start/stop"""
        if self.control_button.text() == "Start Simulation":
            self.control_button.setText("Stop Simulation")
            # TODO: Start WebSocket connection
        else:
            self.control_button.setText("Start Simulation")
            # TODO: Stop WebSocket connection
            
    def _update_metrics(self, metrics: dict):
        """Update UI with new metrics"""
        start_time = self.performance_analyzer.start_ui_update()
        
        try:
            # Update output labels
            self.slippage_label.setText(f"Expected Slippage: {metrics.get('slippage', '--')} bps")
            self.fees_label.setText(f"Expected Fees: {metrics.get('fees', '--')} USD")
            self.impact_label.setText(f"Market Impact: {metrics.get('impact', '--')} bps")
            self.net_cost_label.setText(f"Net Cost: {metrics.get('net_cost', '--')} USD")
            self.maker_taker_label.setText(f"Maker/Taker: {metrics.get('maker_taker', '--')}%")
            self.latency_label.setText(f"Internal Latency: {metrics.get('processing_time', '--')} ms")
            
            # Update performance metrics
            perf_report = self.performance_analyzer.get_performance_report()
            stats = perf_report['statistics']
            
            self.avg_processing_time.setText(
                f"Avg Processing Time: {stats['avg_processing_time']:.2f} ms"
            )
            self.avg_ui_update_time.setText(
                f"Avg UI Update Time: {stats['avg_ui_update_time']:.2f} ms"
            )
            self.total_ticks.setText(
                f"Total Ticks Processed: {perf_report['total_ticks']}"
            )
            
            # Save metrics to storage
            self.storage.save_trading_metrics(metrics)
            self.storage.save_performance_metrics(
                self.performance_analyzer.get_performance_report()
            )
            
            # Update visualization
            self.visualization._update_plots()
            
        except Exception as e:
            self.logger.ui_logger.error(f"Error updating metrics: {str(e)}")
            self.performance_analyzer.record_error()
        finally:
            self.performance_analyzer.end_ui_update(start_time)

    def show_error(self, message: str):
        """Show error message to user"""
        QMessageBox.critical(self, "Error", message) 