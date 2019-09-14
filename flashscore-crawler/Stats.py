import pickle
import os
import PeriodFilter


tournaments = pickle.load(open('resources/periods.pkl', 'rb'))

# years = [2017, 2018, 2019]
years = [2017, 2018]

# player_id = 'GrsQDFC0' # Federer
# player_id = 'xUwlUnRK' # Nadal
# player_id = 'AZg49Et9' # Djokovic
player_id = 'GrsQDFC0'
on_serve = True

keys = ['0:0', '15:0', '0:15', '30:0', '15:15', '0:30', '40:0', '30:15',
        '15:30', '0:40', '40:15', '30:30', '15:40', '40:30', '30:40', '40:40', '50:40', '40:50', 'deuce', 'ad']
deuce_side_keys = ['0:0', '30:0', '15:15', '0:30', '40:15', '30:30', '15:40', '40:40']

won = dict()
lost = dict()
for key in keys:
    won[key] = 0
    lost[key] = 0


def update_stats(score, won_point):
    if won_point:
        relevant_dict = won
    else:
        relevant_dict = lost

    relevant_dict[score] += 1
    if score in deuce_side_keys:
        relevant_dict['deuce'] += 1
    else:
        relevant_dict['ad'] += 1


def process_match(match_id):
    # if match_id != 'WzVaC4Ka':
    #     return False
    match_pkl_path = 'output/matches/' + match_id + '/match.pkl'
    if not os.path.exists(match_pkl_path):
        return False
    match = pickle.load(open(match_pkl_path, 'rb'))
    if match.player1_id == player_id or match.player2_id == player_id:
        if match.player1_id == player_id:
            player_side = 1
        else:
            player_side = 2
        current_game_id = 1
        for i in range(len(match.game_scores)):
            game = match.game_scores[i]
            server_side = match.servers[i]
            if (on_serve and server_side == player_side) or ((not on_serve) and server_side != player_side):
                if server_side == 2:
                    for i in range(len(game)):
                        score = game[i]
                        split_score = score.split(':')
                        reversed_score = split_score[1] + ':' + split_score[0]
                        game[i] = reversed_score

                current_score = '0:0'
                for new_score in game:
                    current1 = int(current_score.split(':')[0])
                    current2 = int(current_score.split(':')[1])
                    new1 = int(new_score.split(':')[0])
                    new2 = int(new_score.split(':')[1])
                    if new1 > current1 or new2 < current2:
                        # server won
                        update_stats(score=current_score, won_point=(player_side == server_side))
                    else:
                        update_stats(score=current_score, won_point=(player_side != server_side))
                    current_score = new_score
                current1 = int(current_score.split(':')[0])
                current2 = int(current_score.split(':')[1])
                if current1 > current2:
                    update_stats(score=current_score, won_point=(player_side == server_side))
                else:
                    update_stats(score=current_score, won_point=(player_side != server_side))
            current_game_id += 1
        return True
    return False


def process_tournament(year, tournament):
    edition_pkl_path = 'output/editions/' + str(year) + ',' + tournament.name + '/edition.pkl'
    if not os.path.exists(edition_pkl_path):
        # print(str(year) + ' ' + tournament.name + ': No pkl')
        return
    edition = pickle.load(open(edition_pkl_path, 'rb'))
    match_ids = edition.get_match_ids()
    tournament_relevant_matches = 0
    for match_id in match_ids:
        is_relevant = process_match(match_id)
        if is_relevant:
            tournament_relevant_matches += 1
    if tournament_relevant_matches > 0:
        print(str(year) + ' ' + tournament.name + ' - ' + str(tournament_relevant_matches))


for year in years:
    tournaments_in_year = PeriodFilter.filter_tournaments_by_year(tournaments, year)
    for tournament in tournaments_in_year:
        process_tournament(year, tournament)

for key in keys:
    percentage = "{0:.2f}".format(100 * float(won[key]) / float(won[key] + lost[key]))
    print(key + ' - ' + str(won[key]) + '/' + str(won[key] + lost[key]) + ' [' + percentage + ']')
