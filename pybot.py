from selenium import webdriver
import time

class Keys(object):
    """
    Set of special keys codes.
    """

    NULL = u'\ue000'
    CANCEL = u'\ue001'  # ^break
    HELP = u'\ue002'
    BACKSPACE = u'\ue003'
    BACK_SPACE = BACKSPACE
    TAB = u'\ue004'
    CLEAR = u'\ue005'
    RETURN = u'\ue006'
    ENTER = u'\ue007'
    SHIFT = u'\ue008'
    LEFT_SHIFT = SHIFT
    CONTROL = u'\ue009'
    LEFT_CONTROL = CONTROL
    ALT = u'\ue00a'
    LEFT_ALT = ALT
    PAUSE = u'\ue00b'
    ESCAPE = u'\ue00c'
    SPACE = u'\ue00d'
    PAGE_UP = u'\ue00e'
    PAGE_DOWN = u'\ue00f'
    END = u'\ue010'
    HOME = u'\ue011'
    LEFT = u'\ue012'
    ARROW_LEFT = LEFT
    UP = u'\ue013'
    ARROW_UP = UP
    RIGHT = u'\ue014'
    ARROW_RIGHT = RIGHT
    DOWN = u'\ue015'
    ARROW_DOWN = DOWN
    INSERT = u'\ue016'
    DELETE = u'\ue017'
    SEMICOLON = u'\ue018'
    EQUALS = u'\ue019'

    NUMPAD0 = u'\ue01a'  # number pad keys
    NUMPAD1 = u'\ue01b'
    NUMPAD2 = u'\ue01c'
    NUMPAD3 = u'\ue01d'
    NUMPAD4 = u'\ue01e'
    NUMPAD5 = u'\ue01f'
    NUMPAD6 = u'\ue020'
    NUMPAD7 = u'\ue021'
    NUMPAD8 = u'\ue022'
    NUMPAD9 = u'\ue023'
    MULTIPLY = u'\ue024'
    ADD = u'\ue025'
    SEPARATOR = u'\ue026'
    SUBTRACT = u'\ue027'
    DECIMAL = u'\ue028'
    DIVIDE = u'\ue029'

    F1 = u'\ue031'  # function  keys
    F2 = u'\ue032'
    F3 = u'\ue033'
    F4 = u'\ue034'
    F5 = u'\ue035'
    F6 = u'\ue036'
    F7 = u'\ue037'
    F8 = u'\ue038'
    F9 = u'\ue039'
    F10 = u'\ue03a'
    F11 = u'\ue03b'
    F12 = u'\ue03c'

    META = u'\ue03d'
    COMMAND = u'\ue03d'

class AmazonBot:
    def __init__(self):
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get('https://www.amazon.in/')
        time.sleep(1)

    def search(keyword):
        search = bot.find_element_by_class_name('nav-searchbar')
        search.clear()
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)
        time.sleep(2)

instanc = AmazonBot()
keyword = 'toys'
instanc.login()
instanc.search(keyword)