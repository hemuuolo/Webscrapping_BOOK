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
        spreadsheet = self.gc.open_by_key('1CPm7wHqKbhfzXYHdsbxIFy-E2gA8esY2fT7Mcjw1Ntg')
        spreadsheet_Rudhi = self.gc.open_by_key('1H2rHCWhwkFRAIVwbEG7-YZjHnOqskmLv6K5pqrwwkI8')
        Spreadsheet_Hemant=self.gc.open_by_key('1HSbjCCTZVq4hkC6DH9738EecxcI32ISsDYw6NHKACoY')
        
        self.source_workbook = spreadsheet.worksheet('Automated Data') #testing purpose
        self.destination_workbook_1 = spreadsheet.worksheet('Overall Inventory')
        self.destination_workbook_2 = spreadsheet.worksheet('Detailed Inventory')
        self.destination_workbook_3 = spreadsheet.worksheet('Dispatched Order')
        #hHemant tab
        self.hemant_overall_inventory = Spreadsheet_Hemant.worksheet('Overall_Invetory')
        self.hemant_detailed_inventory = Spreadsheet_Hemant.worksheet('Detail_Inventory')
        self.hemant_dispatched_order = Spreadsheet_Hemant.worksheet('Dispatch_invetory')
        # Get the source and destination worksheets
        self.rudhi_overall_inventory=spreadsheet_Rudhi.worksheet('Inventory_Overall_Auto')
        self.rudhi_detailed_inventory=spreadsheet_Rudhi.worksheet('Inventory_Day_Level_Auto')
        self.rudhi_dispatched_order=spreadsheet_Rudhi.worksheet('Dispatched Order_Auto')

       


        # Select the specific worksheet within the Google Sheet
        self.worksheet_1 = spreadsheet.get_worksheet(0)  # Use the index of your worksheet (0 for the first sheet) #testing
        self.worksheet_2 = spreadsheet.get_worksheet(0)  # Use the index of your worksheet (0 for the first sheet) #testing

        # Web scraping configuration
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
        self.driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()
        self.Overall_Inventory()
        self.Detailed_inventory()
        self.Dispatch_Invetory()






    
        
