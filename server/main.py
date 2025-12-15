# main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from rooms import RoomManager

app = FastAPI()
rooms = RoomManager()

@app.websocket("/ws/{room_id}/{player_id}")
async def ws_endpoint(websocket: WebSocket, room_id: str, player_id: str):
    await rooms.connect(room_id, player_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            t = data.get("type")

            if t == "select_grid":
                rooms.set_grid(room_id, data["grid"])

            elif t == "start_game":
                await rooms.start_game(room_id)

            elif t == "move":
                await rooms.handle_move(room_id, player_id, data["r"], data["c"])

    except WebSocketDisconnect:
        pass
