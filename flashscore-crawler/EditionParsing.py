import os
from bs4 import BeautifulSoup
from classes.Edition import Edition
from classes.Bracket import Bracket
from classes.Round import Round
import pickle


def get_match_id(match_element):
    link_elements = match_element.find_all("a", {"title": "Click for match detail!"})
    if len(link_elements) > 1:
        raise Exception("Unexpected number of match detail links: " + str(len(link_elements)))
    if len(link_elements) == 0:
        return None

    link_element = link_elements[0]
    id_attr = link_element.attrs["id"]
    if id_attr is None:
        raise Exception("Match details link didn't have an id element")
    id_split = id_attr.split("_")
    if len(id_split) != 3:
        raise Exception("Unexpected structure of match details link id attribute")
    match_id = str(id_split[-1])
    if len(match_id) != 8:
        print("Warning: Unexpected length of match id: " + match_id)
    return match_id


def parse_round_element(round_element):
    edition_round = Round()
    match_elements = round_element.find_all("div", {"class": "match"})
    if len(match_elements) == 0:
        raise Exception("No matches found in round")

    for match_element in match_elements:
        match_id = get_match_id(match_element)
        if match_id is not None:
            edition_round.match_ids.append(match_id)
    return edition_round


def parse_bracket(bracket_soup):
    bracket = Bracket()
    round_elements = bracket_soup.find_all("div", {"class": "round"})
    if len(round_elements) == 0:
        raise Exception("No rounds found")

    for round_element in round_elements:
        edition_round = parse_round_element(round_element)
        bracket.rounds.append(edition_round)
    return bracket


def parse_edition(year, tournament_name):
    print("Parsing " + str(year) + " " + tournament_name)
    edition = Edition()
    dir_name = "output/editions/" + str(year) + "," + tournament_name + "/"
    if not os.path.exists(dir_name):
        raise Exception("Sources dir not found")
    if os.path.exists(dir_name + "edition.pkl"):
        return
    bracket_file_names = [file_name for file_name in os.listdir(dir_name) if "bracket" in file_name]
    for bracket_file_name in bracket_file_names:
        bracket_file_path = dir_name + bracket_file_name
        with open(bracket_file_path, "r") as f:
            soup = BeautifulSoup(f.read().decode("utf-8"), "html.parser")
            bracket = parse_bracket(soup)
            edition.brackets.append(bracket)
    pickle.dump(edition, open(dir_name + "edition.pkl", "wb"))