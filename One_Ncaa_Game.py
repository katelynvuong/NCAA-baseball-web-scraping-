from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd #for exporting data into csv

url = 'https://www.ncaa.com/scoreboard/baseball/d1/2023/06/25/all-conf'
chrome_path = 'Users/katelynvuong/Downloads/chromedriver'


chrome_options = Options()
#chrome_options.add_argument("--headless") 
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)
driver.implicitly_wait(5)
game = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "gamePod-link")))
game.click()
driver.implicitly_wait(5)
tabs_container = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'tabs-container')))
driver.execute_script("arguments[0].scrollIntoView();", tabs_container)
tabs = tabs_container.find_elements(By.TAG_NAME, 'a')[1]
tabs.click()
driver.implicitly_wait(5)
table = driver.find_element(By.ID, "gamecenterAppContent")
innings = table.find_elements(By.TAG_NAME, "tbody" )
team = []
play = []


for inning in innings:
    rows = inning.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 2:
            team_name = cells[0].find_element(By.TAG_NAME, "img").get_attribute("alt")
            title = team_name.split(" title=")[0]
            team.append(title)
            play.append(cells[1].text)


df = pd.DataFrame({'Team': team , 'Play' : play})
df.to_csv('LSU_FLORI_202306250.csv')
print(df)


driver.quit()
