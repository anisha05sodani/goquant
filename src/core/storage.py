import sqlite3
from datetime import datetime
import json
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path

class TradingDataStorage:
    def __init__(self, db_path: str = "data/trading.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS orderbook_snapshots (
                    timestamp TEXT,
                    exchange TEXT,
                    symbol TEXT,
                    mid_price REAL,
                    spread REAL,
                    depth REAL,
                    volume REAL,
                    data TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trading_metrics (
                    timestamp TEXT,
                    slippage REAL,
                    fees REAL,
                    impact REAL,
                    net_cost REAL,
                    maker_taker REAL,
                    processing_time REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    timestamp TEXT,
                    avg_processing_time REAL,
                    avg_ui_update_time REAL,
                    avg_ws_latency REAL,
                    error_rate REAL,
                    ticks_per_second REAL
                )
            """)
    
    def save_orderbook_snapshot(self, snapshot: Dict[str, Any]):
        """Save orderbook snapshot to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO orderbook_snapshots 
                (timestamp, exchange, symbol, mid_price, spread, depth, volume, data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                snapshot['timestamp'],
                snapshot['exchange'],
                snapshot['symbol'],
                snapshot['mid_price'],
                snapshot['spread'],
                snapshot['depth'],
                snapshot['volume'],
                json.dumps(snapshot['data'])
            ))
    
    def save_trading_metrics(self, metrics: Dict[str, Any]):
        """Save trading metrics to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO trading_metrics 
                (timestamp, slippage, fees, impact, net_cost, maker_taker, processing_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                float(metrics['slippage']),
                float(metrics['fees']),
                float(metrics['impact']),
                float(metrics['net_cost']),
                float(metrics['maker_taker']),
                float(metrics['processing_time'])
            ))
    
    def save_performance_metrics(self, metrics: Dict[str, Any]):
        """Save performance metrics to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO performance_metrics 
                (timestamp, avg_processing_time, avg_ui_update_time, 
                 avg_ws_latency, error_rate, ticks_per_second)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                metrics['statistics']['avg_processing_time'],
                metrics['statistics']['avg_ui_update_time'],
                metrics['statistics']['avg_ws_latency'],
                metrics['statistics']['error_rate'],
                metrics['ticks_per_second']
            ))
    
    def get_historical_data(self, 
                          start_time: datetime, 
                          end_time: datetime) -> Dict[str, pd.DataFrame]:
        """Retrieve historical data for analysis"""
        with sqlite3.connect(self.db_path) as conn:
            orderbook_data = pd.read_sql_query("""
                SELECT * FROM orderbook_snapshots 
                WHERE timestamp BETWEEN ? AND ?
            """, conn, params=(start_time.isoformat(), end_time.isoformat()))
            
            trading_metrics = pd.read_sql_query("""
                SELECT * FROM trading_metrics 
                WHERE timestamp BETWEEN ? AND ?
            """, conn, params=(start_time.isoformat(), end_time.isoformat()))
            
            performance_metrics = pd.read_sql_query("""
                SELECT * FROM performance_metrics 
                WHERE timestamp BETWEEN ? AND ?
            """, conn, params=(start_time.isoformat(), end_time.isoformat()))
        
        return {
            'orderbook': orderbook_data,
            'trading': trading_metrics,
            'performance': performance_metrics
        } 