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
class AAJ_Update:
    def __init__(self):
        self.gc = Gsheet.authorize(google_credentials)
        spreadsheet_Main = self.gc.open_by_key('1w6RoC5Bn39bKtdRqaBRtPTZKThmmxxlSeRV0kw1Qm6U')
        self.main_sheet=spreadsheet_Main.worksheet('Refer_value_aajData')
        
        datag=self.main_sheet.get_all_values()
        self.main_df=pd.DataFrame(data=datag[1:], columns=datag[0])
        
        
        spreadsheet = self.gc.open_by_key(self.main_df.loc[0,'Value'])
        spreadsheet_Rudhi = self.gc.open_by_key(self.main_df.loc[1,'Value'])
        Spreadsheet_Hemant=self.gc.open_by_key(self.main_df.loc[2,'Value'])
        
        self.source_workbook = spreadsheet.worksheet('Automated Data') #testing purpose
        self.destination_workbook_1 = spreadsheet.worksheet(self.main_df.loc[3,'Value'])
        self.destination_workbook_2 = spreadsheet.worksheet(self.main_df.loc[4,'Value'])
        self.destination_workbook_3 = spreadsheet.worksheet(self.main_df.loc[5,'Value'])
        #hHemant tab
        self.hemant_overall_inventory = Spreadsheet_Hemant.worksheet(self.main_df.loc[6,'Value'])
        self.hemant_detailed_inventory = Spreadsheet_Hemant.worksheet(self.main_df.loc[7,'Value'])
        self.hemant_dispatched_order = Spreadsheet_Hemant.worksheet(self.main_df.loc[8,'Value'])
        # Get the source and destination worksheets
        self.rudhi_overall_inventory=spreadsheet_Rudhi.worksheet(self.main_df.loc[9,'Value'])
        self.rudhi_detailed_inventory=spreadsheet_Rudhi.worksheet(self.main_df.loc[10,'Value'])
        self.rudhi_dispatched_order=spreadsheet_Rudhi.worksheet(self.main_df.loc[11,'Value'])

       


        # Select the specific worksheet within the Google Sheet
        self.worksheet_1 = spreadsheet.get_worksheet(0)  # Use the index of your worksheet (0 for the first sheet) #testing
        self.worksheet_2 = spreadsheet.get_worksheet(0)  # Use the index of your worksheet (0 for the first sheet) #testing

        # Web scraping configuration
        self.username = self.main_df.loc[13,'Value']
        self.password = self.main_df.loc[14,'Value']
        self.url = self.main_df.loc[15,'Value']
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        time.sleep(3)
        self.driver.find_element(By.ID,  self.main_df.loc[16,'Value']).send_keys(self.username)
        self.driver.find_element(By.ID,  self.main_df.loc[17,'Value']).send_keys(self.password)
        self.driver.find_element(By.ID, self.main_df.loc[18,'Value']).click()
        time.sleep(40)
        opt_var=self.main_sheet.cell(row=2,col=4)
        opt_var=opt_var.value
        print(opt_var)
        opt_var=opt_var.strip()
        iter_val=30
        for j in range(len(opt_var)):
            time.sleep(1)
            self.driver.find_element(By.ID,self.main_df.loc[iter_val,'Value']).send_keys(int(opt_var[j]))
            iter_val += 1
        self.driver.find_element(By.ID,self.main_df.loc[36,'Value']).click()#ctl00_ContentPlaceHolder1_SubmitButton
        time.sleep(8)
        self.driver.find_element(By.XPATH, self.main_df.loc[19,'Value']).click()
        self.Overall_Inventory()
        self.Detailed_inventory()
        self.Dispatch_Invetory()







