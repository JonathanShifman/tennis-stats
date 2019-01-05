from utils import MatchSourceReader
from selenium import webdriver
import os
import pickle
import time


def scrape_match(browser, match_id):
    summary_source, history_source = MatchSourceReader.get_match_sources(browser, match_id)
    dir_path = 'output/matches/' + match_id + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(dir_path + 'summary.txt', 'wb') as output_file:
        output_file.write(summary_source.encode('utf8'))

    with open(dir_path + 'history.txt', 'wb') as output_file:
        output_file.write(history_source.encode('utf8'))


def scrape_matches_from_edition(browser, year, tournament_name):
    edition_dir_name = str(year) + "," + tournament_name
    edition = pickle.load(open("output/editions/" + edition_dir_name + "/edition.pkl", "rb"))
    for bracket in edition.brackets:
        for edition_round in bracket.rounds:
            for match_id in edition_round.match_ids:
                scrape_match(browser, match_id)
                time.sleep(3)


browser = webdriver.Chrome()
scrape_matches_from_edition(browser, 2018, "australian-open")
browser.quit()
