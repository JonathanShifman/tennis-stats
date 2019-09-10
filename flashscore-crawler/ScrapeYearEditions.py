import pickle

from utils import EditionSourceReader, Utils
import time
import os
import sys
import PeriodFilter


year = 2019
if len(sys.argv) > 1:
    year = int(sys.argv[1])

tournaments = pickle.load(open('resources/periods.pkl', 'rb'))
tournaments = PeriodFilter.filter_tournaments_by_year(tournaments, year)
browser = Utils.get_browser()
for tournament in tournaments:
    print("Scraping " + str(year) + " " + tournament.name)
    dir_name = str(year) + "," + tournament.name
    dir_path = 'output/editions/' + dir_name + '/'
    if os.path.exists(dir_path + 'edition.pkl'):
        print("Edition has already been scraped")
        Utils.print_divider()
        continue
    try:
        pass
        edition_string = tournament.name + '-' + str(year)
        # results_source = EditionSourceReader.get_results_tab_source(browser, edition_string)
        bracket_sources = EditionSourceReader.get_bracket_sources(browser, edition_string)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # with open(dir_path + 'results.txt', 'wb') as output_file:
        #     output_file.write(results_source.encode('utf8'))

        bracket_serial_number = 1
        for bracket_source in bracket_sources:
            with open(dir_path + 'bracket' + str(bracket_serial_number) + '.txt', 'wb') as output_file:
                output_file.write(bracket_source.encode('utf8'))
            bracket_serial_number += 1
    except Exception as e:
        print ("Failed to scrape " + str(year) + " " + tournament.name + ": " + e.message)
        # traceback.print_exc()

    Utils.print_divider()
    time.sleep(5)
browser.quit()
