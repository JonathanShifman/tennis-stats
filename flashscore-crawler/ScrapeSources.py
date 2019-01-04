from utils import SourceReader
import time
from selenium import webdriver
import os

with open('resources/tournament-names.txt', 'r') as f:
    # tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]
    tournament_names = ['australian-open']

browser = webdriver.Chrome()
for year in range(2018, 2019):
    for tournament_name in tournament_names:
        print("Parsing " + str(year) + " " + tournament_name)
        edition_string = tournament_name + '-' + str(year)
        results_source = SourceReader.get_results_tab_source(browser, edition_string)
        bracket_sources = SourceReader.get_bracket_sources(browser, edition_string)

        dir_name = str(year) + ',' + tournament_name
        dir_path = 'output/' + dir_name + '/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(dir_path + 'results.txt', 'wb') as output_file:
            output_file.write(results_source.encode('utf8'))

        bracket_serial_number = 1
        for bracket_source in bracket_sources:
            with open(dir_path + 'bracket' + str(bracket_serial_number) + '.txt', 'wb') as output_file:
                output_file.write(bracket_source.encode('utf8'))
            bracket_serial_number += 1

        time.sleep(1)
browser.quit()
