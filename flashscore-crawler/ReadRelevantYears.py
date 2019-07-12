from selenium import webdriver
from utils import Utils
from bs4 import BeautifulSoup
from Tournament import Tournament
import traceback
import time
import pickle


def get_period(start, end):
    if start == end:
        return [start]
    return [start, end]


def get_periods(browser, tournament_name):
    browser.get(Utils.get_archive_url(tournament_name))
    if not Utils.found_page(browser.page_source):
        raise Exception("Archive page not found")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    archive_div_elements = soup.find_all("div", {"id": "tournament-page-archiv"})
    if len(archive_div_elements) != 1:
        raise Exception("Unexpected page structure")

    edition_div_elements = archive_div_elements[0].find_all("div", {"class": "leagueTable__season"})[1:]
    if len(edition_div_elements) == 0:
        raise Exception("No editions found")

    current_period_end = None
    last_encountered_year = None
    periods = []
    for edition_div_element in edition_div_elements:
        year = int(edition_div_element.find("a").text.split(" ")[-1])

        if current_period_end is None:
            current_period_end = year
            last_encountered_year = year
        else:
            if last_encountered_year <= year:
                raise Exception("Unexpected years order")
            elif last_encountered_year - year == 1:
                last_encountered_year = year
            else:
                periods.append(get_period(last_encountered_year, current_period_end))
                current_period_end = year
                last_encountered_year = year
    periods.append(get_period(last_encountered_year, current_period_end))

    return periods


with open('resources/tournament-names.txt', 'r') as f:
    tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]

browser = webdriver.Chrome()
tournaments = []
for tournament_name in tournament_names:
    try:
        periods = get_periods(browser, tournament_name)
        tournaments.append(Tournament(tournament_name, periods))
    except Exception as e:
        print("Failed to read relevant years for " + tournament_name + ": " + e.message)
        traceback.print_exc()
    time.sleep(5)
browser.quit()
pickle.dump(tournaments, open('output/periods.pkl', 'wb'))