# Get the source and destination worksheets

    def Overall_Inventory(self):
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_BtnStockStatus"]/div[2]/p').click()
            time.sleep(2)
            self.driver.find_element(By.ID,'ctl00_ContentPlaceHolder1_ddlItem').send_keys('Kundli-2')
            time.sleep(2)
            self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnShow').click()
            Data = requests.get(self.driver.current_url)
            soup = BeautifulSoup(Data.text, 'html.parser')
            wait = WebDriverWait(self.driver, 20)  # Adjust the timeout as needed
            body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'
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
            Overall_df['System Qty'] = Overall_df['System Qty'].astype(int)
            Overall_df['Under Picking'] = Overall_df['Under Picking'].astype(int)
            Overall_df['Reserve in Order Pool'] = Overall_df['Reserve in Order Pool'].astype(int)
            Overall_df['Available for Picking'] = Overall_df['Available for Picking'].astype(int)
            Odf = Overall_df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            self.destination_workbook_1.batch_clear(['A:K'])
            self.rudhi_overall_inventory.batch_clear(['A:K'])
            self.destination_workbook_1.update(range_name=Update_range, values=data_to_insert)
            self.rudhi_overall_inventory.update(range_name=Update_range, values=data_to_insert)
            #self.hemant_overall_inventory.update(range_name=Update_range, values=data_to_insert)
            print("OverallIventory Updated")

        except NoSuchElementException:
            print("Transportation_Allocation data is not")
        self.driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()

    def Detailed_inventory(self):
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_BtnConsInw"]/div[2]/p').click()
            time.sleep(2)

            Detail_df = pd.DataFrame(columns=['S.No','Date && Time','Finalize Date','Gate Entry Date','LOCAL','Gin No','Printer','Shipping No','Total Titles','Total Qty','Total OK Qty','Total Damage Qty','Reference No','PO No','Balance PO Qty','ISBN','Title','Description','Subject','Author','Price','AGRN Qty','GRN Qty','Short/Excess Qty','Actual Qty','OK Qty','Damage Qty','Location','Qty','VchCode','Shipment ID'])

            id_lis = ['2024-2025', '2024-2025_II']
            for idl in range(len(id_lis)):
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()
                    time.sleep(2)
                    self.driver.find_element(By.ID, "ctl00_dpfin").send_keys(id_lis[idl])
                    time.sleep(3)
                    # ----------------------------------______________________-_-----------------------
                    self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlItem').send_keys('Kundli-2')
                    time.sleep(2)
                    self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnShw').click()
                    time.sleep(2)
                    timeout = 40  # seconds
                    element_present = EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'))
                    WebDriverWait(self.driver, timeout).until(element_present)

                    Data = requests.get(self.driver.current_url)
                    soup = BeautifulSoup(Data.text, 'html.parser')
                    wait = WebDriverWait(self.driver, 20)  # Adjust the timeout as needed
                    body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'
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
            Detail_df['Gin No'] = Detail_df['Gin No'].astype(int)
            Detail_df['Total Titles'] = Detail_df['Total Titles'].astype(int)
            Detail_df['Total Qty'] = Detail_df['Total Qty'].astype(int)
            Detail_df['Total OK Qty'] = Detail_df['Total OK Qty'].astype(int)
            Detail_df['Total Damage Qty'] = Detail_df['Total Damage Qty'].astype(int)
            Detail_df['Balance PO Qty'] = Detail_df['Balance PO Qty'].astype(int)
            Detail_df['AGRN Qty'] = Detail_df['AGRN Qty'].astype(int)
            Detail_df['GRN Qty'] = Detail_df['GRN Qty'].astype(int)
            Detail_df['Short/Excess Qty'] = Detail_df['Short/Excess Qty'].astype(int)
            Detail_df['Actual Qty'] = Detail_df['Actual Qty'].astype(int)
            Detail_df['OK Qty'] = Detail_df['OK Qty'].astype(int)
            Detail_df['Damage Qty'] = Detail_df['Damage Qty'].astype(int)
            Detail_df['Qty'] = Detail_df['Qty'].astype(int)
            Detail_df['VchCode'] = Detail_df['VchCode'].astype(int)
            Odf = Detail_df.fillna('')
            data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
            Update_range = "A1"  # update the range
            
            self.destination_workbook_2.batch_clear(['A:AE'])
            self.rudhi_detailed_inventory.batch_clear(['A:AE'])
            self.destination_workbook_2.update(range_name=Update_range, values=data_to_insert)
            self.rudhi_detailed_inventory.update(range_name=Update_range, values=data_to_insert)
            #self.hemant_detailed_inventory.update(range_name=Update_range, values=data_to_insert)
            print("Detailed Inventory Updated")
        except NoSuchElementException:
            print("Transportation_Allocation data is not")
        self.driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()




    def Dispatch_Invetory(self):
        try:
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_BtnDispatchOrders"]/div[2]/p').click()
            time.sleep(2)

            Detail_df = pd.DataFrame(columns=['SrNo','Dispatch Date','OrderDate','Pick Confirmation DateTime','OrderNo','Reference No','Customer','Narration','Order Qty','Dispatched Qty','TotalCartons','TotWeight','City','Pincode','Transport','Transport Mode','Invoice No','Invoice Amount','GrNo','GrDate','EDD','ADD','Freight','Basis','Gr Sent Date','Docket No','GR Thru Transport','Remarks','Act No Of Cartons','DRS No.','ShipTo Address','OrderDetails'])

            id_lis = ['2024-2025', '2024-2025_II']
            for idl in range(len(id_lis)):
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()
                    time.sleep(2)
                    self.driver.find_element(By.ID, "ctl00_dpfin").send_keys(id_lis[idl])
                    time.sleep(3)
                    self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlItem').send_keys('Kundli-2')
                    time.sleep(2)
                    self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnShow').click()
                    time.sleep(2)
                    timeout = 40  # seconds
                    element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'))
                    WebDriverWait(self.driver, timeout).until(element_present)

                    Data = requests.get(self.driver.current_url)
                    soup = BeautifulSoup(Data.text, 'html.parser')
                    wait = WebDriverWait(self.driver, 20)  # Adjust the timeout as needed
                    body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'
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
            Update_range = "A1"  # update the range
            self.destination_workbook_3.batch_clear(['A:AG'])
            self.rudhi_dispatched_order.batch_clear(['A:AG'])
            self.destination_workbook_3.update(range_name=Update_range, values=data_to_insert)
            self.rudhi_dispatched_order.update(range_name=Update_range, values=data_to_insert)
            
            #self.hemant_dispatched_order.update(range_name=Update_range, values=data_to_insert)
            
            print("Data updated dispactch order.")
        except NoSuchElementException:
            print("Transportation_Allocation data is not")
        self.driver.find_element(By.XPATH, '//*[@id="aspnetForm"]/nav/div[1]/div[1]/img').click()


AAJ_Update()