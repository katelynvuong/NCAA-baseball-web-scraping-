from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from collections import OrderedDict
import pandas as pd 
from urllib.parse import urlsplit

def team_naming(team_list): # returns home and away team 
    unique_teams = list(OrderedDict.fromkeys(team_list))
    unique_teams = [team.replace(" ", "") for team in unique_teams]
    home_team = unique_teams[1]
    away_team = unique_teams[0]

    return home_team, away_team


def get_data(innings, date): #extracting and exporting data into a csv file for each game
    url_parts = urlsplit(driver.current_url) #getting the game ID
    game_id = url_parts.path.split('/')[-2]
    team =[]
    play =[]
    for inning in innings: # extracts play by play data and appends to 'team' and 'play' lists
        rows = inning.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                team_name = cells[0].find_element(By.TAG_NAME, "img").get_attribute("alt")
                title = team_name.split(" title=")[0]
                team.append(title)
                play.append(cells[1].text)

    home_team, away_team = team_naming(team)
    df = pd.DataFrame({'Team': team , 'Play' : play}) #creates dataframe for 'team' and 'play
    csv_filename = f'{away_team}_{home_team}_{date}_{game_id}.csv' #FIXED: creates a {date} and {gameID}
    df.to_csv(csv_filename, index=False) #exports dataframe into a csv file 



url = 'https://www.ncaa.com/scoreboard/baseball/d1/2023/06/11/all-conf'
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
driver.implicitly_wait(5)
games = driver.find_elements(By.CLASS_NAME, "gamePod-link")

date_parts = url.split('/') #getting the date
date = ''.join(date_parts[-4:-1])

for i in range(len(games)): #looping through each game, clicks through all the necessary buttons to get to the play-by-play data
    games = driver.find_elements(By.CLASS_NAME, "gamePod-link") 
    game = games[i]
    game.click()
    driver.implicitly_wait(5)
    tabs_container = driver.find_element(By.CLASS_NAME, 'tabs-container')
    driver.implicitly_wait(5)
    driver.execute_script("arguments[0].scrollIntoView();", tabs_container)
    tabs = tabs_container.find_elements(By.TAG_NAME, 'a')[1]
    tabs.click()
    driver.implicitly_wait(5)
    table = driver.find_element(By.ID, "gamecenterAppContent")
    innings = table.find_elements(By.TAG_NAME, "tbody" )
    get_data(innings, date) #where all the magic happens 
    driver.get(url) 

 
    
    
driver.quit()
