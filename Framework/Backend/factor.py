import talib


class factor:
    def __init__(self, df):
        self.open = df.open
        self.high = df.high
        self.low = df.low
        self.close = df.close
        self.volume = df.volume
        self.df = df

 

    def get_BBANDS(self):
        bbands = talib.BBANDS(self.close, 5, matype=1)
        self.df['BBANDS_upper'] = bbands[0]
        self.df['BBANDS_middle'] = bbands[1]
        self.df['BBANDS_lower'] = bbands[2]

  
    def get_EMA(self):
        self.df['EMA'] = talib.EMA(self.close, timeperiod=6)

    
    def get_ATR(self):
        self.df['ATR'] = talib.ATR(self.high, self.low, self.close, timeperiod=14)

    
    def get_AD(self):
        self.df['AD'] = talib.AD(self.high, self.low, self.close, self.volume)

    
    def get_OBV(self):
        self.df['OBV'] = talib.OBV(self.close, self.volume)

    
    def get_ROC(self):
        self.df['ROC'] = talib.ROC(self.close, timeperiod=10)



    def get_df(self):
        return self.df
