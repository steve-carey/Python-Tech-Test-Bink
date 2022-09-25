import argparse
import csv
from datetime import datetime
from operator import itemgetter

class Mast(object):

    def __init__(self, *args, **kwargs):
        """
        Set up the initial variables for this mast script
        """
        self.params = self.parse_args()
    
    def parse_args(self):
        """
        Parse arguments supplied by the user into a dictionary

        @returns: A dictionary of values based on required arguments
        """
        parser = argparse.ArgumentParser()
    
        parser.add_argument('-q1', help='Return answer to question 1', action='store_true')
        parser.add_argument('-q2', help='Return answer to question 2', action='store_true')
        parser.add_argument('-q3', help='Return answer to question 3', action='store_true')
        parser.add_argument('-q4', help='Return answer to question 4', action='store_true')
        return parser.parse_args()

    def main(self):
        """
        Main control function for this application. All steps required to successfully complete the
        process are outlined in this function and carried out from here
        """
        mast_data = self.generate_mast_data()

        if self.params.q1:
            # 1a

            mast_data_by_current_rent = self.current_rent_ascending(mast_data)
            
            # 1b
            print("\nOutputting the solution to question 1b...\n")
            [print(mast_item) for mast_item in mast_data_by_current_rent[0:5]]

        if self.params.q2:
            
            masts_lease_of_25 = self.lease_years(mast_data, 25)
            # 2a
            print("\nOutputting the solution to question 2a...\n")
            [print(mast_item) for mast_item in masts_lease_of_25]

            # 2b
            print("\nOutputting the solution to question 2b...\n")
            print(self.float_to_currency(self.total_rent(masts_lease_of_25)))

        if self.params.q3:
            # 3a
            print("\nOutputting the solution to question 3...\n")
            [
                print("{}: has {} masts".format(tenant, count)) 
                # If there is 1 mast then we dont want plural wording
                if count > 1 else print("{}: has {} mast".format(tenant, count))
                for tenant, count in self.tenant_mast_count(mast_data).items()
            ]

        if self.params.q4:
            # 4a
            print("\nOutputting the solution to question 4...\n")
            [
                print(mast_data) 
                for mast_data in self.lease_start_date_range(mast_data)
            ]
        
    def generate_mast_data(self):
        '''
        Opens "Python Developer Test Dataset.csv" file 
        @returns: {'heading': [list of data]} from the file
        '''

        with open("Python Developer Test Dataset.csv", 'r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            data_list = []
            for row in csv_reader:

                data_row = [{headers[i]: value for i, value in enumerate(row)}]
                data_list.append(data_row[0])
        return(data_list)

    def current_rent_ascending(self, mast_data, mast_heading="Current Rent"):
        '''
        @param mast_data: list of dicts, each dict is a row of complete mast data
        @param mast_heading: a string used to identify a key within mast_data
        @returns: a list of dicts, each dict is a row of complete mast data ordered by the
        provided key (heading) [{mast row data}, {mast row data}]
        '''

        return sorted(mast_data, key=lambda i: (float(i[mast_heading])))

    def lease_years(self, mast_data, number_of_years):
        '''    
        creates a list of mast data that has a lease of number_of_years

        @param mast_data: list of dicts, each dict is a row of complete mast data
        @param number_of_years: number of years that mast has been leased
        @returns: list of mast data that has a lease of number_of_years 
        '''

        return [
            mast_row for mast_row in mast_data 
            if int(mast_row["Lease Years"]) == number_of_years
        ]

    def total_rent(self, mast_data):
        '''
        Calculates the total rent.

        @param mast_data: list of dicts, each dict is a row of complete mast data
        @returns: the total rent of masts provided in mast_data float
        '''
        total = sum([float(rent["Current Rent"]) for rent in mast_data])

        return total

    def float_to_currency(self, value, currency_sym="£"):
        '''
        @param currency_sym: the currency symbol
        @param value: float value to be converted to currency
        @returns: currency value as a string with symbol i.e. £1,000.00
        '''
        
        return "{}{:,.2f}".format(currency_sym, round(value, 2))

    def tenant_mast_count(self, mast_data):
        '''
        Creates a dictionary containing tenant name and a count of masts for 
        each tenant

        @param mast_data: list of dicts, each dict is a row of complete mast data
        @returns: a dict containing tenant names and associated number of masts
        '''
        tenants_count_dict = {
            'Arqiva': 0,
            'Vodafone': 0,
            'O2': 0,
            'Everything Everywhere': 0,
            'Cornerstone Telecommunications': 0
        }
        
        tenant_names = [
            mast_line["Tenant Name"].upper().replace(' ', '') 
            for mast_line in mast_data
        ]

        for tenant_name in tenant_names:
            for name in tenants_count_dict.keys():
                if name.replace(' ', '').upper() in tenant_name:
                    tenants_count_dict[name] = tenants_count_dict[name] + 1

        return tenants_count_dict

    def lease_start_date_range(
            self, mast_data, date_key="Lease Start Date", 
            start_date='01/06/1999', end_date='31/08/2007'
        ):
        '''
        @param mast_data: List of dicts, each dict is a row of complete mast data
        @param date_key: The key for which date to search within the mast_data dict
        @param start_date: Start date range for search
        @param end_date: End date range for search
        @returns: a list of dicts, each dict is a row of complete mast data ordered by the
        provided key (heading) [{mast row data}, {mast row data}]
        '''

        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        # sort into YYYY/MM/DD for date comparison
        start_date = start_date.strftime('%Y/%m/%d')

        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        # sort into YYYY/MM/DD for date comparison
        end_date = end_date.strftime('%Y/%m/%d')

        return_mast_data = []
        for mast in mast_data:
            date_string = mast[date_key] # dd mmm yyyy

            date = datetime.strptime(date_string, '%d %b %Y')
            # sort into YYYY/MM/DD for date comparison
            date = datetime.strftime(date, '%Y/%m/%d')


            if start_date < date < end_date:
                # change to DD/MM/YYYY
                date = datetime.strptime(date, '%Y/%m/%d')
                mast[date_key] = date.strftime('%d/%m/%Y')
                return_mast_data.append(mast)
        return return_mast_data


if __name__ == "__main__":
    action = Mast()
    action.main()