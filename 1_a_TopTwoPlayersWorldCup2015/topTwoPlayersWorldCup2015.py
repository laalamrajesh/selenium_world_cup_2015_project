import json

import matplotlib
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

SUMMARY = "game"
TEAM = "india"
class Batman:
    def __init__(self, player_name,score,balls):
        self.player_name = player_name
        self.score  = score
        self.balls = balls

    def convert_to_dict(self):
        return {"player_name": self.player_name, "score": self.score, "balls": self.balls}
    def __str__(self):
        return str(self.convert_to_dict())

    def __repr__(self):
        return str(self.convert_to_dict())

class Bowler:
    def __init__(self, player_name,wickets,runs_conceded,overs):
        self.player_name = player_name
        self.runs_conceded  = runs_conceded
        self.overs = overs
        self.wickets = wickets

    def convert_to_dict(self):
        return {"player_name": self.player_name, "wickets" : self.wickets,"runs_conceded": self.runs_conceded, "overs": self.overs}

    def __str__(self):
        return str(self.convert_to_dict())

    def __repr__(self):
        return str(self.convert_to_dict())

class Team:
    def __init__(self,team_name,top_batsmen,top_bowlers):
        self.team_name = team_name
        self.top_batsmen = top_batsmen
        self.top_bowlers  = top_bowlers

    def convert_to_dict(self):
        return { "team_name" : self.team_name, "top_batsmen":[x.convert_to_dict() for x in self.top_batsmen] , "top_bowlers" : [x.convert_to_dict() for x in self.top_bowlers]}


    def __str__(self):
        return str(self.convert_to_dict())

    def __repr__(self):
        return str(self.convert_to_dict())

def getBatsmenDetails(li):
    top_batsmen = []

    for element in li:
        player_name = element.find_element_by_tag_name("a").text
        score_balls = element.find_element_by_tag_name("span").text.split(" (")

        score = score_balls[0]
        balls = score_balls[1][:-1]


        top_batsmen.append(Batman(player_name,score,balls))

    return  top_batsmen

def getBowlerDetails(li):
    top_bowlers = []


    for element in li:
        player_name = element.find_element_by_tag_name("a").text
        wickets_runs_overs = element.find_element_by_tag_name("span").text.split("/")

        wickets = wickets_runs_overs[0]
        runs_overs = wickets_runs_overs[1].split(" (")

        runs_conceded = runs_overs[0]
        overs = runs_overs[1][:-1]

        top_bowlers.append(Bowler(player_name,wickets,runs_conceded,overs))

    return  top_bowlers


def swapBowlers(match):
    try:

        match[0]["top_bowlers"] , match[1]["top_bowlers"] = match[1]["top_bowlers"] , match[0]["top_bowlers"]

    except:
        pass

def getMatchSummary(summaryList):

    match = []
    for inning in summaryList:
        players_ul = inning.find_elements_by_class_name("two-col-table")
        batsmen_li = players_ul[0].find_elements_by_tag_name("li")
        bowlers_li = players_ul[1].find_elements_by_tag_name("li")

        team_name_list = inning.find_element_by_tag_name("x-span").text.split()[:-1]
        team_name = " ".join(team_name_list)
        top_batsmen =  getBatsmenDetails(batsmen_li)
        top_bowlers = getBowlerDetails(bowlers_li)

        match.append(Team(team_name,top_batsmen,top_bowlers).convert_to_dict())

    swapBowlers(match)
    return match


def getWorldCup2015_Summary():
    driver = webdriver.Chrome()
    driver.get("http://www.espncricinfo.com/icc-cricket-world-cup-2015/engine/series/509587.html")
    assert "Results" in driver.title
    ul = driver.find_elements_by_xpath("//*[@id='viewport']/div[3]/div/div[4]/div/div[1]/div/div/ul/li")

    even = 0
    urls = []
    for li in ul:
        if even %2 ==0 :
            inner_li_a = li.find_element_by_tag_name("a")

            summaryLink = inner_li_a.get_attribute("href").replace("scorecard",SUMMARY)
            if TEAM in summaryLink:
                urls.append(summaryLink)

        even+=1

    assert "No results found." not in driver.page_source

    world_cup_2015 = []
    matchCount = 1
    total_matches = len(urls)
    print("Urls Fetching Completed!\nGetting Results ...")
    for url in urls:

        driver.get(url)
        summaryList = driver.find_elements_by_class_name("inning")

        match = getMatchSummary(summaryList)

        world_cup_2015.append( match)

        print(int(100-((total_matches-matchCount)/total_matches)*100),"% Done",end = '\n')

        matchCount+=1
    driver.close()

    return  world_cup_2015






if __name__ == '__main__':
    print("Getting Urls ...")

    world_cup_2015 = getWorldCup2015_Summary()


    print("Completed!")


    print("Opening File ...")
    file = open("world_cup_2015_match_wise_top_2_players.txt","w+")

    print("Writing into file ...")

    jsonFormat = json.dump(world_cup_2015,file,indent=4)


    file.close()

    print("Process Successfully Completed!")