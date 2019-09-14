from utils import Utils
import sys
import MatchScraping


if len(sys.argv) < 2:
    print ('No tournament chosen')
    exit(1)
tournament_name = sys.argv[1]
if len(sys.argv) < 3:
    year = 2019
else:
    year = int(sys.argv[2])

browser = Utils.get_browser()
MatchScraping.scrape_matches_from_edition(browser, year, tournament_name)
browser.quit()