# Get the source and destination worksheets

    def Overall_Inventory(self):
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH,self.main_df.loc[20,'Value'] ).click()
            time.sleep(2)
            self.driver.find_element(By.ID,self.main_df.loc[21,'Value']).send_keys(self.main_df.loc[12,'Value'])
            time.sleep(2)
            self.driver.find_element(By.ID, self.main_df.loc[22,'Value']).click()
            Data = requests.get(self.driver.current_url)
            soup = BeautifulSoup(Data.text, 'html.parser')
            wait = WebDriverWait(self.driver, 20)  # Adjust the timeout as needed
            body_xpath = self.main_df.loc[23,'Value']
            getdata = self.driver.find_element(By.XPATH, body_xpath)
            table_html = getdata.get_attribute('outerHTML')
            soup = BeautifulSoup(table_html, 'html.parser')
            data = []
            for tr in soup.find_all('tr'):
                row = [item.text for item in tr.find_all('th')]
                value = [item.text for item in tr.find_all('td')]
                combine = row + value
                data.append(combine)
            Overall_df = pd.DataFrame(data=data[1:], columns=data[0])
            Overall_df[self.main_df.loc[24,'Value']] = Overall_df[self.main_df.loc[24,'Value']].astype(int)
            Overall_df[self.main_df.loc[25,'Value']] = Overall_df[self.main_df.loc[25,'Value']].astype(int)
            Overall_df[self.main_df.loc[26,'Value']] = Overall_df[self.main_df.loc[26,'Value']].astype(int)
            Overall_df[self.main_df.loc[27,'Value']] = Overall_df[self.main_df.loc[27,'Value']].astype(int)
            Odf = Overall_df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = self.main_df.loc[28,'Value'] # update the range
            self.destination_workbook_1.batch_clear([self.main_df.loc[29,'Value']])
            self.rudhi_overall_inventory.batch_clear([self.main_df.loc[29,'Value']])
            self.destination_workbook_1.update(range_name=Update_range, values=data_to_insert)
            self.rudhi_overall_inventory.update(range_name=Update_range, values=data_to_insert)
            #self.hemant_overall_inventory.update(range_name=Update_range, values=data_to_insert)
            print("OverallIventory Updated")

        except NoSuchElementException:
            print("Transportation_Allocation data is not")
        self.driver.find_element(By.XPATH,self.main_df.loc[19,'Value']).click()

    def Detailed_inventory(self):
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, self.main_df.loc[37,'Value']).click()
            time.sleep(2)
            coo_no=int(self.main_df.loc[44,'Value'])
            columns=[]
            for mmi in range(coo_no):
                c_it=45+mmi
                columns.append(self.main_df.loc[c_it,'Value'])
            Detail_df = pd.DataFrame(columns=columns)
            id_lis = [ self.main_df.loc[38,'Value'],  self.main_df.loc[39,'Value']]
            for idl in range(len(id_lis)):
                try:
                    self.driver.find_element(By.XPATH,self.main_df.loc[19,'Value']).click()
                    time.sleep(2)
                    self.driver.find_element(By.ID,self.main_df.loc[40,'Value']).send_keys(id_lis[idl])
                    time.sleep(3)
                    # ----------------------------------______________________-_-----------------------
                    self.driver.find_element(By.ID, self.main_df.loc[41,'Value']).send_keys(self.main_df.loc[12,'Value'])
                    time.sleep(2)
                    self.driver.find_element(By.ID, self.main_df.loc[42,'Value']).click()
                    time.sleep(2)
                    timeout = 40  # seconds
                    element_present = EC.presence_of_element_located(
                        (By.XPATH, self.main_df.loc[43,'Value']))
                    WebDriverWait(self.driver, timeout).until(element_present)

                    Data = requests.get(self.driver.current_url)
                    soup = BeautifulSoup(Data.text, 'html.parser')
                    wait = WebDriverWait(self.driver, 20)  # Adjust the timeout as needed
                    body_xpath = self.main_df.loc[43,'Value']
                    getdata = self.driver.find_element(By.XPATH, body_xpath)
                    table_html = getdata.get_attribute('outerHTML')
                    soup = BeautifulSoup(table_html, 'html.parser')
                    data = []
                    for tr in soup.find_all('tr'):
                        row = [item.text for item in tr.find_all('th')]
                        value = [item.text for item in tr.find_all('td')]
                        combine = row + value
                        data.append(combine)
                    temp_df = pd.DataFrame(data[1:], columns=data[0])

                    # Perform the merge (here we'll concatenate them as an example)
                    Detail_df = pd.concat([Detail_df,temp_df])
                except Exception as e:
                    print(e)
            #"-------------------------------------------------------_________________________________-----------------------------------"
            Detail_df[self.main_df.loc[50,'Value']] = Detail_df[self.main_df.loc[50,'Value']].astype(int)
            Detail_df[self.main_df.loc[53,'Value']] = Detail_df[self.main_df.loc[53,'Value']].astype(int)
            Detail_df[self.main_df.loc[54,'Value']] = Detail_df[self.main_df.loc[54,'Value']].astype(int)
            Detail_df[self.main_df.loc[55,'Value']] = Detail_df[self.main_df.loc[55,'Value']].astype(int)
            Detail_df[self.main_df.loc[56,'Value']] = Detail_df[self.main_df.loc[56,'Value']].astype(int)
            Detail_df[self.main_df.loc[59,'Value']] = Detail_df[self.main_df.loc[59,'Value']].astype(int)
            Detail_df[self.main_df.loc[66,'Value']] = Detail_df[self.main_df.loc[66,'Value']].astype(int)
            Detail_df[self.main_df.loc[67,'Value']] = Detail_df[self.main_df.loc[67,'Value']].astype(int)
            Detail_df[self.main_df.loc[68,'Value']] = Detail_df[self.main_df.loc[68,'Value']].astype(int)
            Detail_df[self.main_df.loc[69,'Value']] = Detail_df[self.main_df.loc[69,'Value']].astype(int)
            Detail_df[self.main_df.loc[70,'Value']] = Detail_df[self.main_df.loc[70,'Value']].astype(int)
            Detail_df[self.main_df.loc[71,'Value']] = Detail_df[self.main_df.loc[71,'Value']].astype(int)
            Detail_df[self.main_df.loc[73,'Value']] = Detail_df[self.main_df.loc[73,'Value']].astype(int)
            Detail_df[self.main_df.loc[75,'Value']] = Detail_df[self.main_df.loc[74,'Value']].astype(int)
            Odf = Detail_df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = self.main_df.loc[76,'Value'] # update the range
            
            self.destination_workbook_2.batch_clear([self.main_df.loc[77,'Value']])
            self.rudhi_detailed_inventory.batch_clear([self.main_df.loc[77,'Value']])
            self.destination_workbook_2.update(range_name=Update_range, values=data_to_insert)
            self.rudhi_detailed_inventory.update(range_name=Update_range, values=data_to_insert)
            #self.hemant_detailed_inventory.update(range_name=Update_range, values=data_to_insert)
            print("Detailed Inventory Updated")
        except NoSuchElementException:
            print("Transportation_Allocation data is not")
        self.driver.find_element(By.XPATH, self.main_df.loc[19,'Value']).click()




    def Dispatch_Invetory(self):
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_BtnDispatchOrders"]/div[2]/p').click()
            time.sleep(2)
            
            coo_no=int(self.main_df.loc[80,'Value'])
            columns=[]
            for mmi_t in range(coo_no):
                c_it=81+mmi_t
                columns.append(self.main_df.loc[c_it,'Value'])
            Detail_df = pd.DataFrame(columns=columns)
           
            id_lis = [self.main_df.loc[113,'Value'], self.main_df.loc[114,'Value']]
            for idl in range(len(id_lis)):
                try:
                    self.driver.find_element(By.XPATH, self.main_df.loc[19,'Value']).click()
                    time.sleep(2)
                    self.driver.find_element(By.ID, self.main_df.loc[115,'Value']).send_keys(id_lis[idl])
                    time.sleep(3)
                    self.driver.find_element(By.ID, self.main_df.loc[116,'Value']).send_keys('Kundli-2')
                    time.sleep(2)
                    self.driver.find_element(By.ID, self.main_df.loc[117,'Value']).click()
                    time.sleep(2)
                    timeout = 40  # seconds
                    element_present = EC.presence_of_element_located((By.XPATH, self.main_df.loc[118,'Value']))
                    WebDriverWait(self.driver, timeout).until(element_present)

                    Data = requests.get(self.driver.current_url)
                    soup = BeautifulSoup(Data.text, 'html.parser')
                    wait = WebDriverWait(self.driver, 20)  # Adjust the timeout as needed
                    body_xpath = self.main_df.loc[118,'Value']
                    getdata = self.driver.find_element(By.XPATH, body_xpath)
                    table_html = getdata.get_attribute('outerHTML')
                    soup = BeautifulSoup(table_html, 'html.parser')
                    data = []
                    for tr in soup.find_all('tr'):
                        row = [item.text for item in tr.find_all('th')]
                        value = [item.text for item in tr.find_all('td')]
                        combine = row + value
                        data.append(combine)

                    temp_df = pd.DataFrame(data[1:], columns=data[0])
                    Detail_df = pd.concat([Detail_df,temp_df])
                except Exception as e:
                    print(e)


            # Update the data in the destination worksheet
            Odf = Detail_df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = self.main_df.loc[119,'Value']# update the range
            self.destination_workbook_3.batch_clear([self.main_df.loc[120,'Value']])
            self.rudhi_dispatched_order.batch_clear([self.main_df.loc[120,'Value']])
            self.destination_workbook_3.update(range_name=Update_range, values=data_to_insert)
            self.rudhi_dispatched_order.update(range_name=Update_range, values=data_to_insert)
            
            #self.hemant_dispatched_order.update(range_name=Update_range, values=data_to_insert)
            
            print("Data updated dispactch order.")
        except NoSuchElementException:
            print("Transportation_Allocation data is not")
        self.driver.find_element(By.XPATH, self.main_df.loc[19,'Value']).click()


AAJ_Update()