class PyAlgoUtils:
    
    def order_dict(self, data):
        '''
        :data - Python dictionary of stock data
        '''
        
        if not isinstance(data, dict):
            raise Exception("Data must be type dictionary")        
        
        # Catches exception if key doesn't exist in data dictionary
        try:
            ordered_dict = {
                "Date Time": data["date"] + " 13:59:00",
                "Open": data["open"],
                "High": data["high"],
                "Low": data["low"],
                "Close": data["close"],
                "Volume": data["volume"],
                "Adj. Close": data["close"]
            }
        except Exception:
            return None
        
        return ordered_dict