from bs4 import BeautifulSoup
import SourceReader
import time
from selenium import webdriver
import pickle
import Utils


with open('tournament-names.txt', 'r') as f:
    # tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]
    tournament_names = ['halle']

for year in range(2018, 2019):
    browser = webdriver.Chrome()
    for tournament_name in tournament_names:
        edition_raw_sources_dict = SourceReader.get_edition_raw_sources_dict(browser, tournament_name + '-' + str(year))
        for key in edition_raw_sources_dict:
            current_source = edition_raw_sources_dict[key]
            if Utils.found_page(current_source):
                with open('output/' + str(year) + ',' + tournament_name + ',' + key + '.txt', 'wb') as output_file:
                    output_file.write(current_source.encode('utf8'))
                current_source_outcome = 'SUCCESS'
            else:
                current_source_outcome = 'FAILURE'
            print(','.join([str(year), tournament_name, key, current_source_outcome]))
        time.sleep(1)
    browser.quit()
a = 1

