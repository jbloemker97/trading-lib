'''
    Class that gets 15 min delayed financial data from IEX Cloud.
    URL: https://iexcloud.io/docs/api/
'''

import requests

class IEXCloud: 
    __base_url = None
    __default_fields = ['open', 'high', 'low', 'close', 'volume']
    
    def __init__(self, pk_key=None, sk_key=None, test=True):
        self.__pk_key = pk_key
        self.__sk_key = sk_key
        self.test(test)

    def quote(self, ticker, prev_day = True, fields = None):
        if fields is None:
            fields = self.__default_fields

        if prev_day:
            prev_day = 'previous'
        else:
            prev_day = 'quote'

        url = f"{self.__base_url}/stock/{ticker}/{prev_day}/?filter="

        # Append fields in request
        for field in fields:
            url += f"{field},"

        # Remove final , and append our token
        url = url[:-1]
        url += f"&token={self.__sk_key}"

        try: 
            response = requests.get(url)

            if response.status_code is not 200:
                raise Exception(f"Error: Response status code: {response.status_code}")

            return response.json()
        except Exception as error:
            pass

    def hist_data(self, ticker, range, fields = None):
        '''
            Docs: https://iexcloud.io/docs/api/#historical-prices

            Returns *adjusted* historical data for up to 15 years.

            @ ticker [String] - Non case sensative stock ticker
            @ range [String] - Date range from iex cloud. Options: 1m, 3, 6m, ytd, 1y, 2y, 5y, max   
            @ fields [List] - List of fields to query the request with       
        '''

        if fields is None:
            fields = self.__default_fields

        url = f"{self.__base_url}/stock/{ticker}/chart/{range}/?filter="

        # Append fields in request
        for field in fields:
            url += f"{field},"
        
        # Remove final , and append our token
        url = url[:-1]
        url += f"&token={self.__sk_key}"

        try:
            response = requests.get(url)

            if response.status_code is not 200:
                raise Exception(f"Error: Response status code: {response.status_code}")

            return response.json()
        
        except Exception as error:
            pass



    def test(self, test):
        if test:
            self.__base_url = 'https://sandbox.iexapis.com/v1'
        else: 
            self.__base_url = 'https://cloud.iexapis.com/v1'
