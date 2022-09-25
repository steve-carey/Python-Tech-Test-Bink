import unittest
from pathlib import Path
from python_developer_test import Mast

class TestDeveloperTest(unittest.TestCase):

    def test_csv_file_exists(self):
        '''
        Used to test if the .csv file exists
        '''

        file = "Python Developer Test Dataset.csv"
        if not Path(file).resolve().is_file():
            raise AssertionError("File does not exist: {}".format(file))
    
    def test_float_to_currency(self):
        mast = Mast()
        tests = [
            {
                # test hundreds
                "expected": "£123.00", 
                "input": 123,
                "pass": True,
                "currency": False
            },
            {
                 # test thousands and higher rounding boundary
                "expected": "£1,234.01",
                "input": 1234.005,
                "pass": True,
                "currency": False
            },
            {   
                 # test millions and lower rounding boundary
                "expected": "£1,234,567.00",
                "input": 1234567.004,
                "pass": True,
                "currency": False
            },
            {
                # Custom currency symbol
                "expected": "$123.00",
                "input": 123, 
                "pass": True,
                "currency": "$" 
            },
            {
                # Custom currency symbol
                "expected": "Le123.00",
                "input": 123, 
                "pass": True,
                "currency": "Le" 
            },
        ]

        for test in tests:
            
            if test["pass"]:
                # setting result for testing currency kwarg
                if test["currency"]:
                    result = mast.float_to_currency(
                        test["input"],
                        currency_sym=test["currency"]
                    )
                # without currency kwarg in tests
                else:
                    result = mast.float_to_currency(test["input"])
                self.assertEqual(result, test["expected"])

            else:
                self.assertRaises(ValueError, mast.float_to_currency, test["input"])

    def test_current_rent_ascending(self):
        mast = Mast()
        tests = [
            {
                "mast_data": [
                    # reorder based on values
                    {"Current Rent": 3}, 
                    {"Current Rent": 2},
                    {"Current Rent": 1}
                ],
                "expected": [
                    {"Current Rent": 1},
                    {"Current Rent": 2},
                    {"Current Rent": 3}
                ],
                "kwarg": False
            },
            {
                "mast_data": [
                    # reordering for duplicate values
                    {"Current Rent": 4},
                    {"Current Rent": 2},
                    {"Current Rent": 2},
                    {"Current Rent": 1}
                ],
                "expected": [
                    {"Current Rent": 1},
                    {"Current Rent": 2},
                    {"Current Rent": 2},
                    {"Current Rent": 4}
                ],
                "kwarg": False
            },
            {
                "mast_data": [
                    # test for kwarg key
                    {"kwarg": 3}, 
                    {"kwarg": 2},
                    {"kwarg": 1}
                ],
                "expected": [
                    {"kwarg": 1},
                    {"kwarg": 2},
                    {"kwarg": 3}
                ],
                "kwarg": "kwarg"
            },
        ]

        for test in tests:
            
            if test["kwarg"]:
                # set result for kwargs to alter mast_heading key
                result = mast.current_rent_ascending(
                    test["mast_data"],
                    mast_heading=test["kwarg"]
                )
            else:
                # result if we are not using kwargs
                result = mast.current_rent_ascending(test["mast_data"])
            self.assertEqual(result, test["expected"])
        
    def test_lease_years(self):
        mast = Mast()
        tests = [
            {
                "mast_data": [
                    # 2 values of 25 years
                    {"Lease Years": 25}, 
                    {"Lease Years": 25},
                    {"Lease Years": 1}
                ],
                "years": 25,
                "expected": [
                    {"Lease Years": 25}, 
                    {"Lease Years": 25}
                ],
            },
            {
                "mast_data": [
                    # 1 value of 1 years
                    {"Lease Years": 25}, 
                    {"Lease Years": 25},
                    {"Lease Years": 1}
                ],
                "years": 1,
                "expected": [
                    {"Lease Years": 1}
                ],
            },
            {
                "mast_data": [
                    # no values of 10 years
                    {"Lease Years": 25}, 
                    {"Lease Years": 25},
                    {"Lease Years": 1}
                ],
                "years": 10,
                "expected": [],
            },
        ]

        for test in tests:
            result = mast.lease_years(test["mast_data"], test["years"])
            self.assertEqual(result, test["expected"])
    
    def test_lease_years(self):
        '''
        Note: currency rounding is handled by float_to_currency(),
        therefore it is not necessary to test rounding boundaries.
        Rounding boundaries for currencies are tested in test_float_to_currency()
        '''
        mast = Mast()
        tests = [
            {
                "mast_data": [
                    # sum of decimals
                    {"Current Rent": 100000}, 
                    {"Current Rent": 2000},
                    {"Current Rent": 30}
                ],
                "expected": 102030
            },
            {
                "mast_data": [
                    # sum of decimals
                    {"Current Rent": 10}, 
                    {"Current Rent": 10.01},
                    {"Current Rent": 0.3}
                ],
                "expected": 20.31
            },
            {
                "mast_data": [
                    # sum of zeros
                    {"Current Rent": 0}, 
                    {"Current Rent": 0},
                    {"Current Rent": 0}
                ],
                "expected": 0
            },
            {   
                # empty dataset of "Current Rent"
                "mast_data": [],
                "expected": 0
            },
        ]

        for test in tests:
            result = mast.total_rent(test["mast_data"])
            self.assertEqual(result, test["expected"])
    
    def test_tenant_mast_count(self):
        mast = Mast()
        tests = [
            {
                "mast_data": [
                    # Count a single tenant
                    {"Tenant Name": 'Arqiva'}, 
                    {"Tenant Name": 'ARQIVA LTD'},
                    {"Tenant Name": 'Arqiva Communications'}
                ],
                "expected": {
                    'Arqiva': 3,
                    'Vodafone': 0,
                    'O2': 0,
                    'Everything Everywhere': 0,
                    'Cornerstone Telecommunications': 0
                }
            },
            {
                "mast_data": [
                    # Count multiple tenants
                    {"Tenant Name": 'Arqiva'}, 
                    {"Tenant Name": 'Vodafone LTD'},
                    {"Tenant Name": 'Vodafone Communications'},
                    {"Tenant Name": 'O2'},
                    {"Tenant Name": 'O2 (UK) ltd.'},
                ],
                "expected": {
                    'Arqiva': 1,
                    'Vodafone': 2,
                    'O2': 2,
                    'Everything Everywhere': 0,
                    'Cornerstone Telecommunications': 0
                }
            },
            {   
                # empty dataset
                "mast_data": [],
                "expected": {
                    'Arqiva': 0,
                    'Vodafone': 0,
                    'O2': 0,
                    'Everything Everywhere': 0,
                    'Cornerstone Telecommunications': 0
                }
            },
        ]

        for test in tests:
            result = mast.tenant_mast_count(test["mast_data"])
            self.assertEqual(result, test["expected"])
    
    def test_lease_start_date_range(self):
        mast = Mast()
        tests = tests = [
            {
                "mast_data": [
                    # Test withing default range of '01/06/1999' to '31/08/2007'
                    {"Lease Start Date": '31 Jan 1994'}, 
                    {"Lease Start Date": '31 Jan 2001'},
                    {"Lease Start Date": '31 Jan 2008'}
                ],
                "expected": [
                    {"Lease Start Date": '31/01/2001'},
                ],
                "kwargs": False
            },
            {
                "mast_data": [
                    # Test withing default range of '01/06/1999' to '31/08/2007'
                    # using date_key kwarg of "Lease End Date"
                    {"Lease End Date": '31 Jan 1994'}, 
                    {"Lease End Date": '31 Jan 2001'},
                    {"Lease End Date": '31 Jan 2008'}
                ],
                "expected": [
                    {"Lease End Date": '31/01/2001'},
                ],
                "kwargs": {
                    "date_key": "Lease End Date",
                    "start": False,
                    "end": False,
                }
            },
            {
                "mast_data": [
                    # Test withing kwargs range of '31/01/1993' to '31/01/2009'
                    {"Lease End Date": '31 Jan 1994'}, 
                    {"Lease End Date": '31 Jan 2001'},
                    {"Lease End Date": '31 Jan 2008'}
                ],
                "expected": [
                    {"Lease End Date": '31/01/1994'}, 
                    {"Lease End Date": '31/01/2001'},
                    {"Lease End Date": '31/01/2008'}
                ],
                "kwargs": {
                    "date_key": "Lease End Date",
                    "start": "31/01/1993",
                    "end": "31/01/2009",
                }
            },
        ]
        for test in tests:
            # set result if we are using kwargs
            if test["kwargs"]:
                # set result if we are also using start/end data kwargs
                if test["kwargs"]["start"]:
                    result = mast.lease_start_date_range(
                        test["mast_data"], 
                        date_key=test["kwargs"]["date_key"],
                        start_date=test["kwargs"]["start"], 
                        end_date=test["kwargs"]["end"]
                    )
                # set result if we are not using start/end data kwargs
                else:
                    result = mast.lease_start_date_range(
                        test["mast_data"], 
                        date_key=test["kwargs"]["date_key"]
                    )
            else:
                # result without kwargs
                result = mast.lease_start_date_range(test["mast_data"])
            self.assertEqual(result, test["expected"])

if __name__ == "__main__":
    unittest.main()
