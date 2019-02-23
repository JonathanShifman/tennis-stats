from utils import EditionSourceReader, Utils
import time
from selenium import webdriver
import os
import traceback

with open('resources/tournament-names.txt', 'r') as f:
    tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]
    # tournament_names = ['cordoba']

browser = webdriver.Chrome()
for year in range(2019, 2020):
    for tournament_name in tournament_names:
        dir_name = str(year) + "," + tournament_name
        dir_path = 'output/editions/' + dir_name + '/'
        if os.path.exists(dir_path):
            continue
        try:
            print("Scraping " + str(year) + " " + tournament_name)
            edition_string = tournament_name + '-' + str(year)
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
            print ("Failed to parse " + str(year) + " " + tournament_name + ": " + e.message)
            # traceback.print_exc()

        Utils.print_divider()
        Utils.print_divider()
        time.sleep(5)
browser.quit()
