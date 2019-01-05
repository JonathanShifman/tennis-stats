def found_page(source):
    return 'The requested page can\'t be displayed' not in source


def get_edition_url(edition_string):
    return 'https://www.flashscore.com/tennis/atp-singles/' + edition_string + '/'
