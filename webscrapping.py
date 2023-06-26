from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv

startUrl = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome('./chromedriver.exe')
browser.get(startUrl)

time.sleep(10)

scraped_data = []

def scrape():
    soup = BeautifulSoup(browser.page_source, "html.parser")
    bright_star_table = soup.find("table", attrs = {"class", "wikitable"})
    table_body = bright_star_table.find('tbody')
    table_rows = table_body.find_all('tr')

    for row in table_rows:
        table_cols = row.find_all('td')
        # print(table_cols)
        temp_list = []

        for col_data in table_cols:
            data = col_data.text.strip()
            # print(data)
            temp_list.append(data)
        scraped_data.append(temp_list)

    stars_data = []
    
    for i in range(0, len(scraped_data)):

        Star_names = scraped_data[i][1]
        Distance = scraped_data[i][3]
        Mass = scraped_data[i][5]
        Radius = scraped_data[i][6]
        Luminosity = scraped_data[i][7]

        requiared_data = [Star_names, Distance, Mass, Radius, Luminosity]
        stars_data.append(requiared_data)
    
    headers = ['Star_names', 'Distance','Mass','Radius','Luminosity']
    star_df_1 = pd.DataFrame(stars_data, columns=headers)

    star_df_1.to_csv('scraped_data.csv', index = True, index_label="id")
         
scrape()
            
