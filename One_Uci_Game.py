from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd #for exporting data into csv



url = 'https://ucirvinesports.com/sports/baseball/stats/2023/tulane/boxscore/11733'
chrome_path = 'Users/katelynvuong/Downloads/chromedriver'

# got this block of code from the internet to help fix an error 
chrome_options = Options()
#chrome_options.add_argument("--headless") 
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


driver.get(url)
play_by_play_button = driver.find_element("id", 'ui-id-2') #clicking on the play-by-play button using unique id
play_by_play_button.click()

innings = driver.find_elements(By.TAG_NAME, 'tbody')


play = []
tulane_score = []
uci_score = []


for inning in innings:
    rows = inning.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) == 3: #so we don't get the data from the first table
            if cells[0].text != '': # so we get rid of the empty values and all the columns are the same length
                play.append(cells[0].text)
            if cells[1].text != '':  
                tulane_score.append(cells[1].text)
            if cells[2].text != '':  
                uci_score.append(cells[2].text)

df = pd.DataFrame({'Play': play , 'Tulane Score' : tulane_score, 'UCI Score': uci_score})
df.to_csv('uci_tulane_2172023.csv')
print(df)


driver.quit()





