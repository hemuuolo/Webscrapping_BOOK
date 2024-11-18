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

#authentication with Google cloud
with open("credentialImportant.json", "r") as json_file:
    json_string= json.load(json_file)
SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/cloud-platform')
google_credentials = service_account.Credentials.from_service_account_info(json_string,scopes=SCOPES)
class AAJ_Update:
    def __init__(self):
        #Get access to the sheet and all tabs with related data
        self.gc = Gsheet.authorize(google_credentials)
        self.Spreadsheet=self.gc.open_by_key('1WuKlyMSUlbDyMJQXhxVg_m_kyJ8-JsGU55LUEDRWrm0')
        self.transpoprtation_Allocation_Sheet=self.Spreadsheet.worksheet('Transpoprtation Allocation')
        self.Awaiting_Pickup_Sheet=self.Spreadsheet.worksheet('Awaiting Pickup')
        self.Awaiting_Delivery_Beyond_EDD_Sheet=self.Spreadsheet.worksheet('Awaiting delivery beyond EDD')
        self.Awaiting_Delivery_Within_EDD_Sheet=self.Spreadsheet.worksheet('Awaiting delivery within EDD')
        self.Shipment_Delivered_Sheet=self.Spreadsheet.worksheet('Shipment Delivered')
        self.PODs_Pending_To_Update_Sheet=self.Spreadsheet.worksheet("POD's pending to update")

        #declare the credentials and urls
        self.username = 'hemant.girase@uolo.com'
        self.password = 'uolo@123'
        self.url = 'https://app.aajswift.com/login'
        # Open_Chrome_Browser5
        driver=webdriver.Chrome()
        driver.get(self.url)
        #the selenium task now continue
        time.sleep(4)
        # driver.find_element(By.XPATH, '/html/body/div[4]/div/section[2]/div/div[2]/div/div[2]/div/div/a/span/span').click()
        # time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div[1]/form/div[1]/input').send_keys(self.username)
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div[1]/form/div[2]/input').send_keys(self.password)
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="root"]/div/div[3]/div[1]/form/button').click()
        time.sleep(50)
        self.Transportation_Allocation(driver)
        self.Awaiting_Pickup(driver)
        self.Awaiting_Delivery_Beyond_EDD(driver)
        self.Awaiting_Delivery_Within_EDD(driver)
        self.Shipment_Delivered(driver)
        self.PODs_Pending_To_Update(driver)

    def Transportation_Allocation(self,driver):
        try:
            driver.find_element(By.XPATH, '//*[@id="react-tabs-1"]/div/div/div[2]/div[3]/div[2]/div[3]/div[1]/span').click()
            time.sleep(3)
            # get header Data
            
            getdata = driver.find_element(By.XPATH, '//*[@id="id"]/thead')
            htmldata = getdata.get_attribute('outerHTML')
            soup = BeautifulSoup(htmldata, 'html.parser')
            headers = soup.find_all('th', class_='fixed-header')
            capital_letters = [header.text.title() for header in headers]
            # get all data
            getrowdata = driver.find_element(By.XPATH, '//*[@id="id"]')
            rowdataHTML = getrowdata.get_attribute('outerHTML')
            htmlrowData = BeautifulSoup(rowdataHTML, 'html.parser')
            rows = htmlrowData.find('tbody').find_all('tr')
            rowdata = []
            for row in rows:
                data = [cell.text.strip() for cell in row.find_all('td')]
                rowdata.append(data)
            df = pd.DataFrame(rowdata, columns=capital_letters)
            Odf = df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            self.transpoprtation_Allocation_Sheet.clear()
            self.transpoprtation_Allocation_Sheet.update(range_name=Update_range, values=data_to_insert)
            driver.find_element(By.XPATH, '//*[@id="custompopup"]/span/h3/span').click()
        except NoSuchElementException :
            print("Transportation_Allocation data is not")


    def Awaiting_Pickup(self,driver):
        try:
            
            driver.find_element(By.XPATH, '//*[@id="react-tabs-1"]/div/div/div[2]/div[3]/div[2]/div[3]/div[1]/span').click()
            time.sleep(3)
            # get header Data
           
            getdata = driver.find_element(By.XPATH, '//*[@id="id"]')
            htmldata = getdata.get_attribute('outerHTML')
            print("get element data")
            soup = BeautifulSoup(htmldata, 'html.parser')
            headers = soup.find_all('th', class_='fixed-header')
            capital_letters = [header.text.title() for header in headers]
            # get all data
            getrowdata = driver.find_element(By.XPATH, '//*[@id="id"]/tbody')
            rowdataHTML = getrowdata.get_attribute('outerHTML')
            htmlrowData = BeautifulSoup(rowdataHTML, 'html.parser')
            rows = htmlrowData.find('tbody').find_all('tr')
            rowdata = []
            for row in rows:
                data = [cell.text.strip() for cell in row.find_all('td')]
                rowdata.append(data)
            df = pd.DataFrame(rowdata, columns=capital_letters)
            Odf = df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            self.Awaiting_Pickup_Sheet.clear()
            self.Awaiting_Pickup_Sheet.update(range_name=Update_range, values=data_to_insert)
            driver.find_element(By.XPATH, '//*[@id="custompopup"]/span/h3/span').click()
        except NoSuchElementException :
            print("Awaiting_Pickup data is not")


    def Awaiting_Delivery_Beyond_EDD(self,driver):
        try:
            time.sleep(2)
            
            driver.find_element(By.XPATH, '//*[@id="react-tabs-1"]/div/div/div[2]/div[3]/div[3]/div[3]/div[1]/span').click()
            time.sleep(3)
            # get header Data
            getdata = driver.find_element(By.XPATH, '//*[@id="id"]')
            htmldata = getdata.get_attribute('outerHTML')
            soup = BeautifulSoup(htmldata, 'html.parser')
            headers = soup.find_all('th', class_='fixed-header')
            capital_letters = [header.text.title() for header in headers]
            # get all data
            getrowdata = driver.find_element(By.XPATH, '//*[@id="id"]/tbody')
            rowdataHTML = getrowdata.get_attribute('outerHTML')
            htmlrowData = BeautifulSoup(rowdataHTML, 'html.parser')
            rows = htmlrowData.find('tbody').find_all('tr')
            rowdata = []
            for row in rows:
                data = [cell.text.strip() for cell in row.find_all('td')]
                rowdata.append(data)
            df = pd.DataFrame(rowdata, columns=capital_letters)
            Odf = df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            self.Awaiting_Delivery_Beyond_EDD_Sheet.clear()
            self.Awaiting_Delivery_Beyond_EDD_Sheet.update(range_name=Update_range, values=data_to_insert)
            driver.find_element(By.XPATH, '//*[@id="custompopup"]/span/h3/span').click()
        except NoSuchElementException :
            print("Awaiting_Delivery_Beyond_EDD data is not")


    def Awaiting_Delivery_Within_EDD(self,driver):
        try:
            driver.find_element(By.XPATH, '//*[@id="react-tabs-1"]/div/div/div[2]/div[3]/div[4]/div[3]/div[1]/span').click()
            time.sleep(3)
            # get header Data
            getdata = driver.find_element(By.XPATH, '//*[@id="id"]/thead')
            htmldata = getdata.get_attribute('outerHTML')
            soup = BeautifulSoup(htmldata, 'html.parser')
            headers = soup.find_all('th', class_='fixed-header')
            capital_letters = [header.text.title() for header in headers]
            # get all data
            getrowdata = driver.find_element(By.XPATH, '//*[@id="id"]/tbody')
            rowdataHTML = getrowdata.get_attribute('outerHTML')
            htmlrowData = BeautifulSoup(rowdataHTML, 'html.parser')
            rows = htmlrowData.find('tbody').find_all('tr')
            rowdata = []
            for row in rows:
                data = [cell.text.strip() for cell in row.find_all('td')]
                rowdata.append(data)
            df = pd.DataFrame(rowdata, columns=capital_letters)
            Odf = df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            self.Awaiting_Delivery_Within_EDD_Sheet.clear()
            self.Awaiting_Delivery_Within_EDD_Sheet.update(range_name=Update_range, values=data_to_insert)
            driver.find_element(By.XPATH, '//*[@id="custompopup"]/span/h3/span').click()
        except NoSuchElementException:
            print("Awaiting_Delivery_Within_EDD data is not")

    def Shipment_Delivered(self,driver):
        try:
            driver.find_element(By.XPATH, '//*[@id="react-tabs-1"]/div/div/div[2]/div[3]/div[5]/div[3]/div[1]/span').click()
            time.sleep(3)
            # get header Data
            getdata = driver.find_element(By.XPATH, '//*[@id="id"]/thead')
            htmldata = getdata.get_attribute('outerHTML')
            soup = BeautifulSoup(htmldata, 'html.parser')
            headers = soup.find_all('th', class_='fixed-header')
            capital_letters = [header.text.title() for header in headers]
            # get all data
            getrowdata = driver.find_element(By.XPATH, '//*[@id="id"]/tbody')
            rowdataHTML = getrowdata.get_attribute('outerHTML')
            htmlrowData = BeautifulSoup(rowdataHTML, 'html.parser')
            rows = htmlrowData.find('tbody').find_all('tr')
            rowdata = []
            for row in rows:
                data = [cell.text.strip() for cell in row.find_all('td')]
                rowdata.append(data)
            df = pd.DataFrame(rowdata, columns=capital_letters)
            Odf = df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            self.Shipment_Delivered_Sheet.clear()
            self.Shipment_Delivered_Sheet.update(range_name=Update_range, values=data_to_insert)
            driver.find_element(By.XPATH, '//*[@id="custompopup"]/span/h3/span').click()

        except NoSuchElementException:
            print("Shipment_Delivered data is not")

    def PODs_Pending_To_Update(self,driver):
        try:
            driver.find_element(By.XPATH, '//*[@id="react-tabs-1"]/div/div/div[2]/div[3]/div[6]/div[3]/div[1]/span').click()
            time.sleep(3)
            # get header Data
            getdata = driver.find_element(By.XPATH, '//*[@id="id"]/thead')
            htmldata = getdata.get_attribute('outerHTML')
            soup = BeautifulSoup(htmldata, 'html.parser')
            headers = soup.find_all('th', class_='fixed-header')
            capital_letters = [header.text.title() for header in headers]
            # get all data
            getrowdata = driver.find_element(By.XPATH, '//*[@id="id"]/tbody')
            rowdataHTML = getrowdata.get_attribute('outerHTML')
            htmlrowData = BeautifulSoup(rowdataHTML, 'html.parser')
            rows = htmlrowData.find('tbody').find_all('tr')
            rowdata = []
            for row in rows:
                data = [cell.text.strip() for cell in row.find_all('td')]
                rowdata.append(data)
            df = pd.DataFrame(rowdata, columns=capital_letters)
            Odf = df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            self.PODs_Pending_To_Update_Sheet.clear()
            self.PODs_Pending_To_Update_Sheet.update(range_name=Update_range, values=data_to_insert)
            driver.find_element(By.XPATH, '//*[@id="custompopup"]/span/h3/span').click()
        except NoSuchElementException:
            print("PODs_Pending_To_Update data is not")



AAJ_Update()