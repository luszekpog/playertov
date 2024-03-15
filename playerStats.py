import pandas as pd
import datetime
class playerStats:
    def __init__(self, player_id):
        self.player_id = player_id

    async def playerCommonInfo(self):
        from nba_api.stats.endpoints import commonplayerinfo
        data = commonplayerinfo.CommonPlayerInfo(
            player_id=self.player_id
        ).get_data_frames()[0]
        currentyear = datetime.datetime.now().year
        birthdate = data.iloc[0]['BIRTHDATE']
        birthdate = birthdate[0:4]
        age = int(currentyear) - int(birthdate)
        return data.iloc[0]['TEAM_ID'],data.iloc[0]['ROSTERSTATUS'],data.iloc[0]['FIRST_NAME'],data.iloc[0]['LAST_NAME'],data.iloc[0]['POSITION'],age
    async def getSeasonStats(self):
        from nba_api.stats.endpoints import playercareerstats

        data = playercareerstats.PlayerCareerStats(
            player_id=self.player_id
            ).get_data_frames()[0]
        data = data.tail(1)
        if(data.empty):
            avgmin = 0
            avgast = 0
            avgtov = 0
            avgstl=0
        else:
            gp = data.iloc[0]["GP"]
            playermin = data.iloc[0]["MIN"]
            ast = data.iloc[0]["AST"]
            tov=data.iloc[0]["TOV"]
            stl = data.iloc[0]["STL"]
            avgmin = round(playermin/gp,2) 
            avgast = round(ast/gp,2)
            avgtov = round(tov/gp,2)
            avgstl = round(stl/gp,2)
        
        return avgmin,avgast,avgtov,avgstl
    async def getNextGame(self):
        from nba_api.stats.endpoints import playernextngames

        data = playernextngames.PlayerNextNGames(
            number_of_games=1,
            player_id=self.player_id
            ).get_data_frames()[0]
      
            
        return data.iloc[0]['HOME_TEAM_ID'],data.iloc[0]['VISITOR_TEAM_ID'],data.iloc[0]["GAME_DATE"],data.iloc[0]["HOME_TEAM_NAME"],data.iloc[0]["VISITOR_TEAM_NAME"],data.iloc[0]["GAME_TIME"]
        
    def getLastGames(self):
        from nba_api.stats.endpoints import playergamelog
        data = playergamelog.PlayerGameLog(
            player_id=self.player_id
            ).get_data_frames()[0]
        data = data.iloc[:10]
        minutes=0
        ast=0
        tov =0
        for i in range(0,10):
            minutes += data.iloc[i]["MIN"]
            ast +=data.iloc[i]["AST"]
            tov +=data.iloc[i]["TOV"]
        return round(minutes/10,2),round(ast/10,2),round(tov/10,2),data.iloc[0]["GAME_DATE"]