from getData import getData
from playerStats import playerStats
from opponentsStats import opponentsStats
import os
import time
import webbrowser

class PlayerInformation:
    def __init__(self, name):
        self.name = name
        
    async def initialize_data(self):
        self.data_instance = getData(self.name)

        self.player_id = await self.data_instance.findPlayer()
        self.stats_instance = playerStats(self.player_id)
        self.player_common_info = await self.stats_instance.playerCommonInfo()
        self.player_stats = await self.stats_instance.getSeasonStats()
        self.player_next_game = await self.stats_instance.getNextGame()
        self.game_stats = await self.calculate_game_stats()

        self.opponents_id = await self.getOpponentTeamId()
        self.opponents_instance = opponentsStats(self.opponents_id)
        self.opponents_stl = await self.opponents_instance.getOpponentsSteals()
        self.h2hstats = await self.opponents_instance.getH2HStats(self.player_id)
        self.matchup = await self.opponents_instance.getMatchupStats(self.player_common_info[4])
       

    async def print_next_game_info(self):
        print(f'{self.player_common_info[2]} {self.player_common_info[3]} | {self.player_common_info[4]} - Next game: {self.player_next_game[3]} vs. {self.player_next_game[4]} at {self.player_next_game[5]} | {self.player_next_game[2]} ')

    async def calculate_game_stats(self):
        avg_min = self.player_stats[0]
        avg_ast = self.player_stats[1]
        avg_tov = self.player_stats[2]
        player_last_games = playerStats(self.player_id).getLastGames()
        min_diff = round(player_last_games[0] - avg_min, 2)
        ast_diff = round(player_last_games[1] - avg_ast, 2)
        tov_diff = round(player_last_games[2] - avg_tov, 2)
        last_game = player_last_games[3][4:6]
        next_game = self.player_next_game[2][4:6]
        if(int(next_game) - int(last_game) == 1):
            is_b2b = True
        else:
            is_b2b=False
        return min_diff, ast_diff, tov_diff, is_b2b,player_last_games[2]
    
    async def getOpponentTeamId(self):
        if(self.player_common_info[0] ==self.player_next_game[0]):     
            opponent_team = self.player_next_game[1] 
        else:     
            opponent_team = self.player_next_game[0]

        return opponent_team
 
