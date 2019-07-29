import re
import time

import gspread
import math
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials
import random
scope = ['https://www.googleapis.com/auth/devstorage.read_write','https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Google Sheet-80a12669b8a0.json',scope)


def createColors(n):
    colors = []
    color_list = [i for i in range(0,256)]
    count = 0
    while count!= n:
        color = ""
        for _ in range(3):
            val = random.choice(color_list)
            color+=hex(val)[2:]
        if color not in colors :
            colors.append(color)
            count+=1
    return  colors


def removeStar(score):
    return float(score[:-1]) if "*" in score else float(score)


if __name__ == '__main__':

    while True:
        try:
            auth = gspread.authorize(credentials)

            google_sheet = auth.open("WorldCup2015_IndiaIndividualScores").sheet1

            data = google_sheet.get_all_values()
            break
        except Exception:
            print("Connection refused by server")
            time.sleep(1)

    #data = [['Match1', 'bat_first True', 'team_score 300', 'RG Sharma 15', 'S Dhawan 73', 'V Kohli 107', 'SK Raina 74', 'MS Dhoni (c) † 18', 'RA Jadeja 3', 'AM Rahane 0', 'R Ashwin 1*', 'Mohammed Shami 3*', '', ''], ['Match2', 'bat_first True', 'team_score 307', 'RG Sharma 0', 'S Dhawan 137', 'V Kohli 46', 'AM Rahane 79', 'SK Raina 6', 'MS Dhoni (c) † 18', 'RA Jadeja 2', 'R Ashwin 5*', 'Mohammed Shami 4*', '', ''], ['Match3', 'bat_first False', 'team_score 104', 'RG Sharma 57*', 'S Dhawan 14', 'V Kohli 33*', '', '', '', '', '', '', '', ''], ['Match4', 'bat_first False', 'team_score 185', 'RG Sharma 7', 'S Dhawan 9', 'V Kohli 33', 'AM Rahane 14', 'SK Raina 22', 'MS Dhoni (c) † 45*', 'RA Jadeja 13', 'R Ashwin 16*', '', '', ''], ['Match5', 'bat_first False', 'team_score 260', 'RG Sharma 64', 'S Dhawan 100', 'V Kohli 44*', 'AM Rahane 33*', '', '', '', '', '', '', ''], ['Match6', 'bat_first False', 'team_score 288', 'RG Sharma 16', 'S Dhawan 4', 'V Kohli 38', 'AM Rahane 19', 'SK Raina 110*', 'MS Dhoni (c) † 85*', '', '', '', '', ''], ['Match7', 'bat_first True', 'team_score 302', 'RG Sharma 137', 'S Dhawan 30', 'V Kohli 3', 'AM Rahane 19', 'SK Raina 65', 'MS Dhoni (c) † 6', 'RA Jadeja 23*', 'R Ashwin 3*', '', '', ''], ['Match8', 'bat_first False', 'team_score 233', 'RG Sharma 34', 'S Dhawan 45', 'V Kohli 1', 'AM Rahane 44', 'SK Raina 7', 'MS Dhoni (c) † 65', 'RA Jadeja 16', 'R Ashwin 5', 'Mohammed Shami 1*', 'MM Sharma 0', 'UT Yadav 0']]

    print(data)
    batsmen_scores = {}

    for match in data:
        for player_score in match[3:]:
            if player_score!='':
                player_details = player_score.split()
                score = player_details[-1]
                name = " ".join(player_details[:-1])

                if name in batsmen_scores.keys():
                    batsmen_scores[name]["score"] += removeStar(score)
                    if "*" not in score:
                        batsmen_scores[name]["outcount"] += 1

                else:
                    batsmen_scores[name] = { }
                    batsmen_scores[name]["score"] = removeStar(score)

                    batsmen_scores[name]["outcount"] = 1 if "*" not in score else 0




    print(batsmen_scores)


    players = list(batsmen_scores.keys())
    plt.figure(figsize=(20, 10))


    scores = []
    for player in players :
        score = math.floor(batsmen_scores[player]["score"]/batsmen_scores[player]["outcount"]) if batsmen_scores[player]["outcount"] >1 else math.floor(batsmen_scores[player]["score"])
        scores.append(score)
        print(player,score)


    plt.title = "World cup 2015 average scores of indian batsmen on Barchart"

    plt.xlabel = "Players"
    plt.ylabel = "Average Scores"


    x = [i for i in range(len(players))]


    plt.ylim([min(scores)-5,max(scores)+5])

    #colors = createColors(len(players))

    colors = ["C"+str(i) for i in range(len(players))]
    print(colors)

    plt.bar(x,height = scores , label = "2015", color=colors,align='center',width=0.5)


    plt.xticks(x, players)
    plt.legend()


    plt.savefig(fname = "World cup 2015 average scores of indian batsmen on barchart")
