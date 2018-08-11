from GameHistory import GameHistory


def parse_point_score_text(point_score_text):
    point_score_text = point_score_text.replace('BP', '').replace('SP', '').replace('MP', '').replace('A', '50')
    point_score_text_parts = point_score_text.split(':')
    return [int(point_score_text_parts[0]), int(point_score_text_parts[1])]


def calculate_point_from_neighboring_scores(point_score1, point_score2):
    return point_score2[0] - point_score2[1] > point_score1[0] - point_score1[1]


def is_server_ahead(point_score):
    return point_score[0] > point_score[1]


def add_points_to_game_history(game_history, point_score_texts):
    current_point_score = [0, 0]
    for point_score_text in point_score_texts:
        new_point_score = parse_point_score_text(point_score_text)
        new_point = calculate_point_from_neighboring_scores(current_point_score, new_point_score)
        game_history.add_point(new_point)
        current_point_score = new_point_score
    final_point = is_server_ahead(current_point_score)
    game_history.add_point(final_point)


def get_game_history(game_text):
    point_score_texts = game_text.split(', ')
    game_history = GameHistory()
    add_points_to_game_history(game_history, point_score_texts)
    return game_history
