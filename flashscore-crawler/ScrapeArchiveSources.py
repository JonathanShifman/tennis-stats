from utils import Utils
import traceback
import time


def scrape_tournament_archive(browser, tournament_name):
    browser.get(Utils.get_archive_url(tournament_name))
    return browser.page_source


with open('resources/tournament-names.txt', 'r') as f:
    tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]

browser = Utils.get_browser()
for tournament_name in tournament_names:
    try:
        print("Scraping archive source for: " + tournament_name)
        source = scrape_tournament_archive(browser, tournament_name)
        with open('output/archives/' + tournament_name + '-archive.txt', 'w') as output_file:
            output_file.write(source.encode('utf8'))
    except Exception as e:
        print("Failed to scrape tournament archive for " + tournament_name + ": " + e.message)
        traceback.print_exc()
    time.sleep(5)
browser.quit()
