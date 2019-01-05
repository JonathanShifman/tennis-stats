from utils import MatchSourceReader
from selenium import webdriver
import os

match_id = "hUHPU31G"
browser = webdriver.Chrome()
summary_source, set_sources = MatchSourceReader.get_match_sources(browser, match_id)

dir_path = 'output/matches/' + match_id + '/'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

with open(dir_path + 'summary.txt', 'wb') as output_file:
    output_file.write(summary_source.encode('utf8'))

set_number = 1
for set_source in set_sources:
    with open(dir_path + 'set' + str(set_number) + '.txt', 'wb') as output_file:
        output_file.write(set_source.encode('utf8'))
        set_number += 1

browser.quit()
