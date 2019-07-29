import json
import matplotlib
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

TEAM = "india"
class Match:
    def __init__(self,team_score,batsmen,bat_first):
        self.bat_first = bat_first
        self.team_score = team_score
        self.batsmen = batsmen


class Batman:
    def __init__(self, player_name,score):
        self.player_name = player_name
        self.score  = score



def getMatchDetails(innings_li,bat_first):
    batsmen_div = innings_li.find_elements_by_class_name("wrap.batsmen")
    batsmen = []
    for batman in batsmen_div:
        player_name = batman.find_element_by_class_name("cell.batsmen").find_element_by_tag_name("a").text
        score = batman.find_element_by_class_name("cell.runs").text
        out_notout = batman.find_element_by_class_name("cell.commentary").text

        if "not out" in out_notout:
            score+="*"
        batsmen.append(Batman(player_name,score).__dict__)

    team_score = innings_li.find_element_by_class_name("wrap.total").find_elements_by_class_name("cell")[1].text.split()[0].split("/")[0]

    return Match(team_score,batsmen,bat_first).__dict__


def getMatchScorecard(innings1_li, innings2_li, TEAM=None):
    innings1_team_name = innings1_li.find_element_by_tag_name("h2").text
    innings2_team_name = innings2_li.find_element_by_tag_name("h2").text

    if TEAM in innings1_team_name:
        return getMatchDetails(innings1_li,True)

    return getMatchDetails(innings2_li,False)


def getWorldCup2015_Scorecard():

    time_taken_each_url = []
    driver = webdriver.Chrome()

    start_time = time.time()
    driver.get("http://www.espncricinfo.com/icc-cricket-world-cup-2015/engine/series/509587.html")

    time_taken_each_url.append(time.time()-start_time)
    assert "Results" in driver.title
    ul = driver.find_elements_by_xpath("//*[@id='viewport']/div[3]/div/div[4]/div/div[1]/div/div/ul/li")

    even = 0
    urls = []
    for li in ul:
        if even % 2 == 0:
            inner_li_a = li.find_element_by_tag_name("a")

            scorecardLink = inner_li_a.get_attribute("href")

            if TEAM in scorecardLink:
                urls.append(scorecardLink)

                
        even += 1

    assert "No results found." not in driver.page_source

    world_cup_2015 = []
    matchCount = 1
    total_matches = len(urls)
    print("Urls Fetching Completed!\nGetting Results ...")
    for url in urls:

        start_time = time.time()
        driver.get(url)
        time_taken_each_url.append(time.time() - start_time)

        inningsList = driver.find_elements_by_class_name("accordion-item")

        match = getMatchScorecard(inningsList[0],inningsList[1],TEAM[0].upper()+TEAM[1:])

        world_cup_2015.append(match)

        print(int(100 - ((total_matches - matchCount) / total_matches) * 100), "% Done", end='\n')

        matchCount += 1
    driver.close()

    print("Average response time : ",sum(time_taken_each_url)/len(time_taken_each_url))

    return world_cup_2015


if __name__ == '__main__':
    print("Getting Urls ...")

    world_cup_2015 = getWorldCup2015_Scorecard()


    print("Completed!")


    print("Opening File ...")
    file = open("indian_individual_batsmen_score.txt","w+")

    print("Writing into file ...")

    jsonFormat = json.dump(world_cup_2015,file,indent=4)


    file.close()

    print("Process Successfully Completed!")