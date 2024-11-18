import pandas as pd
import requests
from datetime import datetime
import re
import time
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
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

class TracingWb_Scrapping:
    def __init__(self):
        global span_value
        self.gc = Gsheet.authorize(google_credentials)
        spreadsheet = self.gc.open_by_key('16XjJ1OylHSXZdkl4EfuM8-PkGwbL6kRZKPPdrTmc31w')
        # Get the source and destination worksheets
        self.source_workbook = spreadsheet.worksheet('SafeExpress FInal Copypaste')
        self.url='https://www.safexpress.com/'
        Data = self.source_workbook.get_all_values()  # Get all Values in the Sheet
        self.df = pd.DataFrame(Data[1:], columns=Data[0])
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        j=0
        time.sleep(8)
        timeout = 40
        element_present = EC.presence_of_element_located(
            (By.XPATH, '/html/body/app-root/app-home/section/app-home-tracking/section/div/div/form[1]/div[4]/input'))
        WebDriverWait(self.driver, timeout).until(element_present)
        for i in range(len(self.df)):
            if self.df.loc[i,'Flag_For_Extraction']!='Yes':
                try:
                    if j>5:
                      break
                    j+=1

                    self.webScrappingFun(self.df.loc[i,'GR No.'],i)
                except Exception as error:
                    id=''
                    time.sleep(2)
                    self.driver.find_element(By.XPATH,'/html/body/app-root/app-home/section/app-home-tracking/section/div/div/form[1]/div[4]/input').send_keys(id)
                    time.sleep(2)

        df = self.df.iloc[:,1:]
        df = df.fillna('')
        data_to_insert = [df.columns.values.tolist()] + df.values.tolist()
        Update_range = "B1"
        self.source_workbook.update(range_name=Update_range, values=data_to_insert)
        print("done")


    def webScrappingFun(self,id,m):

        self.driver.find_element(By.XPATH,'/html/body/app-root/app-home/section/app-home-tracking/section/div/div/form[1]/div[4]/input').send_keys(id)
        time.sleep(4)
        self.driver.find_element(By.XPATH, '/html/body/app-root/app-home/section/app-home-tracking/section/div/div/form[1]/button').click()
        time.sleep(3)
        timeout=20
        element_present = EC.presence_of_element_located(
            (By.XPATH, '/html/body/app-root/app-home/section/app-home-tracking/section/div[2]'))
        #
        WebDriverWait(self.driver, timeout).until(element_present)
        # destination Status
        div_destination_element = self.driver.find_element(By.XPATH,'/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[2]/div[3]/span[3]')
        des_html = div_destination_element.get_attribute('outerHTML')
        soup_d = BeautifulSoup(des_html, 'html.parser')
        destinationtext=soup_d.get_text(strip=True)
        self.df.loc[m,'Destination']=destinationtext

        # PickUp Status
        PickupElement=self.driver.find_element(By.XPATH,'/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[2]/div[2]/span[3]')
        pic_html=PickupElement.get_attribute('outerHTML')
        Soup_p=BeautifulSoup(pic_html,'html.parser')
        pic_text=Soup_p.get_text(strip=True)
        self.df.loc[m,'Pick Up']=pic_text

        # Delivary Status

        div_element = self.driver.find_element(By.XPATH,'/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[3]')
        div_html = div_element.get_attribute('outerHTML')
        soup = BeautifulSoup(div_html, 'html.parser')
        all_data = soup.find('div')
        all_datas=all_data.get_text(strip=True)
        status=''
        if all_data:
            status_date_pairs = re.findall(r'([A-Z\s]+)(\d{2}-[A-Z][a-z]{2}-\d{4})',all_datas)
            # Convert the pairs into a flat list
            result_list = [item for pair in status_date_pairs for item in pair]
            try:
                self.df.loc[m, 'Shipping Date'] = self.convertdateformat(result_list[1])
                self.df.loc[m, 'In-transit'] = self.convertdateformat(result_list[3])
                self.df.loc[m, 'Arrived Destination'] = self.convertdateformat(result_list[5])
                self.df.loc[m, 'Out For Delivery'] = self.convertdateformat(result_list[7])
                self.df.loc[m, 'Delivered'] = self.convertdateformat(result_list[9])
                self.df.loc[m,'Flag_For_Extraction']='Yes'
                status='Delivered'



            except IndexError:
                #Shipping date
                listpath=['/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[3]/div[1]','/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[3]/div[2]','/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[3]/div[3]','/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[3]/div[4]','/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[3]/div[5]']
                df_columnname=[self.df.loc[m, 'Shipping Date'],self.df.loc[m, 'In-transit'],self.df.loc[m, 'Arrived Destination'],self.df.loc[m, 'Out For Delivery'],self.df.loc[m, 'Delivered']]
                lenstatus = ['Shipping Date', 'In-transit', 'Arrived Destination', 'Out For Delivery', 'Delivered']
                for pa in range(len(listpath)):
                    Xpath=listpath[pa]
                    try:
                        div_element = self.driver.find_element(By.XPATH, Xpath)
                        div_html = div_element.get_attribute('outerHTML')
                        soup = BeautifulSoup(div_html, 'html.parser')
                        pic = soup.get_text(separator=',', strip=True).split(',')
                        self.df.loc[m, 'Flag_For_Extraction'] = 'Yes'

                        if len(pic) == 2:
                            date = self.convertdateformat(pic[1])
                            df_columnname[pa] = date
                            status=lenstatus[pa]
                    except NoSuchElementException:
                        pass
        self.df.loc[m,'Current_Status']=status

        time.sleep(3)
        self.driver.find_element(By.XPATH,'/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[1]/span').click()
        time.sleep(3)
        try:
            self.driver.find_element(By.XPATH,
                                     '/html/body/app-root/app-home/section/app-home-tracking/section/div[2]/div[1]/span').click()
            time.sleep(3)
        except:
            pass





    def convertdateformat(self, datestr):
        date_obj = datetime.strptime(datestr, "%d-%b-%Y")
        # Format the date in the desired format
        formatted_date = date_obj.strftime("%d/%m/%Y")
        return formatted_date




TracingWb_Scrapping()
