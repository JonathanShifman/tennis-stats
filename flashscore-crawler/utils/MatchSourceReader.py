from utils import Utils
import time


def get_match_sources(browser, match_id):
    summary_tab_url = Utils.get_match_url(match_id) + "#match-summary"
    browser.get(summary_tab_url)
    summary_source = browser.page_source

    browser.find_element_by_xpath("//a[contains(@id, 'a-match-history')]").click()
    time.sleep(3)  # FIXME
    set_sources = []
    set_link_li_elements = browser.find_elements_by_xpath("//li[contains(@id, 'mhistory')]")
    for set_link_li_element in set_link_li_elements:
        set_link_element = set_link_li_element.find_element_by_tag_name("a")
        set_link_element.click()
        time.sleep(1)  # FIXME
        set_sources.append(browser.page_source)
    return summary_source, set_sources

