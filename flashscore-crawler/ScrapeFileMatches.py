import sys
import time
from utils import Utils
import MatchScraping

file_name = sys.argv[1]
with open(file_name, 'r') as f:
    match_ids = f.readlines()

browser = Utils.get_browser()
current = 1
total = len(match_ids)
for match_id in match_ids:
    print(Utils.get_time_prefix() + "Scraping match " + match_id + " [" + str(current) + "/" + str(total) + "]")
    should_wait = True
    try:
        should_wait = MatchScraping.scrape_match(browser, match_id)
    except:
        print("Failed to scrape match")
    if should_wait:
        time.sleep(5)
    current += 1
browser.quit()
