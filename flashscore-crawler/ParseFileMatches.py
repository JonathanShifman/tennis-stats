import sys
import MatchParsing

if len(sys.argv) < 2:
    print('No file chosen')
    exit(0)

file_name = sys.argv[1]
with open(file_name, 'r') as f:
    match_ids = [match_id.strip() for match_id in f.readlines()]

current = 1
total = len(match_ids)
for match_id in match_ids:
    try:
        MatchParsing.parse_match(match_id)
    except Exception as e:
        print("Failed to parse match " + match_id + ': ' + e.message)
    current += 1
