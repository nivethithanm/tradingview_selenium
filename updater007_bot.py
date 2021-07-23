import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
import json
import subprocess
import re

"""
TradingViewBot: Definitions of all actions needed to Login and get Charts from TradingView.com using Mozilla Firefox

TradingBotActions: Sequence of actions for tradingview.com simplified

TelegramBot: Handles the messages from Telegram. Definition of our bot

BotFunctions: Payload handling and delegation of TelegramBot's functions

"""

class TradingViewBot:
    
    def __init__(self, val):
        fireFoxOptions = webdriver.FirefoxOptions()
        profile = webdriver.FirefoxProfile('/home/nivethithan/.mozilla/firefox/phwph1d8.default')

        #options.add_argument("user-data-dir=C:\\Path")
        #data_dir = get_data_dir()
        #profile_path = os.path.join(data_dir, 'Selenium_chromium')
        #fireFoxOptions.add_argument(f'--user-data-dir={data_dir}')
        self.bot = webdriver.Firefox(firefox_profile=profile)
        
        # FOR /marvel
        if(val == 0):
            # Update url id
            self.chart = 'g5uZs5rR'
        # FOR /matrix
        elif(val == 1):
            # Update url id
            self.chart = 'g5uZs5rR'

    def login(self,symbol = 'NASDAQ:AMZN',interval = 'D',theme = 'light'):
        # Opens the Firefox with the following url
        bot = self.bot
        bot.get("https://in.tradingview.com/chart/" + str(self.chart) + "/?interval="+ str(interval) + "&symbol=" + str(symbol.upper()) + "&theme=" + str(theme))
        time.sleep(2)
    
    def checkLogin(self,username,password):
        # Enters email_id and password and logs into your account
        if (len(self.bot.find_elements_by_class_name('js-login-link')) == 0):
            time.sleep(2)
        else:
            self.bot.find_element_by_class_name('js-login-link').click()
            time.sleep(2)
            self.bot.find_element_by_class_name('tv-signin-dialog__toggle-email').click()
            time.sleep(2)
            self.bot.find_element_by_name('username').send_keys(username)
            self.bot.find_element_by_name('password').send_keys(password)
            self.bot.find_element_by_class_name('tv-button__loader').click()
        time.sleep(10) #Increase 10 to 120
    
    def getScreen(self):
        # Gets a screenshot of current Firefox screen
        self.bot.save_screenshot(str(os.path.abspath(os.getcwd())) + '/screenshot.png')
        
    def close(self):
        # Closes the Web browser
        self.bot.close()

        
def TradingBotActions(val,  symbol = "NASDAQ:NFLX", interval = "D", theme = "light"):
    # Change Mail ID and Passsword
    username = 'jpnivemeow@gmail.com'
    password = 'Fuck@ll1'
    instanc = TradingViewBot(val)
    instanc.login(symbol,interval,theme)
    instanc.checkLogin(username,password)
    instanc.getScreen()
    instanc.close()

class TelegramBot():
    
    def __init__(self, token):
        # Initializes the Telegram bot and collects payloads
        self.token = token
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        # Get updates about the payloads
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        # Sends text message to a chat with Chat ID = chat_id
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)
    
    def send_picture(self,msg,chat_id,val = 0):
        # Sends the picture got from Web browser's snapshot
        list_ = msg.split(' ')
        # Case for Input: Bot command and ticker symbol
        if(len(list_) == 2):
            symbol = str(list_[1])
            TradingBotActions(val=val, symbol=symbol)
            command = 'curl -s -X POST https://api.telegram.org/bot' + str(self.token) + '/sendPhoto -F chat_id=' + str(chat_id) + ' -F photo=@' + str(os.path.abspath(os.getcwd())) + '/screenshot.png'
            subprocess.call(command.split(' '))
            return
        # Case for Input: Bot command, ticker symbol and TimeFrame    
        elif(len(list_) == 3):
            symbol = str(list_[1])
            interval = str(list_[2])
            TradingBotActions(val=val, symbol=symbol, interval=interval)
            command = 'curl -s -X POST https://api.telegram.org/bot' + str(self.token) + '/sendPhoto -F chat_id=' + str(chat_id) + ' -F photo=@' + str(os.path.abspath(os.getcwd())) + '/screenshot.png'
            subprocess.call(command.split(' '))
            return
        # Case for Input: Bot command, ticker symbol, TimeFrame and Theme     
        elif(len(list_) == 4):
            symbol = str(list_[1])
            interval = str(list_[2])
            theme = str(list_[3])
            TradingBotActions(val=val, symbol = symbol, interval = interval, theme = theme)
            command = 'curl -s -X POST https://api.telegram.org/bot' + str(self.token) + '/sendPhoto -F chat_id=' + str(chat_id) + ' -F photo=@' + str(os.path.abspath(os.getcwd())) + '/screenshot.png'
            subprocess.call(command.split(' '))
            return
    
def BotFunctions(token):
    bot = TelegramBot(token)
    update_id = None
    # Handles payloads parsing
    while True:
        updates = bot.get_updates(offset=update_id)
        if('result' in updates):
            updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                try:
                    if("message" in item):
                        if ('text' in item['message']):
                            message = str(item["message"]["text"])
                        else:
                            message = None
                    elif ("edited_message" in item):
                        if ('text' in item['message']):
                            message = str(item["edited_message"]["text"])
                        else:
                            message = None
                except:
                    message = None
                if("message" in item):
                    from_ = item["message"]["chat"]["id"]
                elif ("edited_message" in item):
                    from_ = item["edited_message"]["chat"]["id"]
                
                if (message != None):    
                    if (message.find('/matrix ') != -1):
                        bot.send_picture(message,from_,0)
                
                    elif (message.find('/marvel ') != -1):
                        bot.send_picture(message,from_,1)
                
                    elif (message.find('/help') != -1):
                        bot.send_message('Usage:\n\nUse this function to get plots \n/[Plot-type] [TickerSymbol] [TimeFrame](Optional) [Theme](Optional)\n\nNote: \n\n[Plot-type]: marvel, matrix\n[TimeFrame]: 1-1440 (for minutes), D (for day), M (for Month)\n[Theme]: light, dark\n', from_)
                
                    elif (re.search("\\w+", message) != -1):
                        bot.send_message('Usage:\n\nUse this function to get plots \n/[Plot-type] [TickerSymbol] [TimeFrame](Optional) [Theme](Optional)\n\nNote: \n\n[Plot-type]: marvel, matrix\n[TimeFrame]: 1-1440 (for minutes), D (for day), M (for Month)\n[Theme]: light, dark\n', from_)


# Driver Code --->

# Your Bot Token got from BotFather in Token variable             
token = '1585200585:AAHIrCjRW3D-16dSB9NX__o00GNo4TGZcr4'
BotFunctions(token)

"""
Note:

Adding bot to Telegram Groups: Use "https://telegram.me/<BOT_NAME>?startgroup=true" and choose the groups for correctly adding bot to the groups

Code requirements: Make sure you have Python, Pip, Selenium, Requests, JSON installed on your Server

Installation:
    Python: "https://www.python.org/downloads/"
    Pip: 
        1. Download the get-pip.py file attached
        2. Change Command Prompt's working directory to downloaded location
        3. Run it via Command Prompt using "python get-pip.py" or "python3 get-pip.py"
        4. Pip is installed now
    Selenium: Run "pip install selenium" from your Command Prompt
    Requests: Run "pip install requests" from your Command Prompt
    JSON: Run "pip install json" from your Command Prompt

"""
