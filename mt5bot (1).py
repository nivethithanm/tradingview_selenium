import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
    
class telegram_chatbot():

    def __init__(self, token):
        self.token = token
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def make_reply(self,msg):
        reply = None
        if msg is not None:
            reply = msg
        return reply
    
    def make_plot(self,msg):
        list_ = msg.split(',')
        if(len(list_) == 4):
            getPlot(str(list_[1]), str(list_[2]), str(list_[3]), str(list_[4]))
            return
    
    def getPlot(tick1, tick2, timeframe1, timeframe2):
        format_str = '%d/%m/%Y'
        #tick_1 = mt5.copy_ticks_from(str(tick1), datetime.strptime(timeframe1, format_str), 1000, mt5.COPY_TICKS_ALL)
        #tick_2 = mt5.copy_ticks_from(str(tick2), datetime.strptime(timeframe1, format_str), 1000, mt5.COPY_TICKS_ALL)    
        tick_1 = mt5.copy_rates_range(tick1, mt5.TIMEFRAME_M1, datetime.strptime(timeframe1, format_str), datetime.strptime(timeframe2, format_str))
        tick_2 = mt5.copy_rates_range(tick2, mt5.TIMEFRAME_M1, datetime.strptime(timeframe1, format_str), datetime.strptime(timeframe2, format_str))
        mt5.shutdown()
        ticks1_frame = pd.DataFrame(tick_1)
        ticks2_frame = pd.DataFrame(tick_2)
        ticks1_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
        ticks2_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
        # display ticks on the chart
        plt.plot(ticks1_frame['time'], ticks_frame['ask'], 'r-', label=str(tick1)+'ask')
        plt.plot(ticks1_frame['time'], ticks_frame['bid'], 'b-', label=str(tick1)+'bid')
        plt.plot(ticks2_frame['time'], ticks_frame['ask'], 'r*', label=str(tick2)+'ask')
        plt.plot(ticks2_frame['time'], ticks_frame['bid'], 'b*', label=str(tick2)+'bid')
         # display the legends
        plt.legend(loc='upper left')
        # add the header
        plt.title(str(tick1) + 'vs' + str(tick2))
        # display the chart
        plt.savefig('file.png')
        command = 'curl -s -X POST https://api.telegram.org/bot' + str(self.token) + '/sendPhoto -F chat_id=' + str(chat_id) + ' -F photo=@' + imagefile
        subprocess.call(command.split(' '))
        return   


token = '1554901580:AAHs2Y559I1m1WkGSwmLPt84jdI9hT6khlc'
bot = telegram_chatbot(token)

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            if (message.find('/getPlot') != -1):
                bot.make_plot(message)
            elif (message.find('/help') != -1):
                bot.send_message('Syntax:\nUse this function to get plots /getPlot,Ticker1,Ticker2,StartTime,EndTime\nNote: Dates should be in detail DD/MM/YYYY/hh/mm format', from_)
            else:
                bot.send_message('Syntax:\nUse this function to get plots /getPlot,Ticker1,Ticker2,StartTime,EndTime\nNote: Dates should be in detail DD/MM/YYYY/hh/mm format', from_)           
