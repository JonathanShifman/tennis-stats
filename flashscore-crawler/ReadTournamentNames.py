from selenium import webdriver
from bs4 import BeautifulSoup

# FIXME
'''
Currently parses paths from 'Current tournaments' section as well (in addition to the desired 'Categories' section)
Includes all tournaments without filtering (Davis cup for example)
'''


def get_source():
    edition_results_url = 'https://www.flashscore.com/tennis/'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(edition_results_url)
    page_source = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()
    return page_source


source = get_source()
relevant_elements = source.find_all(lambda element:
                                    (element.name == 'a' and 'href' in element.attrs and
                                     '/tennis/atp-singles/' in element['href']))

lines = []
for element in relevant_elements:
    split_path = element.attrs['href'].split('/')
    if len(split_path) == 5:
        lines.append(str(split_path[3] + '\n'))

with open('output/tournament-names.txt', 'wb') as f:
    f.writelines(lines)
