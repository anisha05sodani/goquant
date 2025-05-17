import pytest
import asyncio
from unittest.mock import Mock, patch
from src.core.websocket_client import WebSocketClient

@pytest.fixture
def mock_websocket():
    with patch('websockets.connect') as mock:
        yield mock

@pytest.fixture
def ws_client():
    return WebSocketClient("wss://test.url")

@pytest.mark.asyncio
async def test_websocket_connection(mock_websocket, ws_client):
    # Test successful connection
    mock_websocket.return_value = Mock()
    assert await ws_client.connect() is True
    
    # Test connection failure
    mock_websocket.side_effect = Exception("Connection failed")
    assert await ws_client.connect() is False

@pytest.mark.asyncio
async def test_message_processing(mock_websocket, ws_client):
    mock_callback = Mock()
    ws_client.set_callback(mock_callback)
    
    # Simulate receiving a message
    mock_ws = Mock()
    mock_ws.recv.return_value = '{"test": "data"}'
    mock_websocket.return_value = mock_ws
    
    # Start client and wait for one message
    task = asyncio.create_task(ws_client.start())
    await asyncio.sleep(0.1)
    ws_client.running = False
    await task
    
    # Verify callback was called
    mock_callback.assert_called_once_with({"test": "data"}) 