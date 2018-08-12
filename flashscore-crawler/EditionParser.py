from selenium import webdriver
from bs4 import BeautifulSoup
from enum import Enum
import RoundMappings


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


def get_edition_source(edition_string):
        edition_results_url = 'https://www.flashscore.com/tennis/atp-singles/' + edition_string + '/results/'
        browser = webdriver.Chrome()
        browser.get(edition_results_url)
        return BeautifulSoup(browser.page_source, 'html.parser')


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
    match_dict["hash"] = extract_match_hash(match_tr_element)
    return match_dict


class EditionParser:

    def __init__(self):
        self.current_bracket = None
        self.current_round = None
        self.edition_dict = dict()

    def get_possible_next_rows(self):
        if self.current_bracket is None:
            return {Row.Bracket}
        if self.current_round is None:
            return {Row.Round}
        if self.current_bracket['name'] == 'Main':
            expected_num_of_matches_in_round = pow(2, RoundMappings.round_name_to_id[self.current_round['name']] - 1)
            if len(self.current_round['matches']) == expected_num_of_matches_in_round:
                return {Row.Bracket, Row.Round}
            return {Row.Match}
        return {Row.Bracket, Row.Round, Row.Match}

    def generate_edition_json(self, edition_string):
        edition_source = get_edition_source(edition_string)
        tr_classes = {'league', 'event_round', 'odd', 'even'}
        relevant_elements = edition_source.find_all(lambda element:
                                                    (element.name == 'tr' and 'class' in element.attrs and len(
                                                        set(element['class']) & tr_classes) > 0))

        self.edition_dict = dict()
        self.edition_dict['brackets'] = dict()
        for element in relevant_elements:
            possible_next_rows = self.get_possible_next_rows()
            if 'league' in element['class']:
                print 'Attempting to open bracket'
                if Row.Bracket in possible_next_rows:
                    bracket_name = get_bracket_name(element)
                    self.current_bracket = dict()
                    self.current_bracket['name'] = bracket_name
                    self.current_bracket['rounds'] = dict()
                    self.edition_dict['brackets'][bracket_name] = self.current_bracket
                    self.current_round = None
                else:
                    raise UnexpectedStartOfBracket
            elif 'event_round' in element['class']:
                print 'Attempting to open round'
                if Row.Round in possible_next_rows:
                    round_name = get_round_name(element)
                    self.current_round = dict()
                    self.current_round['name'] = round_name
                    self.current_round['matches'] = []
                    self.current_bracket['rounds'][round_name] = self.current_round
                else:
                    raise UnexpectedStartOfRound
            else:  # 'odd' or 'even' in element['class']
                print 'Attempting to parse match'
                if Row.Match in possible_next_rows:
                    match_dict = parse_match_row(element)
                    self.current_round['matches'].append(match_dict)
                else:
                    raise UnexpectedMatch


