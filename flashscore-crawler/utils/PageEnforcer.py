import time
from bs4 import BeautifulSoup


def edition_results_loaded(soup):
    return len(soup.find_all("tr", {"class": "stage-finished"})) > 0


def edition_more_results_loaded(soup, num_of_matches_before_click):
    return len(soup.find_all("tr", {"class": "stage-finished"})) > num_of_matches_before_click


def edition_bracket_loaded(soup):
    return len(soup.find_all("div", {"class": "match"})) > 0


def enforce(browser, check_function, condition_meaning="", timeout=10, check_interval=1, initial_wait=-1,
            additional_params=None):
    if condition_meaning is not None and len(condition_meaning) > 0:
        print("Enforcing condition: " + condition_meaning)

    if initial_wait < 0:
        initial_wait = check_interval

    soup = BeautifulSoup(browser.page_source, "html.parser")
    print("Waiting for initial check for " + str(initial_wait) + " seconds")
    time.sleep(initial_wait)
    time_passed = initial_wait
    while time_passed < timeout:
        if additional_params is None:
            condition_satisfied = check_function(soup)
        else:
            condition_satisfied = check_function(soup, additional_params)
        if condition_satisfied:
            print("Condition satisfied")
            return
        print("Condition not satisfied. Waiting an interval of " + str(check_interval) + " seconds")
        time.sleep(check_interval)
        time_passed += check_interval
    print("Timeout exceeded")
    raise Exception("Timeout exceeded")
