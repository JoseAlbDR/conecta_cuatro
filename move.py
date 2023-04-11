class Move:
    def __init__(self, position, board_code, recommendations, player) -> None:
        self.position = position
        self.board_code = board_code
        self.recommendations = recommendations
        self.player = player