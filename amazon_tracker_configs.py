# Imports
from selenium import webdriver


# Configs

DIRECTORY = 'JSON_Reports'
ITEM_NAME = 'MacBook Pro'
CURRENCY = '$'
MIN_PRICE = '1000'
MAX_PRICE = '2000'
FILTERS = {
    'min' : MIN_PRICE,
    'max' : MAX_PRICE
}
BASE_URL = 'https://www.amazon.com'



# Chrome Driver Setup Functions


def get_chrome_driver(options):
    return webdriver.Chrome(chrome_options=options)

def get_chromdriver_options():
    return webdriver.ChromeOptions()
    
     
def set_ignore_certificate_error(options):
    return options.add_argument('--ignore-certifictae-errors')

def set_incognito_mode(options):
    return options.add_argument('--incognito')

    
def hello():
    print("hello World")