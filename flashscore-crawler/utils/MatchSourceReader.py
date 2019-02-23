from utils import Utils
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_match_sources(browser, match_id):
    match_url = Utils.get_match_url(match_id)
    browser.get(match_url + "#match-summary")
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "parts")))
    summary_source = browser.page_source

    browser.get(match_url + "#point-by-point")
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "tab-mhistory-1-history")))
    history_source = browser.page_source

    return summary_source, history_source

