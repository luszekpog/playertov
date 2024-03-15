class TurnoverAspects:
    def __init__(self, avg_turnovers,opponent_steals,opponent_defRating,avg_minutes,matchup_steals,is_b2b,avg_assists,opponent_stealsh2h,tov_diff,ast_diff,min_diff,player_age,bet_odds,tov_bet):
        self.avg_turnovers = avg_turnovers##
        self.avg_assists = avg_assists##
        self.avg_minutes = avg_minutes##
        self.tov_diff = tov_diff##
        self.ast_diff = ast_diff##
        self.min_diff = min_diff##
        self.is_b2b = is_b2b##
        self.opponent_steals = opponent_steals##
        self.opponent_stealsh2h = opponent_stealsh2h##
        self.matchup_steals = matchup_steals##
        self.bet_odds = bet_odds#
        self.player_age = player_age##
        self.opponent_defRating = opponent_defRating##
        self.tov_bet = tov_bet##

    async def calculate_chances(self):
        points = 0 
        max_point = 32
        random_events = 5
        bet_odds_probability = 1 / self.bet_odds * 100

        if self.is_b2b:
            points += 1

        if self.min_diff > 0 and self.ast_diff > 0:
            points += 2
        if self.tov_diff > 0:
            points += 2

        if self.player_age < 23 or self.player_age >= 33:
            points += 2

        if 117 <= self.opponent_defRating < 119:
            points += 1
        elif 115 <= self.opponent_defRating < 117:
            points += 2
        elif 113 <= self.opponent_defRating < 115:
            points += 3
        elif self.opponent_defRating < 113:
            points += 4

        if self.opponent_steals < self.opponent_stealsh2h:
            points += 2
        
        all_matchup_steals = round(sum(self.matchup_steals), 2)
        if 2.5 <= all_matchup_steals < 3.5:
            points += 1
        elif 3.5 <= all_matchup_steals < 5.5:
            points += 2
        elif 5.5 <= all_matchup_steals < 7.5:
            points += 3
        elif all_matchup_steals >= 7.5:
            points += 5

        if 6.25 <= self.opponent_steals < 6.25:
            points += 1
        elif 6.25 <= self.opponent_steals < 7.25:
            points += 2
        elif 7.25 <= self.opponent_steals < 8.25:
            points += 3
        elif self.opponent_steals >= 8.25:
            points += 4

        if self.avg_minutes >= 25:
            points += 2
        
        if 2.5 <= self.avg_assists < 3.5:
            points += 1
        elif self.avg_assists >= 3.5:
            points += 2

        tov_diff = self.avg_turnovers - self.tov_bet
        if 0.1 <= tov_diff <= 0.15:
            points += 1
        elif 0.15 < tov_diff <= 0.3:
            points += 3
        elif 0.3 < tov_diff <= 0.4:
            points += 5
        elif 0.4 < tov_diff <= 0.5:
            points += 6
        elif tov_diff > 0.5:
            points += 7

        if(self.tov_bet == 0.5):
            points += 3

        points_probability = ((points - random_events) / max_point) * 100
        points_probability = round(points_probability, 2)
        bet_odds_probability = round(bet_odds_probability, 2)

        diff_probability = points_probability - bet_odds_probability
        
        if 3 <= diff_probability:
            is_playable = "It's a value bet"
        elif  0 <= diff_probability < 3:
            is_playable = "Bookmaker is right"
        else:
            is_playable ="It is a bad bet"

        if(points_probability>60):
            is_playable = "It's a good bet"
        elif(points_probability<25):
            is_playable = "you shoud play under"

        return points_probability, bet_odds_probability, is_playable

            