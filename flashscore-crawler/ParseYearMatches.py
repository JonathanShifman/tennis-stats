from MatchParsing import *
import sys


def year_in_period(year, period):
    if len(period) == 1:
        return year == period[0]
    # len(period) == 2
    return period[0] <= year <= period[1]


tournaments = pickle.load(open('resources/periods.pkl', 'rb'))
if len(sys.argv) < 2:
    year = 2019
else:
    year = int(sys.argv[1])


for tournament in tournaments:
    if year_in_period(year, tournament.periods[0]):
        try:
            parse_edition_matches(year, tournament.name)
        except Exception as e:
            print ('Failed to parse edition: ' + e.message)
