def get_edition_raw_sources_dict(browser, edition_string):
    edition_raw_sources_dict = dict()
    entry_keys = ['results', 'draw', 'standings']
    edition_url = 'https://www.flashscore.com/tennis/atp-singles/' + edition_string + '/'
    for key in entry_keys:
        browser.get(edition_url + key + '/')
        edition_raw_sources_dict[key] = browser.page_source
    return edition_raw_sources_dict
