class Edition:

    def __init__(self):
        self.brackets = []

    def get_match_ids(self):
        match_ids = []
        for bracket in self.brackets:
            for edition_round in bracket.rounds:
                match_ids.extend(edition_round.match_ids)
        return match_ids
