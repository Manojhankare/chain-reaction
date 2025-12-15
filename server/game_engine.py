# game_engine.py

class ChainReaction:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.board = [
            [{"count": 0, "owner": None} for _ in range(cols)]
            for _ in range(rows)
        ]

    def capacity(self, r, c):
        if (r in [0, self.rows-1]) and (c in [0, self.cols-1]):
            return 1  # corner
        if r in [0, self.rows-1] or c in [0, self.cols-1]:
            return 2  # edge
        return 3      # center

    def apply_move(self, r, c, player_id):
        cell = self.board[r][c]

        # Rule: can place if empty or owned by player
        if cell["owner"] not in [None, player_id]:
            return  # illegal move (should never happen)

        queue = [(r, c)]

        while queue:
            r, c = queue.pop(0)
            cell = self.board[r][c]

            # Claim
            cell["owner"] = player_id
            cell["count"] += 1

            # Explosion condition
            if cell["count"] > self.capacity(r, c):
                # Reset current cell after explosion
                cell["count"] = 0
                cell["owner"] = None

                # Spread to neighbors
                for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        queue.append((nr, nc))
