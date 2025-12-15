# game_state.py

class GameState:
    def __init__(self, player_ids):
        # KEEP ORDER — this is very important
        self.players = list(player_ids)

        # Alive players must also be a LIST (not a set!)
        self.alive_players = list(player_ids)

        self.turn_index = 0  # always start with first player

    def current_player(self):
        return self.alive_players[self.turn_index]

    def next_player(self):
        if not self.alive_players:
            return None

        self.turn_index = (self.turn_index + 1) % len(self.alive_players)
        return self.alive_players[self.turn_index]

    def update_alive_players(self, board):
        """Collect which players have at least 1 atom"""

        atom_count = {}

        for row in board:
            for cell in row:
                owner = cell["owner"]
                if owner:
                    atom_count.setdefault(owner, 0)
                    atom_count[owner] += cell["count"]

        # Keep original ordering: only filter players that still have atoms
        new_alive = [p for p in self.players if atom_count.get(p, 0) > 0]

        # If no one placed atoms yet, do NOT eliminate anyone
        if len(atom_count) == 0:
            return

        self.alive_players = new_alive

        # Fix turn index if it goes out of range
        if self.turn_index >= len(self.alive_players):
            self.turn_index = 0

    def check_winner(self):
        """Winner = only 1 alive player left AND they have atoms"""
        if len(self.alive_players) == 1:
            return self.alive_players[0]
        return None
