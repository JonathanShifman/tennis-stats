from utils import MatchSourceReader, Utils
import os
import pickle
import time


def scrape_match(browser, match_id):
    dir_path = 'output/matches/' + match_id + '/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        if os.path.exists(dir_path + 'summary.txt') and os.path.exists(dir_path + 'history.txt'):
            print("Match has already been scraped")
            return False
    summary_source, history_source = MatchSourceReader.get_match_sources(browser, match_id)

    with open(dir_path + 'summary.txt', 'wb') as output_file:
        output_file.write(summary_source.encode('utf8'))

    with open(dir_path + 'history.txt', 'wb') as output_file:
        output_file.write(history_source.encode('utf8'))

    return True


def scrape_matches_from_edition(browser, year, tournament_name):
    print("Scraping " + tournament_name + " " + str(year))
    edition_dir_name = str(year) + "," + tournament_name
    edition = pickle.load(open("output/editions/" + edition_dir_name + "/edition.pkl", "rb"))

    match_ids = []
    for bracket in edition.brackets:
        for edition_round in bracket.rounds:
            for match_id in edition_round.match_ids:
                match_ids.append(match_id)

    total = len(match_ids)
    current = 1
    print('Total matches to scrape: ' + str(total))
    for match_id in match_ids:
        print(Utils.get_time_prefix() + "Scraping match " + match_id + " [" + str(current) + "/" + str(total) + "]")
        should_wait = True
        try:
            should_wait = scrape_match(browser, match_id)
        except:
            print("Failed to scrape match")
        if should_wait:
            time.sleep(5)
        current += 1
