import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


def addRow(row, match_row):
    for index, value in enumerate(match_row):
        google_sheet.update_cell(row, index+1,value)


if __name__ == '__main__':

    scope = ['https://www.googleapis.com/auth/devstorage.read_write','https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('Google Sheet-80a12669b8a0.json',scope)


    while True:
        try:
            auth = gspread.authorize(credentials)
            google_sheet = auth.open('WorldCup2015_IndiaIndividualScores').sheet1

            break
        except Exception:
            print("Connection refused by server")

            time.sleep(1)

    file = open("indian_individual_batsmen_score.txt", "r+")

    data = json.load(file)
    print("Connection Success")

    cell_list = []
    for match_no in range(1, len(data) + 1):
        match = data[match_no - 1]
        match_row = ["Match" + str(match_no)]

        match_row.append("bat_first " + str(match["bat_first"]))
        match_row.append("team_score " + match["team_score"])

        batsmen = match["batsmen"]

        for batman in batsmen:
            match_row.append(batman["player_name"] + " " + batman["score"])

        col_cell = 64+len(match_row)
        cells = google_sheet.range('A'+str(match_no)+':'+chr(col_cell)+str(match_no))

        index = 0
        for cell in cells:
            cell.value = match_row[index]
            cell_list.append(cell)
            index+=1
    print(cell_list)
    google_sheet.update_cells(cell_list)





