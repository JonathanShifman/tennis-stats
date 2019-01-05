from selenium import webdriver
from utils import Utils
from bs4 import BeautifulSoup
import traceback
import time


def get_period_str(start, end):
    if start == end:
        return str(start)
    return str(start) + "-" + str(end)


def get_periods(browser, tournament_name):
    browser.get(Utils.get_archive_url(tournament_name))
    if not Utils.found_page(browser.page_source):
        raise Exception("Archive page not found")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    archive_div_elements = soup.find_all("div", {"id": "tournament-page-archiv"})
    if len(archive_div_elements) != 1:
        raise Exception("Unexpected page structure")

    edition_row_elements = archive_div_elements[0].find("tbody").find_all("tr")
    if len(edition_row_elements) == 0:
        raise Exception("No editions found")

    current_period_end = None
    last_encountered_year = None
    periods = []
    for edition_row_element in edition_row_elements:
        td_elements = edition_row_element.find_all("td")
        if len(td_elements) > 2:
            raise Exception("Unexpected page structure")
        year = int(td_elements[0].find("a").text.split(" ")[-1])

        if current_period_end is None:
            current_period_end = year
            last_encountered_year = year
        else:
            if last_encountered_year <= year:
                raise Exception("Unexpected years order")
            elif last_encountered_year - year == 1:
                last_encountered_year = year
            else:
                periods.append(get_period_str(last_encountered_year, current_period_end))
                current_period_end = year
                last_encountered_year = year
    periods.append(get_period_str(last_encountered_year, current_period_end))

    return periods


with open('resources/tournament-names.txt', 'r') as f:
    tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]

browser = webdriver.Chrome()
output_lines = []
for tournament_name in tournament_names:
    try:
        periods = get_periods(browser, tournament_name)
        output_line = tournament_name + "," + ",".join(periods)
        output_lines.append(output_line)
        print(output_line)
    except Exception as e:
        print("Failed to read relevant years for " + tournament_name + ": " + e.message)
        traceback.print_exc()
    time.sleep(5)
browser.quit()

with open("resources/periods_output.txt", "w") as output_file:
    for line in output_lines:
        output_file.write(line + "\n")

