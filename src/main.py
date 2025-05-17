import sys
import asyncio
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt
import qasync
import websockets

WS_URL = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoQuant Trading Simulator")
        self.setMinimumSize(1200, 800)
        self._setup_ui()

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        left_panel = self._create_input_panel()
        right_panel = self._create_output_panel()
        layout.addWidget(left_panel)
        layout.addWidget(right_panel)

    def _create_input_panel(self):
        panel = QGroupBox("Input Parameters")
        layout = QVBoxLayout(panel)
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItem("OKX")
        layout.addWidget(QLabel("Exchange:"))
        layout.addWidget(self.exchange_combo)
        self.asset_combo = QComboBox()
        self.asset_combo.addItem("BTC-USDT-SWAP")
        layout.addWidget(QLabel("Asset:"))
        layout.addWidget(self.asset_combo)
        self.order_type_combo = QComboBox()
        self.order_type_combo.addItem("market")
        layout.addWidget(QLabel("Order Type:"))
        layout.addWidget(self.order_type_combo)
        self.quantity_input = QLineEdit("100")
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.quantity_input)
        self.volatility_input = QLineEdit("0.02")
        layout.addWidget(QLabel("Volatility:"))
        layout.addWidget(self.volatility_input)
        self.fee_tier_combo = QComboBox()
        self.fee_tier_combo.addItems(["Tier 1", "Tier 2", "Tier 3"])
        layout.addWidget(QLabel("Fee Tier:"))
        layout.addWidget(self.fee_tier_combo)
        self.control_button = QPushButton("Start Simulation")
        layout.addWidget(self.control_button)
        layout.addStretch()
        return panel

    def _create_output_panel(self):
        panel = QGroupBox("Output Parameters")
        layout = QVBoxLayout(panel)
        self.status_label = QLabel("Status: Not started")
        layout.addWidget(self.status_label)
        self.slippage_label = QLabel("Expected Slippage: --")
        self.fees_label = QLabel("Expected Fees: --")
        self.impact_label = QLabel("Market Impact: --")
        self.net_cost_label = QLabel("Net Cost: --")
        self.maker_taker_label = QLabel("Maker/Taker: --")
        self.latency_label = QLabel("Internal Latency: --")
        layout.addWidget(self.slippage_label)
        layout.addWidget(self.fees_label)
        layout.addWidget(self.impact_label)
        layout.addWidget(self.net_cost_label)
        layout.addWidget(self.maker_taker_label)
        layout.addWidget(self.latency_label)
        layout.addStretch()
        return panel

    def update_outputs(self, data):
        # Dummy calculations for demonstration
        self.status_label.setText("Status: Receiving data")
        self.slippage_label.setText(f"Expected Slippage: {round(float(data['bids'][0][0]) * 0.0001, 4)} bps")
        self.fees_label.setText(f"Expected Fees: {round(float(self.quantity_input.text()) * 0.001, 4)} USD")
        self.impact_label.setText(f"Market Impact: {round(float(data['asks'][0][0]) * 0.0002, 4)} bps")
        self.net_cost_label.setText(f"Net Cost: {round(float(self.quantity_input.text()) * 1.001, 4)} USD")
        self.maker_taker_label.setText("Maker/Taker: 50/50")
        self.latency_label.setText("Internal Latency: <1ms")

async def run_websocket(window: MainWindow):
    window.status_label.setText("Status: Connecting...")
    try:
        async with websockets.connect(WS_URL) as ws:
            window.status_label.setText("Status: Connected!")
            async for message in ws:
                data = json.loads(message)
                window.update_outputs(data)
                await asyncio.sleep(0.1)
    except Exception as e:
        window.status_label.setText(f"Error: {e}")

def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()

    def on_start():
        asyncio.create_task(run_websocket(window))

    window.control_button.clicked.connect(on_start)

    with loop:
        loop.run_forever()

if __name__ == "__main__":
    main() 