from bs4 import BeautifulSoup
from enum import Enum
import SourceReader


class UnexpectedStartOfBracket(Exception):
    pass


class UnexpectedStartOfRound(Exception):
    pass


class UnexpectedMatch(Exception):
    pass


class Row(Enum):
    Bracket = 1
    Round = 2
    Match = 3


def get_edition_source(browser, edition_string):
    return BeautifulSoup(SourceReader.get_edition_raw_sources_dict(browser, edition_string)['results'], 'html.parser')


def get_bracket_name(tr_element):
    if 'Qualification' in tr_element.find('span', {'class': 'tournament_part'}).text:
        return 'Qual'
    return 'Main'


def get_round_name(tr_element):
    return tr_element.td.text


def extract_match_hash(match_tr_element):
    return match_tr_element['id'].replace('g_2_', '')


def parse_match_row(match_tr_element):
    match_dict = dict()
    match_dict['hash'] = extract_match_hash(match_tr_element)
    return match_dict


def generate_edition_json(edition_source_file_path):
    with open(edition_source_file_path, 'rb') as f:
        edition_source = BeautifulSoup(f.read(), 'html.parser')
    tr_classes = {'league', 'event_round', 'odd', 'even'}
    relevant_elements = edition_source.find_all(lambda element:
                                                (element.name == 'tr' and 'class' in element.attrs and len(
                                                    set(element['class']) & tr_classes) > 0))

    edition_dict = dict()
    edition_dict['brackets'] = []
    for element in relevant_elements:
        if 'league' in element['class']:
            print 'Parsing bracket row'
            print 'Opening new bracket'
            bracket_name = get_bracket_name(element)
            current_bracket = dict()
            current_bracket['name'] = bracket_name
            current_bracket['rounds'] = []
            edition_dict['brackets'].append(current_bracket)
            round_name_to_index = dict()
            current_round = None
        elif 'event_round' in element['class']:
            print 'Parsing round row'
            round_name = get_round_name(element)
            if round_name not in round_name_to_index:
                print 'Opening new round'
                new_round = dict()
                new_round['name'] = round_name
                new_round['matches'] = []
                current_bracket['rounds'].append(new_round)
                round_name_to_index[round_name] = len(current_bracket['rounds']) - 1
            current_round = current_bracket['rounds'][round_name_to_index[round_name]]
        else:  # 'odd' or 'even' in element['class']
            print 'Parsing match row'
            match_dict = parse_match_row(element)
            current_round['matches'].append(match_dict)
    return edition_dict
