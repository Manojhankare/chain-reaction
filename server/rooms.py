# rooms.py

from game_engine import ChainReaction
from game_state import GameState
from config import GRID_OPTIONS, MAX_PLAYERS

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, room_id):
        self.rooms[room_id] = {
            "players": {},
            "status": "waiting",
            "grid": GRID_OPTIONS["medium"],
            "game": None,
            "state": None,
        }

    async def connect(self, room_id, player_id, websocket):
        if room_id not in self.rooms:
            self.create_room(room_id)

        room = self.rooms[room_id]

        if len(room["players"]) >= MAX_PLAYERS:
            await websocket.close()
            return

        room["players"][player_id] = websocket
        await websocket.accept()

        # Broadcast lobby update
        await self.broadcast(room_id, {
            "type": "lobby_update",
            "players": list(room["players"].keys())
        })

    async def broadcast(self, room_id, message):
        room = self.rooms[room_id]

        for ws in room["players"].values():
            await ws.send_json(message)

    def set_grid(self, room_id, grid_key):
        room = self.rooms[room_id]
        room["grid"] = GRID_OPTIONS[grid_key]

    async def start_game(self, room_id):
        room = self.rooms[room_id]

        players = list(room["players"].keys())
        rows, cols = room["grid"]
        
        print("INITIALIZING GAME WITH GRID:", rows, cols)

        room["game"] = ChainReaction(rows, cols)
        print("BOARD SIZE:", len(room["game"].board), len(room["game"].board[0]))

        room["state"] = GameState(players)
        room["status"] = "running"

        await self.broadcast(room_id, {
            "type": "game_started",
            "grid": room["grid"],
            "turn": room["state"].current_player(),
            "board": room["game"].board   # FIXED
        })

    async def handle_move(self, room_id, player_id, r, c):
        room = self.rooms[room_id]
        game = room["game"]
        state = room["state"]

        if player_id != state.current_player():
            return

        # Apply move
        game.apply_move(r, c, player_id)

        # Update eliminated players
        state.update_alive_players(game.board)

        winner = state.check_winner()

        if winner:
            await self.broadcast(room_id, {
                "type": "game_over",
                "winner": winner
            })
            room["status"] = "finished"
            return

        # Rotate turn
        state.next_player()

        await self.broadcast(room_id, {
            "type": "board_update",
            "board": game.board,
            "turn": state.current_player()
        })
