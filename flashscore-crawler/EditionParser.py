from selenium import webdriver
from bs4 import BeautifulSoup


class UnexpectedStartOfBracket(Exception):
    pass


class UnexpectedStartOfRound(Exception):
    pass


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

    def can_open_new_bracket(self, bracket_name):
        if self.current_bracket is None:
            return True
        if bracket_name in self.edition_dict['brackets'] or self.expecting_another_match_row():
            return False
        return True

    def can_open_new_round(self, round_name):
        if self.current_bracket is None:
            return False
        if self.current_round is None:
            return True
        if round_name in self.current_bracket or self.expecting_another_match_row():
            return False
        return True

    def expecting_another_match_row(self):
        if self.current_round is None:
            return False
        return True

    def generate_edition_json(self, edition_string):
        edition_source = get_edition_source(edition_string)
        tr_classes = {'league', 'event_round', 'odd', 'even'}
        relevant_elements = edition_source.find_all(lambda element:
                                                    (element.name == 'tr' and 'class' in element.attrs and len(
                                                        set(element['class']) & tr_classes) > 0))

        self.edition_dict = dict()
        self.edition_dict['brackets'] = dict()
        for element in relevant_elements:
            if 'league' in element['class']:
                bracket_name = get_bracket_name(element)
                if self.can_open_new_bracket(bracket_name):
                    self.current_bracket = dict()
                    self.edition_dict['brackets'][bracket_name] = self.current_bracket
                else:
                    raise UnexpectedStartOfBracket
            elif 'event_round' in element['class']:
                round_name = get_round_name(element)
                if self.can_open_new_round(round_name):
                    self.current_round = []
                    self.current_bracket[round_name] = self.current_round
                else:
                    raise UnexpectedStartOfRound
            else:  # 'odd' or 'even' in element['class']
                if self.expecting_another_match_row():
                    match_dict = parse_match_row(element)
                    self.current_round.append(match_dict)


