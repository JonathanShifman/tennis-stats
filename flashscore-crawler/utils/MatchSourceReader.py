from utils import Utils
import time


def get_match_sources(browser, match_id):
    summary_tab_url = Utils.get_match_url(match_id) + "#match-summary"
    browser.get(summary_tab_url)
    summary_source = browser.page_source

    time.sleep(2)  # FIXME
    browser.find_element_by_xpath("//a[contains(@id, 'a-match-history')]").click()
    time.sleep(2)  # FIXME
    history_source = browser.page_source

    return summary_source, history_source

