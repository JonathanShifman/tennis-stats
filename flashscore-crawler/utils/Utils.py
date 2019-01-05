import time
from utils import PageEnforcer


domain = "https://www.flashscore.com/"


def get_source(browser, url, condition_to_enforce=None, condition_meaning=None):
    browser.get(url)
    if condition_to_enforce is not None:
        PageEnforcer.enforce(browser, condition_to_enforce, condition_meaning)
    return browser.page_source


def found_page(source):
    return 'The requested page can\'t be displayed' not in source


def get_edition_url(edition_string):
    return domain + "tennis/atp-singles/" + edition_string + "/"


def get_match_url(match_id):
    return domain + "match/" + match_id + "/"


def get_archive_url(tournament_name):
    return domain + "tennis/atp-singles/" + tournament_name + "/archive/"


def print_divider():
    print("---------------------------------")