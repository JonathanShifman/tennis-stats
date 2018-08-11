from MatchHistory import MatchHistory
import SetParser
from selenium import webdriver
from bs4 import BeautifulSoup


def parse_match(match_hash):
    match_url = 'https://www.flashscore.com/match/' + match_hash + '/#point-by-point'
    browser = webdriver.Chrome()
    browser.get(match_url)
    match_source = BeautifulSoup(browser.page_source, 'html.parser')

    match_history = MatchHistory()
    for set_number in range(1, 6):
        set_div_element = match_source.find('div', attrs={'id': 'tab-mhistory-' + str(set_number) + '-history'})
        if set_div_element is not None:
            set_history = SetParser.get_set_history(set_div_element)
            match_history.add_set_history(set_history)
    return match_history
