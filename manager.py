from HaoPosition import Algo
from time import sleep
import requests
from logging import Handler, Formatter
import logging
import datetime

TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = 


class RequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
                             data=payload).content


class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)


class Manager:
    def __init__(self):
        pass

    def getData(self, stockIndex, startDate, endDate):
        myObj = Algo()
        myData = myObj.getDf(stockIndex, startDate, endDate)
        return myData

    def getPara(self, data):
        myObj = Algo()
        myPara = myObj.getPara(data)
        return myPara

    def getMACD(self, startDate, endDate):
        myObj = Algo()
        macd = myObj.getMACD(startDate=startDate, endDate=endDate)
        return macd

    def callBack(self):
        return self.getData(stockIndex='399106.XSHE', startDate='2021-01-21', endDate='2021-01-28') + self.getData(
            '000001.XSHG', startDate='2021-01-21', endDate='2021-01-28')

    def run(self):
        logger = self.setup_logger()

        # Run forever
        while True:
            print(self.callBack())
            logger.info(
                "position: %s" % self.getPara(data=self.callBack()) + str(self.getMACD('2020-01-01', '2021-01-28')))
            sleep(600)

    def setup_logger(self):
        # Prints logger info to terminal
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
        ch = logging.StreamHandler()
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def message(self):
        logger = logging.getLogger('msg')
        logger.setLevel(logging.INFO)

        handler = RequestsHandler()
        formatter = LogstashFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.setLevel(logging.INFO)
        # run forever
        while True:
            logger.info(
                "position: %s" % self.getPara(data=self.callBack()) + str(self.getMACD('2020-01-01', '2021-01-28')))
            sleep(10)


if __name__ == '__main__':
    myObj = Manager()
    myObj.message()
