import pickle
import os


def year_in_period(year, period):
    if len(period) == 1:
        return year == period[0]
    # len(period) == 2
    return period[0] <= year <= period[1]


tournaments = pickle.load(open('resources/periods.pkl', 'rb'))
year = 2018
print_missing = False
for tournament in tournaments:
    if year_in_period(year, tournament.periods[0]):
        edition_pkl_path = 'output/editions/' + str(year) + ',' + tournament.name + '/edition.pkl'
        if not os.path.exists(edition_pkl_path):
            print(tournament.name + ': No pkl')
            continue
        edition = pickle.load(open(edition_pkl_path, 'rb'))
        match_ids = edition.get_match_ids()
        scraped_matches_counter = 0
        missing_matches = []
        for match_id in match_ids:
            if os.path.exists('output/matches/' + match_id + '/history.txt'):
                scraped_matches_counter += 1
            else:
                missing_matches.append(match_id)
        print(tournament.name + ': ' + str(scraped_matches_counter) + "/" + str(len(match_ids)))
        if print_missing:
            print("Missing matches: " + str(missing_matches))
