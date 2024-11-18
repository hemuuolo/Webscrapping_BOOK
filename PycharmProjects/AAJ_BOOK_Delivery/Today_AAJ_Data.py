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
import json

with open("credentialImportant.json", "r") as json_file:
    json_string= json.load(json_file)
SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/cloud-platform')
google_credentials = service_account.Credentials.from_service_account_info(json_string,scopes=SCOPES)

class Today_AAj:
    def __init__(self):
        self.gc = Gsheet.authorize(google_credentials)
        spreadsheet = self.gc.open_by_key('1CPm7wHqKbhfzXYHdsbxIFy-E2gA8esY2fT7Mcjw1Ntg')
        spreadsheet_Rudhi = self.gc.open_by_key('1H2rHCWhwkFRAIVwbEG7-YZjHnOqskmLv6K5pqrwwkI8')
        self.Today_OrderpoolSheet_Rudhi = spreadsheet_Rudhi.worksheet('Today_Orderpool_Auto (TBD)')
        self.Today_Order_Under_PickingSheet_Rudhi = spreadsheet_Rudhi.worksheet('Today_Order Under Picking_Auto (TBD)')
        self.Today_Under_DispatchSheet_Rudhi = spreadsheet_Rudhi.worksheet('Today_Under Dispatch_Auto (TBD)')
        self.Today_Dispatched_OrderSheet_Rudhi = spreadsheet_Rudhi.worksheet('Todays_Dispatched_Order_Auto (TBD)')
        self.Detail_order_Under_PickingSheet_Rudhi = spreadsheet_Rudhi.worksheet('Details_Order Under Picking_Auto (TBD)')
        self.Details_under_Dispatchsheet_Rudhi = spreadsheet_Rudhi.worksheet('Details_Under Dispatch_Auto (TBD)')
        self.Details_Today_atchsheet_order_Rudhi = spreadsheet_Rudhi.worksheet('Details_Today Dispatched Order_Auto (TBD)')
        self.rudhi_dispatched_order = spreadsheet_Rudhi.worksheet('Dispatched Order_Auto')




        # Get the source and destination worksheets
        self.Today_OrderpoolSheet = spreadsheet.worksheet('Today_Orderpool')
        self.Today_Order_Under_PickingSheet = spreadsheet.worksheet('Today_Order Under Picking')
        self.Today_Under_DispatchSheet = spreadsheet.worksheet('Today_Under Dispatch')
        self.Today_Dispatched_OrderSheet= spreadsheet.worksheet('Today Dispatched Order')
        self.Detail_order_Under_PickingSheet=spreadsheet.worksheet('Details_Order Under Picking')
        self.Details_under_Dispatchsheet=spreadsheet.worksheet('Details_Under Dispatch')
        self.Details_Today_atchsheet_order=spreadsheet.worksheet('Details_Todays_dispatched_Order')
        self.destination_workbook_3 = spreadsheet.worksheet('Dispatched Order')



        self.username = 'kp.singh@uolo.com'
        self.password = 'uolo@123'
        self.url = 'https://wms.aajenterprises.com/login.aspx'
        self.home_url = 'https://wms.aajenterprises.com/Reporthome.aspx'
        self.ConsolidatedInwardReport_url = 'https://wms.aajenterprises.com/ConsolidatedInwardReport.aspx'
        self.Location = 'Kundli - 2'
        self.Publisher = 'Uolo Edtech Pvt Ltd'
        self.Stock_type = 'Fresh Stock'
        self.Dispatched_Order = 'https://wms.aajenterprises.com/DispatchedOrder.aspx'

        #calling function

        self.Today_Orderpoolfun()
        self.Order_Under_Picking()
        self.Under_Dispatch()
        self.Today_Dispatched_Order()
        self.Dispatch_Invetory()
    def Today_Orderpoolfun(self):
        Orderpoolfun_url='https://wms.aajenterprises.com/OrdersInOP.aspx'
        Sheetshow_url='https://wms.aajenterprises.com/OrdersInOP.aspx'
        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtName').send_keys(self.username)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(self.password)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnLogin').click()
        time.sleep(2)
        self.Today_OrderpoolSheet.clear() #clear the data from Sheet
        self.Today_OrderpoolSheet_Rudhi.clear()
        if driver.current_url == self.home_url:
            print("Login successful")

            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_hyperOP').click()
            time.sleep(5)
            if driver.current_url == Orderpoolfun_url:
                print("Entered successfully")
                driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlItem').send_keys(self.Location)
                driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnShow').click()
                time.sleep(3)
                if driver.current_url == Sheetshow_url:
                    print("Data visible")
                    Data = requests.get(driver.current_url)
                    soup = BeautifulSoup(Data.text, 'html.parser')
                    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
                    body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'
                    getdata = driver.find_element(By.XPATH, body_xpath)
                    table_html = getdata.get_attribute('outerHTML')
                    soup = BeautifulSoup(table_html, 'html.parser')
                    data = []
                    for tr in soup.find_all('tr'):
                        row = [item.text for item in tr.find_all('th')]
                        value = [item.text for item in tr.find_all('td')]
                        combine = row + value
                        data.append(combine)

                    if len(data)>1:
                        Overall_df = pd.DataFrame(data[1:], columns=data[0])
                        Odf = Overall_df.fillna('')
                        data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
                        Update_range = "A1"  # update the range

                        self.Today_OrderpoolSheet.update(range_name=Update_range, values=data_to_insert)
                        self.Today_OrderpoolSheet_Rudhi.update(range_name=Update_range, values=data_to_insert)
                        print("Updated Succesfull")

                    else:
                        print("Data is Empty")
                else:
                    print("failed in the website not match")
            else:
                print("failed in the website not match")

        else:
            print("Login failed. Redirected to:", driver.current_url)


    def Order_Under_Picking(self):
        Orderpoolfun_url = 'https://wms.aajenterprises.com/OrdersUnderpick.aspx'
        self.Today_Order_Under_PickingSheet.clear()
        self.Today_Order_Under_PickingSheet_Rudhi.clear()
        self.Detail_order_Under_PickingSheet.clear()
        self.Detail_order_Under_PickingSheet_Rudhi.clear()

        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtName').send_keys(self.username)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(self.password)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnLogin').click()
        time.sleep(2)
        if driver.current_url == self.home_url:
            print("Login successful")

            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_HyperOUP').click()
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[1])

            print("Entered successfully")
            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlItem').send_keys(self.Location)
            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnShow').click()
            time.sleep(3)
            if driver.current_url == Orderpoolfun_url:
                print("Data visible")
                wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
                body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'
                getdata = driver.find_element(By.XPATH, body_xpath)
                table_html = getdata.get_attribute('outerHTML')
                soup = BeautifulSoup(table_html, 'html.parser')

                data = []
                for tr in soup.find_all('tr'):
                    row = [item.text for item in tr.find_all('th')]
                    value = [item.text for item in tr.find_all('td')]
                    combine = row + value
                    data.append(combine)
                if len(data) > 2:
                    Odf = pd.DataFrame(data[1:], columns=data[0])

                    # vv = []
                    # df_details_odf = pd.DataFrame(vv,
                    #                               columns=["Title", "ISBN", "Qty To be Dispatched",
                    #                                        "Supply Qty",
                    #                                        "Price", "Discount", "Amount", "School Name"])
                    # for j in range(len(Odf)):
                    #     k = j + 2
                    #     time.sleep(2)
                    #     schoolName = f'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[{k}]/td[6]'
                    #     SchoolNamedriv = driver.find_element(By.XPATH, schoolName)
                    #     School_html = SchoolNamedriv.get_attribute('outerHTML')
                    #     table_t = BeautifulSoup(School_html, 'html.parser')
                    #     School_nameid = table_t.get_text(strip=True)
                    #     datap = []
                    #     try:
                    #         if k < 10:
                    #             driver.find_element(By.XPATH,
                    #                                 f'//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl0{k}_LinkButton1"]').click()
                    #         else:
                    #             driver.find_element(By.XPATH,
                    #                                 f'//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl{k}_LinkButton1"]').click()
                    #         time.sleep(2)
                    #         body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView2"]/tbody'
                    #         wait.until(EC.presence_of_element_located((By.XPATH, body_xpath)))
                    #         tadata = driver.find_element(By.XPATH, body_xpath)
                    #         table_html = tadata.get_attribute('outerHTML')
                    #         table_t = BeautifulSoup(table_html, 'html.parser')
                    #
                    #         for tr in table_t.find_all('tr')[1:]:
                    #             row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
                    #             datap.append(row_data)
                    #     except Exception as error:
                    #         print(error)
                    #     df_temp = pd.DataFrame(datap,
                    #                            columns=["Title", "ISBN", "Qty To be Dispatched",
                    #                                     "Supply Qty",
                    #                                     "Price", "Discount", "Amount"])
                    #     df_temp['School Name'] = School_nameid
                    #     df_details_odf = pd.concat([df_details_odf, df_temp], ignore_index=True)

                    Odf = Odf.iloc[:, :-1]
                    Odf = Odf.fillna('')
                    data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
                    Update_range = "A1"  # update the range
                    self.Today_Order_Under_PickingSheet.update(range_name=Update_range,
                                                               values=data_to_insert)
                    self.Today_Order_Under_PickingSheet_Rudhi.update(range_name=Update_range,
                                                                     values=data_to_insert)
                    # Update the details tab
                    # df_details_odf = df_details_odf.fillna('')
                    # data_to_insert = [df_details_odf.columns.values.tolist()] + df_details_odf.values.tolist()
                    # Update_range = "A1"  # update the range
                    # self.Detail_order_Under_PickingSheet.update(range_name=Update_range,
                    #                                             values=data_to_insert)
                    # self.Detail_order_Under_PickingSheet_Rudhi.update(range_name=Update_range,
                    #                                                   values=data_to_insert)
                    print("Updated Succesfull")


    def Under_Dispatch(self):
        Orderpoolfun_url = 'https://wms.aajenterprises.com/Readytodispatch.aspx'
        self.Today_Under_DispatchSheet.clear()
        self.Details_under_Dispatchsheet.clear()
        self.Today_Under_DispatchSheet_Rudhi.clear()
        self.Details_under_Dispatchsheet_Rudhi.clear()


        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtName').send_keys(self.username)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(self.password)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnLogin').click()
        time.sleep(2)
        if driver.current_url == self.home_url:
            print("Login successful")

            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_HyperOUD').click()
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[1])
            print("Entered successfully")
            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlItem').send_keys(self.Location)
            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnShow').click()
            time.sleep(3)
            if driver.current_url == Orderpoolfun_url:
                print("Data visible")
                wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
                body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'
                getdata = driver.find_element(By.XPATH, body_xpath)
                table_html = getdata.get_attribute('outerHTML')
                soup = BeautifulSoup(table_html, 'html.parser')

                data = []
                for tr in soup.find_all('tr'):
                    row = [item.text for item in tr.find_all('th')]
                    value = [item.text for item in tr.find_all('td')]
                    combine = row + value
                    data.append(combine)
                if len(data) > 2:
                    Odf = pd.DataFrame(data[1:], columns=data[0])
                    # vv = []
                    # df_details_odf = pd.DataFrame(vv,
                    #                               columns=["Title", "ISBN", "Qty To be Dispatched",
                    #                                        "Supply Qty",
                    #                                        "Price", "Discount", "Amount", "School Name"])
                    # for j in range(len(Odf)):
                    #     k = j + 2
                    #     time.sleep(2)
                    #     schoolName = f'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[{k}]/td[6]'
                    #     SchoolNamedriv = driver.find_element(By.XPATH, schoolName)
                    #     School_html = SchoolNamedriv.get_attribute('outerHTML')
                    #     table_t = BeautifulSoup(School_html, 'html.parser')
                    #     School_nameid = table_t.get_text(strip=True)
                    #     datap = []
                    #     try:
                    #         if k < 10:
                    #             driver.find_element(By.XPATH,
                    #                                 f'//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl0{k}_LinkButton1"]').click()
                    #         else:
                    #             driver.find_element(By.XPATH,
                    #                                 f'//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl{k}_LinkButton1"]').click()
                    #         time.sleep(2)
                    #         body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView2"]/tbody'
                    #         wait.until(EC.presence_of_element_located((By.XPATH, body_xpath)))
                    #         tadata = driver.find_element(By.XPATH, body_xpath)
                    #         table_html = tadata.get_attribute('outerHTML')
                    #         table_t = BeautifulSoup(table_html, 'html.parser')
                    #         for tr in table_t.find_all('tr')[1:]:
                    #             row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
                    #             datap.append(row_data)
                    #     except Exception as error:
                    #         print(error)
                    #
                    #     df_temp = pd.DataFrame(datap,
                    #                            columns=["Title", "ISBN", "Qty To be Dispatched",
                    #                                     "Supply Qty",
                    #                                     "Price", "Discount", "Amount"])
                    #     df_temp['School Name'] = School_nameid
                    #     df_details_odf = pd.concat([df_details_odf, df_temp], ignore_index=True)
                    Odf = Odf.iloc[:, :-1]
                    Odf = Odf.fillna('')
                    data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
                    Update_range = "A1"  # update the range
                    self.Today_Under_DispatchSheet.update(range_name=Update_range,
                                                          values=data_to_insert)
                    self.Today_Under_DispatchSheet_Rudhi.update(range_name=Update_range,
                                                                values=data_to_insert)
                    # # Update the details tab
                    # df_details_odf = df_details_odf.fillna('')
                    # data_to_insert = [df_details_odf.columns.values.tolist()] + df_details_odf.values.tolist()
                    # Update_range = "A1"  # update the range
                    # self.Details_under_Dispatchsheet.update(range_name=Update_range,
                    #                                         values=data_to_insert)
                    # self.Details_under_Dispatchsheet_Rudhi.update(range_name=Update_range,
                    #                                               values=data_to_insert)
                    print("Updated Succesfull")



    def Today_Dispatched_Order(self):
        Orderpoolfun_url = 'https://wms.aajenterprises.com/DispatchedOrdersForHome.aspx'
        self.Details_Today_atchsheet_order.clear()
        self.Today_Dispatched_OrderSheet.clear()
        self.Details_Today_atchsheet_order_Rudhi.clear()
        self.Today_Dispatched_OrderSheet_Rudhi.clear()


        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtName').send_keys(self.username)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(self.password)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnLogin').click()
        time.sleep(2)
        if driver.current_url == self.home_url:
            print("Login successful")

            driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_HyperDO").click()

            time.sleep(5)
            driver.switch_to.window(driver.window_handles[1])
            print("Entered successfully")  # ctl00$ContentPlaceHolder1$ddlItem
            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlItem').send_keys(self.Location)
            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnShow').click()
            time.sleep(3)
            if driver.current_url == Orderpoolfun_url:
                print("Data visible")
                wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
                if 8 == 8:
                    body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody'
                    getdata = driver.find_element(By.XPATH, body_xpath)
                    table_html = getdata.get_attribute('outerHTML')
                    soup = BeautifulSoup(table_html, 'html.parser')

                    data = []
                    for tr in soup.find_all('tr'):
                        row = [item.text for item in tr.find_all('th')]
                        value = [item.text for item in tr.find_all('td')]
                        combine = row + value
                        data.append(combine)
                    if len(data) > 1:
                        Odf = pd.DataFrame(data[1:], columns=data[0])
                        # vv = []
                        # df_details_odf = pd.DataFrame(vv,
                        #                               columns=['Title', 'ISBN', 'Dispatched Quantity', 'Price',
                        #                                        'Discount', 'Amount', 'School Name'])
                        # for j in range(len(Odf)):
                        #     k = j + 2
                        #     time.sleep(2)
                        #     schoolName = f'//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tbody/tr[{k}]/td[6]'
                        #     SchoolNamedriv = driver.find_element(By.XPATH, schoolName)
                        #     School_html = SchoolNamedriv.get_attribute('outerHTML')
                        #     table_t = BeautifulSoup(School_html, 'html.parser')
                        #     School_nameid = table_t.get_text(strip=True)
                        #     datap = []
                        #     try:
                        #         if k < 10:
                        #             driver.find_element(By.XPATH,
                        #                                 f'//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl0{k}_LinkButton1"]').click()
                        #         else:
                        #             driver.find_element(By.XPATH,
                        #                                 f'//*[@id="ctl00_ContentPlaceHolder1_GridView1_ctl{k}_LinkButton1"]').click()
                        #         time.sleep(2)
                        #         body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView2"]/tbody'
                        #         wait.until(EC.presence_of_element_located((By.XPATH, body_xpath)))
                        #         tadata = driver.find_element(By.XPATH, body_xpath)
                        #         table_html = tadata.get_attribute('outerHTML')
                        #         table_t = BeautifulSoup(table_html, 'html.parser')
                        #
                        #         for tr in table_t.find_all('tr')[1:]:
                        #             row_data = [td.get_text(strip=True) for td in tr.find_all('td')]
                        #             datap.append(row_data)
                        #     except Exception as error:
                        #         print(error)
                        #     df_temp = pd.DataFrame(datap,
                        #                            columns=['Title', 'ISBN', 'Dispatched Quantity', 'Price',
                        #                                     'Discount', 'Amount'])
                        #     df_temp['School Name'] = School_nameid
                        #     df_details_odf = pd.concat([df_details_odf, df_temp], ignore_index=True)

                        Odf = Odf.iloc[:, :-1]
                        Odf = Odf.fillna('')
                        data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
                        Update_range = "A1"  # update the range

                        self.Today_Dispatched_OrderSheet.update(range_name=Update_range,
                                                                values=data_to_insert)
                        self.Today_Dispatched_OrderSheet_Rudhi.update(range_name=Update_range,
                                                                      values=data_to_insert)
                        # Update the details tab
                        # df_details_odf = df_details_odf.fillna('')
                        # data_to_insert1 = [df_details_odf.columns.values.tolist()] + df_details_odf.values.tolist()
                        # Update_range = "A1"  # update the range
                        # self.Details_Today_atchsheet_order.update(range_name=Update_range,
                        #                                           values=data_to_insert1)
                        # self.Details_Today_atchsheet_order_Rudhi.update(range_name=Update_range,
                        #                                                 values=data_to_insert1)


                        print("Updated Succesfull")

    def Dispatch_Invetory(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtName').send_keys(self.username)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(self.password)
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnLogin').click()
        time.sleep(2)

        if driver.current_url == self.home_url:
            print("Login successful")

            driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnDispatchOrders').click()
            time.sleep(5)

            if driver.current_url == self.Dispatched_Order:
                print("Entered successfully")

                driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlItem').send_keys(self.Location)
                driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_ddlMatCent').send_keys(self.Publisher)
                driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_BtnShow').click()
                time.sleep(3)

                if driver.current_url == self.Dispatched_Order:
                    print("Data visible")

                    # Extract data from the webpage
                    Data = requests.get(driver.current_url)
                    soup = BeautifulSoup(Data.text, 'html.parser')
                    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
                    body_xpath = '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]'
                    getdata = driver.find_element(By.XPATH, body_xpath)
                    table_html = getdata.get_attribute('outerHTML')
                    soup = BeautifulSoup(table_html, 'html.parser')

                    data = []

                    for tr in soup.find_all('tr'):
                        row = [item.text for item in tr.find_all('th')]
                        value = [item.text for item in tr.find_all('td')]
                        combine = row + value
                        data.append(combine)

                    Detail_df = pd.DataFrame(data[1:], columns=data[0])
                    # Update the data in the destination worksheet
                    Odf = Detail_df.fillna('')
                    data_to_insert = [Odf.columns.values.tolist()] + Odf.values.tolist()
                    Update_range = "A1"  # update the range
                    self.destination_workbook_3.update(range_name=Update_range, values=data_to_insert)
                    self.rudhi_dispatched_order.update(range_name=Update_range, values=data_to_insert)
                    print("Data updated.")
                else:
                    print("Failed1")

            else:
                print("Failed2")
        else:
            print("Login failed. Redirected to:", driver.current_url)

        # Quit the Chrome WebDriver
        driver.quit()


Today_AAj()

