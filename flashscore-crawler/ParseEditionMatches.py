from MatchParsing import *
import sys

if len(sys.argv) < 2:
    print ('No tournament chosen')
    exit(1)
tournament_name = sys.argv[1]
if len(sys.argv) < 3:
    year = 2019
else:
    year = int(sys.argv[2])

parse_edition_matches(year, tournament_name)
