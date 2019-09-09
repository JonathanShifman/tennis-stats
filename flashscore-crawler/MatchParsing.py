import os
from bs4 import BeautifulSoup
import pickle
from classes.MatchHistory import MatchHistory


def parse_match(match_id):
    print("Parsing match " + match_id)
    history_file_path = 'output/matches/' + match_id + '/history.txt'
    if not os.path.exists(history_file_path):
        raise Exception("Couldn't find history file")

    with open(history_file_path, 'r') as history_file:
        soup = BeautifulSoup(history_file.read().decode("utf-8"), "html.parser")

    history = MatchHistory()
    pickle.dump(history, open('output/matches/' + match_id + '/match.pkl', "wb"))



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