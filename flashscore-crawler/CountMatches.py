import pickle
from utils import Utils

'''
Counts the amount of matches at it appears in the generated edition data.
Relies only on locally stored info - No crawling here.
'''


with open('resources/tournament-names.txt', 'r') as f:
    tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]
    # tournament_names = ["australian-open", "acapulco"]

total_num_of_matches = 0
years = [2019]
for year in years:
    for tournament_name in tournament_names:
        try:
            edition_pkl_path = 'output/editions/' + str(year) + ',' + tournament_name + '/edition.pkl'
            edition = pickle.load(open(edition_pkl_path, 'rb'))
            match_ids = edition.get_match_ids()
            total_num_of_matches += len(match_ids)
            print(str(year) + " " + tournament_name + " " + str(len(match_ids)))
        except:
            print(str(year) + " " + tournament_name + ": Failed to count matches")
Utils.print_divider()
print(total_num_of_matches)

