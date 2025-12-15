# game_state.py

class GameState:
    def __init__(self, player_ids):
        self.players = player_ids[:]     # All players initially alive
        self.alive_players = set(player_ids)
        self.turn_index = 0

    def next_player(self):
        player_list = list(self.alive_players)

        if not player_list:
            return None

        self.turn_index = (self.turn_index + 1) % len(player_list)
        return player_list[self.turn_index]

    def current_player(self):
        return list(self.alive_players)[self.turn_index]

    def update_alive_players(self, board):
        # If a player has no atoms → eliminated
        atom_count = {}

        for row in board:
            for cell in row:
                owner = cell["owner"]
                if owner:
                    atom_count[owner] = atom_count.get(owner, 0) + 1

        # Remove players with 0 atoms
        self.alive_players = {p for p in self.players if atom_count.get(p, 0) > 0}

        # Reset turn index if needed
        if self.turn_index >= len(self.alive_players):
            self.turn_index = 0

    def check_winner(self):
        if len(self.alive_players) == 1:
            return list(self.alive_players)[0]
        return None
