import talib


class factor:
    def __init__(self, df):
        self.open = df.open
        self.high = df.high
        self.low = df.low
        self.close = df.close
        self.volume = df.volume
        self.pct = (self.close - self.open)/self.open
        df['pct'] = self.pct
        self.df = df

    def get_SMA(self):
        self.df['SMA'] =  talib.SMA(self.close, 5).fillna(method = 'bfill').fillna(method = 'ffill')

    def get_BBANDS(self):
        bbands = talib.BBANDS(self.close, 5, matype=1)
        self.df['BBANDS_upper'] = bbands[0]
        self.df['BBANDS_middle'] = bbands[1]
        self.df['BBANDS_lower'] = bbands[2]

    def get_DEMA(self):
        self.df['DEMA'] = talib.DEMA(self.close, timeperiod=30)

    def get_MA(self):
        self.df['MA'] = talib.MA(self.close, timeperiod=30, matype=0)

    def get_EMA(self):
        self.df['EMA'] = talib.EMA(self.close, timeperiod=6)

    def get_KAMA(self):
        self.df['KAMA'] = talib.KAMA(self.close, timeperiod=30)

    def get_MIDPRICE(self):
        self.df['MIDPRICE'] = talib.MIDPOINT(self.close, timeperiod=14)

    def get_SAR(self):
        self.df['SAR'] = talib.SAR(self.high, self.low, acceleration=0, maximum=0)

    def get_T3(self):
        self.df['T3'] = talib.T3(self.close, timeperiod=5, vfactor=0)

    def get_TEMA(self):
        self.df['TEMA'] = talib.TEMA(self.close, timeperiod=30)

    def get_SAREXT(self):
        self.df['SAREXT'] = talib.SAREXT(self.high, self.low, startvalue=0, offsetonreverse=0, accelerationinitlong=0,
                                   accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0,
                                   accelerationshort=0, accelerationmaxshort=0)

    def get_WMA(self):
        self.df['WMA'] = talib.WMA(self.close, timeperiod=30)

    def get_ATR(self):
        self.df['ATR'] = talib.ATR(self.high, self.low, self.close, timeperiod=14)

    def get_NATR(self):
        self.df['NATR'] = talib.NATR(self.high, self.low, self.close, timeperiod=14)

    def get_TRANGE(self):
        self.df['TRANGE'] = talib.TRANGE(self.high, self.low, self.close)

    def get_AD(self):
        self.df['AD'] = talib.AD(self.high, self.low, self.close, self.volume)

    def get_ADOSC(self):
        self.df['ADOSC'] = talib.ADOSC(self.high, self.low, self.close, self.volume, fastperiod=3, slowperiod=10)

    def get_OBV(self):
        self.df['OBV'] = talib.OBV(self.close, self.volume)

    def get_HT_DCPERIOD(self):
        self.df['HT_DCPERIOD'] = talib.HT_DCPERIOD(self.close)

    def get_HT_DCPHASE(self):
        self.df['HT_DCPHASE'] = talib.HT_DCPHASE(self.close)

    def get_HT_PHASOR(self):
        ht = talib.HT_PHASOR(self.close)
        self.df['HT_PHASOR_inphase'] = ht[0]
        self.df['HT_PHASOR_quadrature'] = ht[1]

    def get_HT_SINE(self):
        ht = talib.HT_SINE(self.close)
        self.df['HT_SINE_sine'] = ht[0]
        self.df['HT_SINE_leadsine'] = ht[1]

    def get_HT_TRENDMODE(self):
        self.df['HT_TRENDMODE'] = talib.HT_TRENDMODE(self.close)

    def get_AVGPRICE(self):
        self.df['AVGPRICE'] = talib.AVGPRICE(self.open, self.high, self.low, self.close)

    def get_MEDPRICE(self):
        self.df['MEDPRICE'] = talib.MEDPRICE(self.high, self.low)

    def get_TYPPRICE(self):
        self.df['TYPPRICE'] = talib.TYPPRICE(self.high, self.low, self.close)

    def get_WCLPRICE(self):
        self.df['WCLPRICE'] = talib.WCLPRICE(self.high, self.low, self.close)

    def get_ADX(self):
        self.df['ADX'] = talib.ADX(self.high, self.low, self.close, timeperiod=14)

    def get_ADXR(self):
        self.df['ADXR'] = talib.ADXR(self.high, self.low, self.close, timeperiod=14)

    def get_APO(self):
        self.df['APO'] = talib.APO(self.close, fastperiod=12, slowperiod=26, matype=0)

    def get_AROON(self):
        aroon = talib.AROON(self.high, self.low, timeperiod=14)
        self.df['aroondown'] = aroon[0]
        self.df['aroonup'] = aroon[1]

    def get_AROONOSC(self):
        self.df['AROONOSC'] = talib.AROONOSC(self.high, self.low, timeperiod=14)

    def get_BOP(self):
        self.df['BOP'] = talib.BOP(self.open, self.high, self.low, self.close)

    def get_CCI(self):
        self.df['CCI'] = talib.CCI(self.high, self.low, self.close, timeperiod=14)

    def get_CMO(self):
        self.df['CMO'] = talib.CMO(self.close, timeperiod=14)

    def get_DX(self):
        self.df['DX'] = talib.DX(self.high, self.low, self.close, timeperiod=14)

    def get_MACD(self):
        macd = talib.MACD(self.close, fastperiod=12, slowperiod=26, signalperiod=9)
        self.df['macd'] = macd[0]
        self.df['macdsignal'] = macd[1]
        self.df['macdhist'] = macd[2]

    def get_MACDEXT(self):
        macd = talib.MACDEXT(self.close, fastperiod=12, fastmatype=0,
                       slowperiod=26, slowmatype=0, signalperiod=9,
                       signalmatype=0)

        self.df['macd_ext'] = macd[0]
        self.df['macdsignal_ext'] = macd[1]
        self.df['macdhist_ext'] = macd[2]

    def get_MFI(self):
        self.df['MFI'] = talib.MFI(self.high, self.low, self.close, self.volume, timeperiod=14)

    def get_MINUS_DI(self):
        self.df['MINUS_DI'] = talib.MINUS_DI(self.high, self.low, self.close, timeperiod=14)

    def get_MINUS_DM(self):
        self.df['MINUS_DM'] = talib.MINUS_DM(self.high, self.low, timeperiod=14)

    def get_MOM(self):
        self.df['MOM'] = talib.MOM(self.close, timeperiod=10)

    def get_PLUS_DI(self):
        self.df['PLUS_DI'] = talib.PLUS_DI(self.high, self.low, self.close, timeperiod=14)

    def get_PLUS_DM(self):
        self.df['PLUS_DM'] = talib.PLUS_DM(self.high, self.low, timeperiod=14)

    def get_PPO(self):
        self.df['PPO'] = talib.PPO(self.close, fastperiod=12, slowperiod=26, matype=0)

    def get_ROC(self):
        self.df['ROC'] = talib.ROC(self.close, timeperiod=10)

    def get_ROCP(self):
        self.df['ROCP'] = talib.ROCP(self.close, timeperiod=10)


    def get_RSI(self):
        self.df['RSI'] = talib.RSI(self.close, timeperiod=14)

    def get_STOCH(self):
        st = talib.STOCH(self.high, self.low, self.close, fastk_period=5, slowk_period=3,
                   slowk_matype=0, slowd_period=3, slowd_matype=0)

        self.df['STOCH_slowk'] = st[0]
        self.df['STOCH_slowd'] = st[1]

    def get_STOCHF(self):
        st = talib.STOCHF(self.high, self.low, self.close, fastk_period=5,
                    fastd_period=3, fastd_matype=0)

        self.df['STOCHF_fastk'] = st[0]
        self.df['STOCHF_fastd'] = st[1]

    def get_STOCHRSI(self):
        st = talib.STOCHRSI(self.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.df['STOCHRSI_fastk'] = st[0]
        self.df['STOCHRSI_fastd'] = st[1]

    def get_TRIX(self):
        self.df['TRIX'] = talib.TRIX(self.close, timeperiod=30)

    def get_ULTOSC(self):
        self.df['ULTOSC'] = talib.ULTOSC(self.high, self.low, self.close, timeperiod1=7, timeperiod2=14, timeperiod3=28)

    def get_WILLR(self):
        self.df['WILLR'] = talib.WILLR(self.high, self.low, self.close, timeperiod=14)

    def get_BETA(self):
        self.df['BETA'] = talib.BETA(self.high, self.low, timeperiod=5)

    def get_CORREL(self):
        self.df['CORREL'] = talib.CORREL(self.high, self.low, timeperiod=30)

    def get_LINEARREG(self):
        self.df['LINEARREG'] = talib.LINEARREG(self.close, timeperiod=14)

    def get_LINEARREG_ANGLE(self):
        self.df['LINEARREG_ANGLE'] = talib.LINEARREG_ANGLE(self.close, timeperiod=14)

    def get_LINEARREG_INTERCEPT(self):
        self.df['LINEARREG_INTERCEPT'] = talib.LINEARREG_INTERCEPT(self.close, timeperiod=14)

    def get_LINEARREG_SLOPE(self):
        self.df['LINEARREG_SLOPE'] = talib.LINEARREG_SLOPE(self.close, timeperiod=14)

    def get_STDDEV(self):
        self.df['STDDEV'] = talib.STDDEV(self.close, timeperiod=5, nbdev=1)

    def get_TSF(self):
        self.df['TSF'] = talib.TSF(self.close, timeperiod=14)

    def get_VAR(self):
        self.df['VAR'] = talib.VAR(self.close, timeperiod=5, nbdev=1)

    def get_trial(self):
        return 0

    def get_all(self):
        f = Factor(self.df)
        public_method_names = [method for method in dir(f) if callable(getattr(f, method)) if (not method.startswith('_')) and method not in ['get_all','get_df']]
        for method in public_method_names:
            getattr(f, method)()
        self.df = f.df.copy()


    def get_df(self):
        self.df = self.df.fillna(method = 'ffill').fillna(method = 'bfill')
        return self.df
