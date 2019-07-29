import time

import gspread
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/devstorage.read_write','https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Google Sheet-80a12669b8a0.json',scope)

if __name__ == '__main__':
    while True:
        try:
            auth = gspread.authorize(credentials)

            google_sheet = auth.open("WorldCup2015_IndiaIndividualScores").sheet1

            data = google_sheet.get_all_values()

            matches = []
            scores = []

            for match in data:
                bat_first = match[1].split()[1]

                if bat_first == 'True':
                    team_score = match[2].split()[1]

                    matches.append(match[0])
                    scores.append(int(team_score))
            print(matches, scores)
            break
        except Exception:
            print("Connection refused by server")
            time.sleep(5)
            matches = [1,2,3]
            scores = [34,67,78]
            break

    fig, p = plt.subplots()

    plt.ylim([min(scores) - 5, max(scores) + 5])
    p.plot(matches, scores, label="2015", color='green', linestyle='dashed', linewidth=3, marker='o',
             markerfacecolor='blue', markersize=6)


    p.set(xlabel = "Matches",ylabel = "Scores",title = "World cup 2015 matches and scores of india batted first" )
    p.legend()

    fig.savefig(fname="World cup 2015 matches and scores of india batted first")