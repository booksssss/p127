from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

startUrl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome('./chromedriver.exe')
browser.get(startUrl)

time.sleep(10)
planetData = []
headers = ["name", "light years from earth", "planet mass", "stellar magnitude", "discovery date", "hyperlink"]

def scrape():
    for i in range(1,2): #two options: stay in page or go to back to list.
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser") # making an object of the beautiful soup to convert html into text. page source is nasa website, and parse it as a html content. 
            currentPageNo= int(soup.find_all("input", attrs = {"class", "page_num"})[0].get("value"))
           #comparing the left and right with i to make sure that the correct data is being pulled out using .get()
            if currentPageNo < i:
                browser.find_element(By.XPATH,value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a') #navigating through links through selenium for the right
            elif currentPageNo > i:
                browser.find_element(By.XPATH,value = '//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a')#navigating through links through selenium for the left
            else:
                break

        for ultag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            litags = ultag.find_all("li")
            templist = []
            for index, litag in enumerate(litags): #we need enumerate to give index; becaue the first index is the hyperlink, which is considred different
                if index == 0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0]) #if first index, extract the tag, otherwise extract data in tag
                    except:
                        templist.append("")#put something empty
            hyperlinkLitag = litags[0]
            templist.append("https://exoplanets.nasa.gov"+hyperlinkLitag.find_all("a", href = True)[0]["href"])
            planetData.append(templist)
        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()  #uses selenium
        print(f"print{i} scrapping completed")

            
            
        
scrape()
planetDf1 = pd.DataFrame(planetData, columns= headers) #any file as a tabular dataframe
planetDf1.to_csv("updatedScrapper.csv", index = True, index_label= "id")
