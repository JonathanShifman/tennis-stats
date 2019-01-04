from utils import Utils
from bs4 import BeautifulSoup
import time


def get_edition_url(edition_string):
    return 'https://www.flashscore.com/tennis/atp-singles/' + edition_string + '/'


def get_source(browser, url):
    browser.get(url)
    return browser.page_source


def get_tab_source(browser, edition_string, tab_name):
    url = get_edition_url(edition_string) + tab_name + '/'
    return get_source(browser, url)


def get_show_more_matches_link(browser):
    try:
        link_element = browser.find_element_by_xpath("//table[contains(@id, 'tournament-page-results-more')]")\
            .find_element_by_tag_name("a")
        return link_element
    except:
        return None


def get_results_tab_source(browser, edition_string):
    url = get_edition_url(edition_string) + 'results/'
    browser.get(url)
    show_more_matches_link = get_show_more_matches_link(browser)
    if show_more_matches_link is not None:
        show_more_matches_link.click()
        time.sleep(5) # FIXME: Check that there are changes
    return browser.page_source


def determine_relevant_tab_source(draw_source, standings_source):
    found_draw_tab = Utils.found_page(draw_source)
    found_standings_tab = Utils.found_page(standings_source)
    if found_draw_tab and not found_standings_tab:
        return "draw", draw_source
    if found_standings_tab and not found_draw_tab:
        return "standings", standings_source
    raise Exception("Found either both 'draw' and 'standings' tabs, or neither of them")


def get_bubble_suffixes(soup):
    return [tag.find("a")["href"] for tag in soup.find_all("li", {"class": "bubble"})]


def get_bracket_sources_from_tab_source(browser, tab_source, tab_url):
    tab_soup = BeautifulSoup(tab_source, "html.parser")
    bubble_suffixes = get_bubble_suffixes(tab_soup)
    bracket_sources = [get_source(browser, tab_url + bubble_suffix) for bubble_suffix in bubble_suffixes]
    return bracket_sources


def get_bracket_sources(browser, edition_string):
    edition_url = get_edition_url(edition_string)
    draw_source = get_source(browser, edition_url + "draw")
    standings_source = get_source(browser, edition_url + "standings")
    relevant_tab_name, relevant_tab_source = determine_relevant_tab_source(draw_source, standings_source)
    relevant_tab_url = edition_url + relevant_tab_name + "/"
    return get_bracket_sources_from_tab_source(browser, relevant_tab_source, relevant_tab_url)
