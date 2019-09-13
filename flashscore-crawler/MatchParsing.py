import os
from bs4 import BeautifulSoup
import pickle
from classes.Match import Match


def parse_match(match_id):
    print("Parsing match " + match_id)
    history_file_path = 'output/matches/' + match_id + '/history.txt'
    if not os.path.exists(history_file_path):
        raise Exception("Couldn't find history file")

    with open(history_file_path, 'r') as history_file:
        soup = BeautifulSoup(history_file.read().decode("utf-8"), "html.parser")

    player1_element = soup.find("div", {"class": "home-box"}).find_all("a", {"class": "participant-imglink"})[0]
    player2_element = soup.find("div", {"class": "away-box"}).find_all("a", {"class": "participant-imglink"})[0]
    player1_id = str(player1_element["onclick"].split('/')[-1].split('\'')[0])
    player2_id = str(player2_element["onclick"].split('/')[-1].split('\'')[0])

    server_elements = soup.find_all("tr", {"class": "fifteens_available"})
    servers = []
    for server_element in server_elements:
        serve_elements = server_element.find_all("td", {"class": "server"})
        if len(serve_elements[0].find_all("div", {"class": "icon-box"})) > 0:
            servers.append(1)
        else:
            servers.append(2)

    score_row_elements = soup.find_all("tr", {"class": "fifteen"})
    game_scores = [str(element.find('td').text)
                       .replace('BP', '')
                       .replace('SP', '')
                       .replace('MP', '')
                       .replace('A', '50')
                       .split(', ')
                   for element in score_row_elements]

    match = Match(player1_id, player2_id, servers)
    match.game_scores = game_scores

    pickle.dump(match, open('output/matches/' + match_id + '/match.pkl', "wb"))


def parse_edition_matches(year, tournament_name):
    print('Parsing edition: ' + tournament_name + ' ' + str(year))
    edition_dir_name = str(year) + "," + tournament_name
    pickle_path = "output/editions/" + edition_dir_name + "/edition.pkl"
    if not os.path.exists(pickle_path):
        raise Exception("Pickle not found: " + pickle_path)

    edition = pickle.load(open(pickle_path, "rb"))
    for bracket in edition.brackets:
        for edition_round in bracket.rounds:
            for match_id in edition_round.match_ids:
                try:
                    parse_match(match_id)
                except Exception as e:
                    print("Failed to parse match " + match_id + ": " + e.message)
