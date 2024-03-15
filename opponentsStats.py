from playerStats import playerStats
import pandas as pd
from bs4 import BeautifulSoup
import requests
class opponentsStats:
    def __init__(self,opponent_team_id):
        self.opponent_team_id = opponent_team_id
        
    async def getOpponentsSteals(self):
        from nba_api.stats.endpoints import teamyearbyyearstats

        data = teamyearbyyearstats.TeamYearByYearStats(
            team_id=self.opponent_team_id
            ).get_data_frames()[0]
        data = data.iloc[-1]
        stl = data["STL"]
        gp = data["GP"]
        avgstl = round(stl/gp,2)
        return avgstl
    
    async def getH2HStats(self,player_id):
        from nba_api.stats.endpoints import teamvsplayer
        data = teamvsplayer.TeamVsPlayer(
            team_id=self.opponent_team_id,
            last_n_games=3,
            vs_player_id=player_id,
            measure_type_detailed_defense="Base",
        ).get_data_frames()[0]  
        stl = round(data["STL"]/3,2)
        stl = stl[0]
        return stl
    
    async def getMatchupStats(self,position):
        from nba_api.stats.endpoints import commonteamroster
        data = commonteamroster.CommonTeamRoster(
            team_id=self.opponent_team_id
        ).get_data_frames()[0]
        position_sign=position[0]
        possible_matchups=[]
        for i in range(0,len(data)):
            if(data.iloc[i]["POSITION"].find(position_sign)):
                possible_matchups.append(data.iloc[i]["PLAYER_ID"])

        rivals_stats=[]
        rival_stl =[]
      
        for i in range(0,len(possible_matchups)):
            rivals_stats.append(await playerStats(possible_matchups[i]).getSeasonStats())
            if(rivals_stats[i][3] >= 0.5):
                rival_stl.append(rivals_stats[i][3])

        return rival_stl


        

                

    