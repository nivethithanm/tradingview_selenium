import os
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
import json

path = os.path.abspath(os.getcwd())

def getHtml(symbol, interval):

    html = """
<html>
<head>
<script type="text/javascript" src="https://s3.tradingview.com/tv.js">
</script>
</head>
<body>
<div class="tradingview-widget-container" id="tradingview_c39ad"></div>
<script>
LoadChart("""+ "\"" + str(symbol) + "\"" + ',' + "\"" + str(interval) + "\"" + """);
function LoadChart(symbol, interval){
new TradingView.widget(
  {
  "width": 980,
  "height": 610,
  "symbol": symbol,
  "interval": interval,
  "timezone": "Etc/UTC",
  "theme": "light",
  "style": "1",
  "locale": "in",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "allow_symbol_change": true,
  "container_id": "tradingview_c39ad"
	});
}
</script>
</body>
</html>
"""
    with open(str(path)+ "/index.html", "w+") as file:
        file.write(html)

class TradingViewBot:
    def __init__(self):
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get("file:///"+ str(path)+ "/index.html")
        time.sleep(6)
                      
    def getScreen(self):
        self.bot.save_screenshot(str(path) + '/screenshot.png')
        
    def close(self):
        self.bot.close()
        

symbol = "NASDAQ:AMZN"
interval = "D"
getHtml(symbol, interval)
instanc = TradingViewBot()
instanc.login()
instanc.getScreen()
instanc.close()
