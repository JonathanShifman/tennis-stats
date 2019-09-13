import pickle
import os
import sys


def year_in_period(year, period):
    if len(period) == 1:
        return year == period[0]
    # len(period) == 2
    return period[0] <= year <= period[1]


tournaments = pickle.load(open('resources/periods.pkl', 'rb'))
# years = [2017, 2018, 2019]
years = [2018]
player_id = 'Gz6r1gS0'

keys = ['0:0', '15:0', '0:15', '30:0', '15:15', '0:30', '40:0', '30:15',
        '15:30', '0:40', '40:15', '30:30', '15:40', '40:30', '30:40', '40:40', '50:40', '40:50']

won = dict()
lost = dict()
for key in keys:
    won[key] = 0
    lost[key] = 0

total_matches = 0

for year in years:
    for tournament in tournaments:
        if year_in_period(year, tournament.periods[0]):
            edition_pkl_path = 'output/editions/' + str(year) + ',' + tournament.name + '/edition.pkl'
            if not os.path.exists(edition_pkl_path):
                print(str(year) + ' ' + tournament.name + ': No pkl')
                continue
            edition = pickle.load(open(edition_pkl_path, 'rb'))
            match_ids = edition.get_match_ids()
            total_matches += len(match_ids)
            relevant_matches = 0
            matches_with_pkl = 0
            for match_id in match_ids:
                match_pkl_path = 'output/matches/' + match_id + '/match.pkl'
                if not os.path.exists(match_pkl_path):
                    continue
                else:
                    matches_with_pkl += 1
                    match = pickle.load(open(match_pkl_path, 'rb'))
                    if match.player1_id == player_id or match.player2_id == player_id:
                        relevant_matches += 1
                        for game in match.game_scores:
                            current_score = '0:0'
                            for new_score in game:
                                current1 = int(current_score.split(':')[0])
                                current2 = int(current_score.split(':')[1])
                                new1 = int(new_score.split(':')[0])
                                new2 = int(new_score.split(':')[1])
                                if new1 > current1 or new2 < current2:
                                    # player 1 won
                                    if match.player1_id == player_id:
                                        won[current_score] += 1
                                    else:
                                        lost[current_score] += 1
                                else:
                                    # player 2 won
                                    if match.player1_id == player_id:
                                        lost[current_score] += 1
                                    else:
                                        won[current_score] += 1
                                current_score = new_score
                            current1 = int(current_score.split(':')[0])
                            current2 = int(current_score.split(':')[1])
                            if current1 > current2:
                                # player 1 won
                                if match.player1_id == player_id:
                                    won[current_score] += 1
                                else:
                                    lost[current_score] += 1
                            else:
                                # player 2 won
                                if match.player1_id == player_id:
                                    lost[current_score] += 1
                                else:
                                    won[current_score] += 1
            print(str(year) + ' ' + tournament.name + ': ' + str(relevant_matches) + ' ' + str(matches_with_pkl))

print(total_matches)

for key in keys:
    print(key + ' - ' + str(won[key]) + '/' + str(won[key] + lost[key]))
