from jqdatasdk import *
import numpy as np
import pandas as pd
auth('13808015546', '015546')


class Algo:
    def __init__(self):
        pass

    def getDf(self, stockIndex, startDate, endDate):
        panel = get_price(get_index_stocks(stockIndex), start_date=startDate, end_date=endDate,
                          fields=['open', 'close'],
                          fq='pre')
        panel = pd.pivot_table(panel, index='time', columns='code', values=['open', 'close'])
        df_open = panel['open']
        df_close = panel['close']
        dailyRet = (df_close - df_open) / df_open
        threeRet = dailyRet.iloc[-1] + dailyRet.iloc[-2] + dailyRet.iloc[-3]
        sixRet = dailyRet.sum()
        val1 = 0
        val2 = 0
        for i in range(len(list(threeRet))):
            if threeRet[i] >= 0.05:
                val1 += 1
            elif threeRet[i] <= -0.05:
                val2 += 1
        val3 = 0
        val4 = 0
        for i in range(len(sixRet)):
            if sixRet[i] >= 0.1:
                val3 += 1
            elif sixRet[i] <= -0.1:
                val4 += 1
        para = np.array([val1, val2, val3, val4])
        return para

    def getMACD(self, startDate, endDate):
        df1 = get_price('000001.XSHG', start_date=startDate, end_date=endDate, fq='pre', frequency='1d',
                        fields=['open', 'close'])

        df2 = get_price('399106.XSHE', start_date=startDate, end_date=endDate, fq='pre', frequency='1d',
                        fields=['open', 'close'])  # 深证综指

        df3 = get_price('399102.XSHE', start_date=startDate, end_date=endDate, fq='pre', frequency='1d',
                        fields=['open', 'close']) # 创业板综

        df1['EMA_short'] = df1['close'].ewm(span=12, adjust=False).mean()
        df1['EMA_long'] = df1['close'].ewm(span=26, adjust=False).mean()
        df1['DIF'] = df1['EMA_short'] - df1['EMA_long']
        df1['DEA'] = df1['DIF'].ewm(span=9, adjust=False).mean()

        df2['EMA_short'] = df2['close'].ewm(span=12, adjust=False).mean()
        df2['EMA_long'] = df2['close'].ewm(span=26, adjust=False).mean()
        df2['DIF'] = df2['EMA_short'] - df2['EMA_long']
        df2['DEA'] = df2['DIF'].ewm(span=9, adjust=False).mean()

        df3['EMA_short'] = df3['close'].ewm(span=12, adjust=False).mean()
        df3['EMA_long'] = df3['close'].ewm(span=26, adjust=False).mean()
        df3['DIF'] = df3['EMA_short'] - df3['EMA_long']
        df3['DEA'] = df3['DIF'].ewm(span=9, adjust=False).mean()

        df1 = df1.tail(1)
        df2 = df2.tail(1)
        df3 = df3.tail(1)

        macd = pd.concat([df1, df2, df3])
        para = []
        for i in range(len(macd['DIF'])):
            if macd['DIF'][i] > macd['DEA'][i] >= 0:
                para.append(20)

            elif macd['DIF'][i] > 0 >= macd['DEA'][i]:
                para.append(15)

            elif 0 >= macd['DIF'][i] > macd['DEA'][i]:
                para.append(10)
            else:
                para.append(0)
        return para

    def getPara(self, data):
        if data[0] / data[1] < 1 and data[2] / data[3] < 1:
            para = [0, 0]

        elif data[0] / data[1] >= 2 and data[2] / data[3] >= 2:
            para = [20, 20]

        elif data[0] / data[1] < 1 and data[2] / data[3] >= 2:
            para = [0, 20]

        elif data[0] / data[1] < 1 and 1 <= data[2] / data[3] < 2:
            para = [0, 10]

        elif 1 <= data[0] / data[1] < 2 and 1 <= data[2] / data[3] < 2:
            para = [10, 10]

        elif 1 <= data[0] / data[1] < 2 and data[2] / data[3] < 1:
            para = [10, 0]

        elif 1 <= data[0] / data[1] < 2 and data[2] / data[3] >= 2:
            para = [10, 20]

        elif data[0] / data[1] >= 2 and data[2] / data[3] < 1:
            para = [20, 0]

        else:
            para = [20, 10]
        return para


if __name__ == '__main__':
    obj = Algo()
    print(obj.getMACD('2020-01-01', '2020-11-27'))
