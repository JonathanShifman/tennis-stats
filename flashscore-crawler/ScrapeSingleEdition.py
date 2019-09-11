import sys
import os
from utils import Utils, EditionSourceReader

if len(sys.argv) < 2:
    print ('No tournament chosen')
    exit(1)
tournament_name = sys.argv[1]
if len(sys.argv) < 3:
    year = 2019
else:
    year = int(sys.argv[2])


browser = Utils.get_browser()
print("Scraping " + str(year) + " " + tournament_name)
dir_name = str(year) + "," + tournament_name
dir_path = 'output/editions/' + dir_name + '/'
if os.path.exists(dir_path + 'bracket1.txt'):
    print("Edition has already been scraped")
    Utils.print_divider()
    exit(0)
try:
    pass
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
    print ("Failed to scrape " + str(year) + " " + tournament_name + ": " + e.message)
    # traceback.print_exc()

browser.quit()
