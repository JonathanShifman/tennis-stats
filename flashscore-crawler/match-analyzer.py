from selenium import webdriver
from BeautifulSoup import BeautifulSoup
from MatchHistory import MatchHistory
from SetHistory import SetHistory
from GameHistory import GameHistory


def get_set_source(browser, set_number):
    set_button = browser.find_element_by_id('mhistory-' + str(set_number) + '-history')
    set_button.click()
    return browser.page_source


def cross_merge_lists(list1, list2):
    merged_list = []
    for i in range(len(list1)):
        merged_list.append(list1[i])
        if i < len(list2):
            merged_list.append(list2[i])
    return merged_list


def get_game_tr_elements(set_div_element):
    game_tr_elements_odd = set_div_element.findAll('tr', attrs={'class': 'odd fifteen'})
    game_tr_elements_even = set_div_element.findAll('tr', attrs={'class': 'even fifteen'})
    return cross_merge_lists(game_tr_elements_odd, game_tr_elements_even)


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


def get_set_history(set_div_element):
    set_history = SetHistory()
    game_tr_elements = get_game_tr_elements(set_div_element)
    for game_tr_element in game_tr_elements:
        game_text = game_tr_element.findChildren('td')[0].text
        game_history = get_game_history(game_text)
        set_history.add_game_history(game_history)
    return set_history


def get_match_history(match_url):
    browser = webdriver.Chrome()
    browser.get(match_url)
    parsed_match_source = BeautifulSoup(browser.page_source)

    match_history = MatchHistory()
    for set_number in range(1, 6):
        set_div_element = parsed_match_source.find('div', attrs={'id': 'tab-mhistory-' + str(set_number) + '-history'})
        if set_div_element is not None:
            set_history = get_set_history(set_div_element)
            match_history.add_set_history(set_history)
    return match_history


url = 'https://www.flashscore.com/match/bBzDCf9a/#point-by-point'
match_history = get_match_history(url)
print match_history

