import asyncio
from player_information import PlayerInformation
from turnoverAspects import TurnoverAspects
import customtkinter
import webbrowser


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

async def return_def_rtg(entry4,question_window,odds,tov_bet,player_info):
    def_rtg = float(entry4.get())
    def_rtg = round(def_rtg,2)
    question_window.destroy()
    result_window = customtkinter.CTk()
    tov_aspects = TurnoverAspects(
            avg_minutes=player_info.player_stats[0],
            avg_assists=player_info.player_stats[1],
            avg_turnovers=player_info.game_stats[4],
            tov_diff=player_info.game_stats[2],
            ast_diff=player_info.game_stats[1],
            min_diff=player_info.game_stats[0],
            is_b2b=player_info.game_stats[3],
            opponent_steals=player_info.opponents_stl,
            opponent_stealsh2h=player_info.h2hstats,
            matchup_steals=player_info.matchup,
            opponent_defRating=def_rtg,
            player_age=player_info.player_common_info[5],
            bet_odds=odds,
            tov_bet=tov_bet)
    results = await tov_aspects.calculate_chances()    
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    result_window.minsize(300, 300)
    result_window.title("Results")

    result_info = f"With this odds your bookmaker gives you: {results[1]} % chances.\n My algorithm gives you: {results[0]}% chances. \nI think: {results[2]}"

    result_label = customtkinter.CTkLabel(result_window, padx=10, pady=10,text=result_info)
    result_label.pack()

    result_window.mainloop()
def get_def_rtg(odds,tov_bet,name):
    root.destroy()
    player_info = PlayerInformation(name)
    asyncio.run(player_info.initialize_data())
    url = f"https://www.nba.com/stats/team/{player_info.opponents_id}/advanced"
    question_window = customtkinter.CTk()
    question_window.title("Defensive Rating")

    label4 = customtkinter.CTkLabel(question_window, text="Opponents defensive rating statistic (DEFRTG) is not supported in any free API,\n but it is needed. Please check it out and enter here:")
    label4.grid(row=0, column=0, padx=20, pady=10)
    
    
    entry4 = customtkinter.CTkEntry(question_window)
    entry4.grid(row=0, column=1, columnspan=2, padx=20, pady=10)
 
    enter_button = customtkinter.CTkButton(question_window, text="Submit", command=lambda: asyncio.run(return_def_rtg(entry4,question_window,odds,tov_bet,player_info)))
    enter_button.grid(row=1, column=1, padx=20, pady=10)
    webbrowser.open(url)
    question_window.mainloop()
   

def button_clicked():
    name=entry.get()
    tov_bet = float(entry2.get())
    tov_bet = round(tov_bet,2)

    odds = float(entry3.get())
    odds = round(odds,2)
    
    get_def_rtg(odds,tov_bet,name)


root = customtkinter.CTk()
root.minsize(300, 300)
root.title("Turnover Odds")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="Enter player name:")
label1.pack(pady=12,padx=10)

entry = customtkinter.CTkEntry(master=frame)
entry.pack(pady=0,padx=10)

label2 = customtkinter.CTkLabel(master=frame, text="Enter player's line of turnovers:")
label2.pack(pady=12,padx=10)

entry2 = customtkinter.CTkEntry(master=frame)
entry2.pack(pady=0,padx=10)

label3 = customtkinter.CTkLabel(master=frame, text="Enter odds here: ")
label3.pack(pady=12,padx=10)

entry3 = customtkinter.CTkEntry(master=frame)
entry3.pack(pady=0,padx=10)

submit_button = customtkinter.CTkButton(master=frame ,text="Submit",command=lambda: button_clicked())
submit_button.pack(pady=12,padx=10)


root.mainloop()


    