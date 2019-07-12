import os
import pickle
from bs4 import BeautifulSoup


def parse_match(match_id):
    history_file_path = 'output/matches/' + match_id + '/history.txt'
    if not os.path.exists(history_file_path):
        raise Exception("Couldn't find history file")

    with open(history_file_path, 'r') as history_file:
        soup = BeautifulSoup(history_file.read().decode("utf-8"), "html.parser")
        a = 1


def parse_matches_from_edition(year, tournament_name):
    edition_dir_name = str(year) + "," + tournament_name
    edition = pickle.load(open("output/editions/" + edition_dir_name + "/edition.pkl", "rb"))
    for bracket in edition.brackets:
        for edition_round in bracket.rounds:
            for match_id in edition_round.match_ids:
                print("Parsing match " + match_id)
                try:
                    parse_match(match_id)
                except:
                    print("Failed to parse match")


parse_matches_from_edition(2019, "brisbane")
