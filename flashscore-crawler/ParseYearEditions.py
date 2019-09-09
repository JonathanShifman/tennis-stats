from EditionParsing import *
from utils import Utils
import sys


year = 2019
if len(sys.argv) > 1:
    year = int(sys.argv[1])

tournament_names = Utils.get_tournament_names()
for tournament_name in tournament_names:
    try:
        parse_edition(str(year), tournament_name)
    except Exception as e:
        print("Failed to parse edition: " + str(year) + " " + tournament_name + ": " + e.message)
