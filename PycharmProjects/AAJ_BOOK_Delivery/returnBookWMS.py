import pandas as pd
import requests
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
class ReturnBook:
    def __init__(self):
        self.gc = Gsheet.authorize(google_credentials)
        Spreadsheet=self.gc.open_by_key('17l41CxYGp-s1w76BhfYDct0hKjHRWRcueR9NLJ-LOkg')
        self.ReturnBookSheet=Spreadsheet.worksheet('Return_DataPython')
        data=self.ReturnBookSheet.get_all_values()
        self.df=pd.DataFrame(data=data[1:],columns=data[0])
        #Web scraping configuration
        self.username = 'hemant.girase@uolo.com'
        self.password = 'uolo@123'
        self.url = 'https://wms.aajenterprises.com/login.aspx'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        time.sleep(3)
        self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtName').send_keys(self.username)
        self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(self.password)
        self.driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_btnLogin').click()
        time.sleep(40)
        self.loopfunction()

    def loopfunction(self):
        self.driver.find_element(By.XPATH,'//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//*[@id="ctl00_BtnConsSR"]/div[2]/p').click()
        time.sleep(3)
        for i in range(len(self.df)):
            key=self.df.loc[i,'SR number']
            print(key)
            try:

                if ('24-25' in key)  and ('SR' in key) and  ( self.df.loc[i,'SR Report Link']=='') and (self.df.loc[i,'Status']=='Done'):
                    row=i+2
                    part_name=self.df.loc[i,'Flag for Part']
                    time.sleep(4)
                    self.driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()
                    time.sleep(2)
                    if part_name=='Part 1':
                        self.driver.find_element(By.ID, "ctl00_dpfin").send_keys('2024-2025')
                    elif part_name=='Part 2':
                        self.driver.find_element(By.ID, "ctl00_dpfin").send_keys('2024-2025_II')

                    time.sleep(3)
                    url=self.getData(key)
                    self.ReturnBookSheet.update([[url]],f"S{row}")

            except ValueError:
                pass
            self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtSrNo').clear()

    def getData(self,sales_id):
        try:

            self.driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_txtSrNo').send_keys(sales_id)
            time.sleep(3)
            self.driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_btnShw').click()
            time.sleep(3)

            element_present = EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_Panel1'))
            timeout = 40
            WebDriverWait(self.driver, timeout).until(element_present)

            time.sleep(10)
            getdata = self.driver.find_element(By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody')
            table_html = getdata.get_attribute('outerHTML')
            soup = BeautifulSoup(table_html, 'html.parser')
            data = []
            for tr in soup.find_all('tr'):
                row = [item.text for item in tr.find_all('th')]
                value = [item.text for item in tr.find_all('td')]
                combine = row + value
                data.append(combine)
            df=pd.DataFrame(data=data[1:],columns=data[0])
            time.sleep(2)
            MCopy_ExternalSheet = self.gc.create(f'{sales_id}_Spreadsheet')
            MCopy_ExternalSheet.share("", perm_type="anyone", role="writer")
            DataSheet=MCopy_ExternalSheet.worksheet('Sheet1')
            df = df.fillna('')
            data_to_insert = [df.columns.values.tolist()] + df.values.tolist()
            Update_range = "A1"
            time.sleep(2)
            DataSheet.update(range_name=Update_range, values=data_to_insert)
            print(MCopy_ExternalSheet.url)
            return MCopy_ExternalSheet.url
            
        except NoSuchElementException:
            print("error")
            pass
        except Exception as error :
            print(error)






ReturnBook()