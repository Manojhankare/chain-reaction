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
        # Corner
        if (r in [0, self.rows-1]) and (c in [0, self.cols-1]):
            return 1

        # Edge
        if r in [0, self.rows-1] or c in [0, self.cols-1]:
            return 2

        # Center
        return 3

    def apply_move(self, r, c, player_id):
        queue = [(r, c, player_id)]

        while queue:
            r, c, pid = queue.pop(0)
            cell = self.board[r][c]

            cell["owner"] = pid
            cell["count"] += 1

            if cell["count"] > self.capacity(r, c):
                cell["count"] = 0
                cell["owner"] = None

                for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        queue.append((nr, nc, pid))
