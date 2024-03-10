from datetime import datetime

import pandas as pd
import requests


class Authority:
    def __init__(self):
        '''
            - constructor for the class
            - initialized an empty list
        '''
        self.entries = []

    def suspended_licenses(self, response):
        '''
        - method for determining the list of suspended licenses by the authority
        :param response: contains 150 data points from the API
        :return: an excel which contains the list of all suspended licenses
        '''
        for entry in response:
            if entry["suspendat"] == True:
                self.entries.append(entry)

        df = pd.DataFrame(self.entries)
        df.to_excel('suspendedLicenses.xlsx')

    def valid_licenses(self, response):
        '''
        - method for extracting the valid licenses issued until today's date
        :param response: contains 150 data points from the API
        :return: an excel file which contains the list of all valid licenses issued until today's date
        '''
        valid_licenses = []
        # get the current date
        currentDate = datetime.today()
        for entry in response:
            dateE = datetime.strptime(entry["dataDeExpirare"], "%d/%m/%Y")
            if dateE >= currentDate:
                valid_licenses.append(entry)

        df = pd.DataFrame(valid_licenses)
        df.to_excel('validLicenses.xlsx')

    def category_count(self, response):
        '''
        - method for finding licenses based on category and their count
        :param response: contains 150 data points from the API
        :return: an excel file which contains all licenses based on category and their count
        '''
        category_count = {}
        for entry in response:
            category = entry["categorie"]
            category_count[category] = category_count.get(category, 0) + 1

        df = pd.DataFrame(list(category_count.items()), columns=['Category', 'Count'])
        df.to_excel('categories.xlsx')


if __name__ == "__main__":
    api_url = "http://localhost:30000/drivers-licenses/list?length=150"
    # response will contain 150 data points from the API
    response = requests.get(api_url)
    authority = Authority()

    while (True):
        option = input(
            "0. Exit\n1. List suspended licenses\n2. List valid licenses\n3. Licenses based on their count\n Enter "
            "option: ")

        if option == '1':
            authority.suspended_licenses(response.json())
            print("Suspended list of liceses can be found at 'suspendedLicenses.xlsx'")
        elif option == '2':
            authority.valid_licenses(response.json())
            print("Valid liceses can be found at 'validLicenses.xlsx'")
        elif option == '3':
            authority.category_count(response.json())
            print("Licenses based on their count can be found in 'categories.xlsx'")
        elif option == '0':
            break
        else:
            print("Invalid option. Please select from the options list.")
