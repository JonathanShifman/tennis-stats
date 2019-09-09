import pickle

from utils import EditionSourceReader, Utils
import time
import os
import traceback


def year_in_period(year, period):
    if len(period) == 1:
        return year == period[0]
    # len(period) == 2
    return period[0] <= year <= period[1]


def year_in_tournament_periods(year, tournament):
    for period in tournament.periods:
        if year_in_period(year, period):
            return True
    return False


tournaments = pickle.load(open('resources/periods.pkl', 'rb'))
browser = Utils.get_browser()
for year in range(2018, 2019):
    for tournament in tournaments:
        if year_in_tournament_periods(year, tournament):
            dir_name = str(year) + "," + tournament.name
            dir_path = 'output/editions/' + dir_name + '/'
            if os.path.exists(dir_path + 'edition.pkl'):
                continue
            try:
                print("Scraping " + str(year) + " " + tournament.name)
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
                print ("Failed to parse " + str(year) + " " + tournament.name + ": " + e.message)
                # traceback.print_exc()

            Utils.print_divider()
            Utils.print_divider()
            time.sleep(5)
browser.quit()
