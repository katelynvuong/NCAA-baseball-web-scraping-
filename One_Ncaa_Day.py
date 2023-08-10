from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from collections import OrderedDict
import pandas as pd #for exporting data into csv

def team_naming(team_list): #FIX: remove spaces from team names
    unique_teams = list(OrderedDict.fromkeys(team_list))
    home_team = unique_teams[1]
    away_team = unique_teams[0]

    return home_team, away_team


def get_data(innings):
    team =[]
    play =[]
    for inning in innings:
        rows = inning.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                team_name = cells[0].find_element(By.TAG_NAME, "img").get_attribute("alt")
                title = team_name.split(" title=")[0]
                team.append(title)
                play.append(cells[1].text)

    home_team, away_team = team_naming(team)
    df = pd.DataFrame({'Team': team , 'Play' : play})
    csv_filename = f'{home_team}_{away_team}_202306100.csv'
    df.to_csv(csv_filename, index=False)




url = 'https://www.ncaa.com/scoreboard/baseball/d1/2023/06/10/all-conf'
chrome_path = 'Users/katelynvuong/Downloads/chromedriver'


chrome_options = Options()
#chrome_options.add_argument("--headless") 
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)
driver.implicitly_wait(5)
games = driver.find_elements(By.CLASS_NAME, "gamePod-link")


for i in range(len(games)):
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
    get_data(innings)
    driver.get(url) 

 
    
    
driver.quit()