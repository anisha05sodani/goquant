import asyncio
import json
import logging
from typing import Optional, Callable, Dict, Any
import websockets
from websockets.exceptions import WebSocketException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketClient:
    def __init__(self, url: str):
        self.url = url
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.callback: Optional[Callable] = None
        self.running = False
        self.logger = logging.getLogger('websocket')

    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            self.websocket = await websockets.connect(self.url)
            self.logger.info(f"Connected to {self.url}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            return False

    async def subscribe(self):
        """Subscribe to the orderbook feed."""
        if not self.websocket:
            raise RuntimeError("WebSocket not connected")
        
        # Add subscription message if required by the exchange
        # await self.websocket.send(json.dumps({"op": "subscribe", "args": ["orderbook"]}))

    def set_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Set callback function for processing messages."""
        self.callback = callback

    async def start(self):
        """Start listening to the WebSocket feed."""
        if not await self.connect():
            return

        self.running = True
        try:
            while self.running:
                try:
                    message = await self.websocket.recv()
                    data = json.loads(message)
                    if self.callback:
                        await self.callback(data)
                except websockets.exceptions.ConnectionClosed:
                    self.logger.error("Connection closed unexpectedly")
                    if not await self.connect():
                        break
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}")
                    await asyncio.sleep(1)  # Prevent tight loop on errors
        finally:
            await self.close()

    async def close(self):
        """Close the WebSocket connection."""
        self.running = False
        if self.websocket:
            await self.websocket.close()
            self.logger.info("WebSocket connection closed") 