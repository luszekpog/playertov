from nba_api.stats.static import players,teams
import pandas as pd

class getData:
    def __init__(self,full_name):
        self.full_name = full_name
    async def findPlayer(self):
        try:
            player = players.find_players_by_full_name(self.full_name)
            player_id = player[0]['id']
            return player_id
        except:
            print("Nie znaleziono zawodnika!")
            


    