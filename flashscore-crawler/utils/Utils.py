domain = "https://www.flashscore.com/"


def get_source(browser, url):
    browser.get(url)
    return browser.page_source


def found_page(source):
    return 'The requested page can\'t be displayed' not in source


def get_edition_url(edition_string):
    return domain + "tennis/atp-singles/" + edition_string + "/"


def get_match_url(match_id):
    return domain + "match/" + match_id + "/"
