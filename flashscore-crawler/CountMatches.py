import pickle
from utils import Utils


def count_matches_in_edition(year, tournament_name):
    dir_name = str(year) + "," + tournament_name
    dir_path = "output/editions/" + dir_name + "/"
    edition = pickle.load(open(dir_path + "edition.pkl", "rb"))
    num_of_matches = 0
    num_of_matches_per_bracket = []
    for bracket in edition.brackets:
        num_of_matches_in_current_bracket = 0
        for edition_round in bracket.rounds:
            num_of_matches += len(edition_round.match_ids)
            num_of_matches_in_current_bracket += len(edition_round.match_ids)
        num_of_matches_per_bracket.append(num_of_matches_in_current_bracket)
    return num_of_matches, num_of_matches_per_bracket


with open('resources/tournament-names.txt', 'r') as f:
    tournament_names = [tournament_name.strip() for tournament_name in f.readlines()]
    # tournament_names = ["australian-open", "acapulco"]

total_num_of_matches = 0
for tournament_name in tournament_names:
    try:
        num_of_matches_in_edition, num_of_matches_per_bracket = count_matches_in_edition(2018, tournament_name)
        total_num_of_matches += num_of_matches_in_edition
        print(str(2018) + " " + tournament_name + " " + str(num_of_matches_per_bracket))
    except:
        print("Failed to count matches")
Utils.print_divider()
print(total_num_of_matches)

