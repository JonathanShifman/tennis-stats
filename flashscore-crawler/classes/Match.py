from MatchHistory import MatchHistory


class Match:

    def __init__(self, player1_id, player2_id):
        self.match_history = MatchHistory()
        self.player1_id = player1_id
        self.player2_id = player2_id
