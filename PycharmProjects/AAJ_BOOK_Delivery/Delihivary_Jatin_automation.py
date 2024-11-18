import pandas as pd
import requests
from datetime import datetime
import re
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import gspread as Gsheet
from google.oauth2 import service_account
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
with open("credentialImportant.json", "r") as json_file:
    json_string= json.load(json_file)
SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/cloud-platform')
google_credentials = service_account.Credentials.from_service_account_info(json_string,scopes=SCOPES)

class Delhivery_Scrapping:
    def __init__(self):
        global span_value
        self.gc = Gsheet.authorize(google_credentials)
        spreadsheet = self.gc.open_by_key('16XjJ1OylHSXZdkl4EfuM8-PkGwbL6kRZKPPdrTmc31w')
        # Get the source and destination worksheets
        self.source_workbook = spreadsheet.worksheet('Final-Copy Paste')
        Data = self.source_workbook.get_all_values()  # Get all Values in the Sheet
        self.df = pd.DataFrame(Data[1:], columns=Data[0])
        self.url='https://www.delhivery.com/'
        self.driver = webdriver.Chrome()
        j=0

        for i in range(len(self.df)):
            if j>100:
                break

            if self.df.loc[i,'Flag_For_Extraction']!='Yes':
                try:
                    self.driver.get(self.url)
                    if len(self.df.loc[i,'GR No.'])==9:
                        j=j+1
                        self.WebScrappingLRN(self.df.loc[i,'GR No.'], i)
                    elif len(self.df.loc[i,'GR No.'])==13 or len(self.df.loc[i,'GR No.'])==14:
                        j = j + 1
                        self.WebScrappingLRNAWB(self.df.loc[i, 'GR No.'], i)

                except Exception as error:
                    print(error)

        df=self.df.iloc[:,1:-1]
        df = df.fillna('')
        data_to_insert = [df.columns.values.tolist()] + df.values.tolist()
        Update_range = "B1"
        self.source_workbook.update(range_name=Update_range, values=data_to_insert)
        print("done")




    def WebScrappingLRN(self,keys,m):
        self.driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/ul/li[4]/a').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/input').send_keys(keys)
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/button').click()
        # Wait for the page to load
        time.sleep(3)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]")))
        estimated_date = 0
        time.sleep(3)
        div_element = self.driver.find_element(By.XPATH,
                                          '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/p')
        div_html = div_element.get_attribute('outerHTML')
        soup = BeautifulSoup(div_html, 'html.parser')
        all_data = soup.find('p')
        EstimatedDate = all_data.get_text(strip=True)

        if len(EstimatedDate)>5:
            self.df.loc[m, 'Estimated  Delivary Date'] = EstimatedDate
        else:
            EstimatedDate = (f"{EstimatedDate[:2]}/{EstimatedDate[2:]}/2024")
            self.df.loc[m, 'Estimated  Delivary Date'] = self.convertdateformat(EstimatedDate)




        j = [13, 10, 20, 13]
        tpath = ['ff', ' //*[@id="collapse1"]/div/table/tbody', ' //*[@id="collapse2"]/div/table/tbody',
                 ' //*[@id="collapse3"]/div/table/tbody']

        try:
            element = self.driver.find_element(By.XPATH,'//*[@id="heading0"]')
            j = [13, 10, 20, 13]
            tpath = ['//*[@id="collapse0"]/div/table/tbody', ' //*[@id="collapse1"]/div/table/tbody', ' //*[@id="collapse2"]/div/table/tbody',
                     ' //*[@id="collapse3"]/div/table/tbody']
            li_of_xpath = [
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/h2/a/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[3]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[4]/div']
            p = 0
            g = 3
            for i in range(len(li_of_xpath)):
                Status_element = self.driver.find_element(By.XPATH, li_of_xpath[i])
                divv_html = Status_element.get_attribute('outerHTML')
                soup_soup = BeautifulSoup(divv_html, 'html.parser')
                all_datas = soup_soup.find('div')
                data_status = all_datas.get_text(strip=True)
                if len(data_status) > j[i]:
                    match = re.match(r'(\D+)(.*)', data_status)  # split databy if the staus have date


                    left_side = match.group(1).strip()  # left side
                    right_side = match.group(2).strip()  # right side data
                    self.df.iloc[m, g] = self.convertdateformatbyslace(right_side.split(",")[0])

                    g=g+1

            p=g-4
            if p != -1:
                try:
                    Status_table = self.driver.find_element(By.XPATH, tpath[p])
                    table_html = Status_table.get_attribute('outerHTML')
                    soup_table = BeautifulSoup(table_html, 'html.parser')
                    # Find all rows in the table
                    rows = soup_table.find_all('tr')
                    # Extract data from each row
                    data = []
                    for row in rows:
                        cols = row.find_all('td')
                        cols = [col.text.strip() for col in cols]
                        data.append(cols)
                    dff = pd.DataFrame(data, columns=['Date', 'Location', 'Status'])
                    dff = dff.tail(1).reset_index(drop=True)
                    dff.loc[0, 'Date'] = self.convertdateformatbyslace(dff.loc[0, 'Date'].split(",")[0])
                    self.df.loc[m, 'Current_Status Date'] = dff.loc[0, 'Date']
                    self.df.loc[m, 'Current_Location'] = dff.loc[0, 'Location']
                    self.df.loc[m, 'Current_Status'] = dff.loc[0, 'Status']
                    self.df.loc[m, 'Flag_For_Extraction'] = 'Yes'
                except NoSuchElementException as error:
                    print("Element not found:", error)

            time.sleep(3)

            # Element found, do something with it
        except:
            j = [13, 10, 20, 13]
            tpath = ['fff', ' //*[@id="collapse1"]/div/table/tbody', ' //*[@id="collapse2"]/div/table/tbody',
                     ' //*[@id="collapse3"]/div/table/tbody']
            li_of_xpath = [
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/h2/a/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[3]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[4]/div']
            p = 0
            g = 4
            for i in range(len(li_of_xpath)):
                Status_element = self.driver.find_element(By.XPATH, li_of_xpath[i])
                divv_html = Status_element.get_attribute('outerHTML')
                soup_soup = BeautifulSoup(divv_html, 'html.parser')
                all_datas = soup_soup.find('div')
                data_status = all_datas.get_text(strip=True)
                if len(data_status) > j[i]:
                    match = re.match(r'(\D+)(.*)', data_status)  # split databy if the staus have date
                    p=p+1

                    left_side = match.group(1).strip()  # left side
                    right_side = match.group(2).strip()  # right side data
                    self.df.iloc[m, g] = self.convertdateformatbyslace(right_side.split(",")[0])

                    g = g + 1



            if p != 0:
                try:
                    Status_table = self.driver.find_element(By.XPATH, tpath[p])
                    table_html = Status_table.get_attribute('outerHTML')
                    soup_table = BeautifulSoup(table_html, 'html.parser')
                    # Find all rows in the table
                    rows = soup_table.find_all('tr')
                    # Extract data from each row
                    data = []
                    for row in rows:
                        cols = row.find_all('td')
                        cols = [col.text.strip() for col in cols]
                        data.append(cols)
                    dff = pd.DataFrame(data, columns=['Date', 'Location', 'Status'])
                    dff = dff.tail(1).reset_index(drop=True)
                    dff.loc[0, 'Date'] = self.convertdateformatbyslace(dff.loc[0, 'Date'].split(",")[0])
                    self.df.loc[m, 'Current_Status Date'] = dff.loc[0, 'Date']
                    self.df.loc[m, 'Current_Location'] = dff.loc[0, 'Location']
                    self.df.loc[m, 'Current_Status'] = dff.loc[0, 'Status']
                    self.df.loc[m, 'Flag_For_Extraction'] = 'Yes'
                except NoSuchElementException as error:
                    print("Element not found:", error)


            time.sleep(3)
    def WebScrappingLRNAWB(self,keys,m):
        self.driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/ul/li[2]/a').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/input').send_keys(keys)
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/div[1]/button').click()
        # Wait for the page to load
        time.sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]")))
        estimated_date = 0
        time.sleep(2)
        div_element = self.driver.find_element(By.XPATH,
                                          '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/p')
        div_html = div_element.get_attribute('outerHTML')
        soup = BeautifulSoup(div_html, 'html.parser')
        all_data = soup.find('p')
        EstimatedDate = all_data.get_text(strip=True)

        if len(EstimatedDate)>5:
            self.df.loc[m, 'Estimated  Delivary Date'] = EstimatedDate
        else:
            EstimatedDate = (f"{EstimatedDate[:2]}/{EstimatedDate[2:]}/2024")
            self.df.loc[m, 'Estimated  Delivary Date'] = self.convertdateformat(EstimatedDate)




        j = [13, 10, 20, 13]
        tpath = ['ff', ' //*[@id="collapse1"]/div/table/tbody', ' //*[@id="collapse2"]/div/table/tbody',
                 ' //*[@id="collapse3"]/div/table/tbody']

        try:
            element = self.driver.find_element(By.XPATH,'//*[@id="heading0"]')
            j = [13, 10, 20, 13]
            tpath = ['//*[@id="collapse0"]/div/table/tbody', ' //*[@id="collapse1"]/div/table/tbody', ' //*[@id="collapse2"]/div/table/tbody',
                     ' //*[@id="collapse3"]/div/table/tbody']
            li_of_xpath = [
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/h2/a/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[3]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[4]/div']
            p = 0
            g = 3
            for i in range(len(li_of_xpath)):
                Status_element = self.driver.find_element(By.XPATH, li_of_xpath[i])
                divv_html = Status_element.get_attribute('outerHTML')
                soup_soup = BeautifulSoup(divv_html, 'html.parser')
                all_datas = soup_soup.find('div')
                data_status = all_datas.get_text(strip=True)
                if len(data_status) > j[i]:
                    match = re.match(r'(\D+)(.*)', data_status)  # split databy if the staus have date


                    left_side = match.group(1).strip()  # left side
                    right_side = match.group(2).strip()  # right side data
                    self.df.iloc[m, g] = self.convertdateformatbyslace(right_side.split(",")[0])

                    g=g+1

            p=g-4
            if p != -1:
                try:
                    Status_table = self.driver.find_element(By.XPATH, tpath[p])
                    table_html = Status_table.get_attribute('outerHTML')
                    soup_table = BeautifulSoup(table_html, 'html.parser')
                    # Find all rows in the table
                    rows = soup_table.find_all('tr')
                    # Extract data from each row
                    data = []
                    for row in rows:
                        cols = row.find_all('td')
                        cols = [col.text.strip() for col in cols]
                        data.append(cols)
                    dff = pd.DataFrame(data, columns=['Date', 'Location', 'Status'])
                    dff = dff.tail(1).reset_index(drop=True)
                    dff.loc[0, 'Date'] = self.convertdateformatbyslace(dff.loc[0, 'Date'].split(",")[0])
                    self.df.loc[m, 'Current_Status Date'] = dff.loc[0, 'Date']
                    self.df.loc[m, 'Current_Location'] = dff.loc[0, 'Location']
                    self.df.loc[m, 'Current_Status'] = dff.loc[0, 'Status']
                    self.df.loc[m, 'Flag_For_Extraction'] = 'Yes'
                except NoSuchElementException as error:
                    print("Element not found:", error)

            time.sleep(3)

            # Element found, do something with it
        except:
            j = [13, 10, 20, 13]
            tpath = ['fff', ' //*[@id="collapse1"]/div/table/tbody', ' //*[@id="collapse2"]/div/table/tbody',
                     ' //*[@id="collapse3"]/div/table/tbody']
            li_of_xpath = [
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[1]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/h2/a/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[3]/div',
                '/html/body/app-root[1]/app-new-unified-tracking-details/div/div/div/div/div[2]/div[1]/div[4]/div/div[2]/div/div[4]/div']
            p = 0
            g = 4
            for i in range(len(li_of_xpath)):
                Status_element = self.driver.find_element(By.XPATH, li_of_xpath[i])
                divv_html = Status_element.get_attribute('outerHTML')
                soup_soup = BeautifulSoup(divv_html, 'html.parser')
                all_datas = soup_soup.find('div')
                data_status = all_datas.get_text(strip=True)
                if len(data_status) > j[i]:
                    match = re.match(r'(\D+)(.*)', data_status)  # split databy if the staus have date
                    p=p+1

                    left_side = match.group(1).strip()  # left side
                    right_side = match.group(2).strip()  # right side data
                    self.df.iloc[m, g] = self.convertdateformatbyslace(right_side.split(",")[0])

                    g = g + 1



            if p != 0:
                try:
                    Status_table = self.driver.find_element(By.XPATH, tpath[p])
                    table_html = Status_table.get_attribute('outerHTML')
                    soup_table = BeautifulSoup(table_html, 'html.parser')
                    # Find all rows in the table
                    rows = soup_table.find_all('tr')
                    # Extract data from each row
                    data = []
                    for row in rows:
                        cols = row.find_all('td')
                        cols = [col.text.strip() for col in cols]
                        data.append(cols)
                    dff = pd.DataFrame(data, columns=['Date', 'Location', 'Status'])
                    dff = dff.tail(1).reset_index(drop=True)
                    dff.loc[0, 'Date'] = self.convertdateformatbyslace(dff.loc[0, 'Date'].split(",")[0])
                    self.df.loc[m, 'Current_Status Date'] = dff.loc[0, 'Date']
                    self.df.loc[m, 'Current_Location'] = dff.loc[0, 'Location']
                    self.df.loc[m, 'Current_Status'] = dff.loc[0, 'Status']
                    self.df.loc[m, 'Flag_For_Extraction'] = 'Yes'
                except NoSuchElementException as error:
                    print("Element not found:", error)


            time.sleep(3)





    def convertdateformat(self, datestr):

        date_obj = datetime.strptime(datestr, "%d/%b/%Y")
        # Format the date in the desired format
        formatted_date = date_obj.strftime("%d/%m/%Y")
        return formatted_date
    def convertdateformatbyslace(self, datestr):
        date_obj = datetime.strptime(datestr, "%d %b %Y")
        # Format the date in the desired format
        formatted_date = date_obj.strftime("%d/%m/%Y")
        return formatted_date

Delhivery_Scrapping()