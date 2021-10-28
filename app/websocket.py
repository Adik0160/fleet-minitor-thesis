from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket, deviceNr: int):
        await websocket.accept()
        self.active_connections.append({'wsHandler': websocket, 'deviceNr': deviceNr})

    def disconnect(self, websocket: WebSocket):
        for i in range(len(self.active_connections)):
            if self.active_connections[i]['wsHandler'] == websocket:
                del self.active_connections[i]
                break

    async def broadcastDataToDeviceId(self, message: str, deviceNr: int):
        for connection in self.active_connections:
            if connection['deviceNr'] == deviceNr:
                await connection['wsHandler'].send_text(message)

wsManager = ConnectionManager()