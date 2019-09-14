def year_in_period(year, period):
    if len(period) == 1:
        return year == period[0]
    # len(period) == 2
    return period[0] <= year <= period[1]


def year_in_tournament_periods(year, tournament):
    for period in tournament.periods:
        if year_in_period(year, period):
            return True
    return False


def filter_tournaments_by_year(tournaments, year):
    filtered = []
    for tournament in tournaments:
        if year_in_tournament_periods(year, tournament):
            filtered.append(tournament)
    return filtered