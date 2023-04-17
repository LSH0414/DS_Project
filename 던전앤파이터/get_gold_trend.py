from urllib import parse

import pandas as pd
import xmltodict

import warnings
warnings.filterwarnings('ignore')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome( service=Service(ChromeDriverManager().install()) )

url = 'http://trade.itemmania.com/_xml/gamemoney_avg.xml.php?gamecode=281&servercode=12189&count=90'
driver.get(url)

html = driver.page_source
driver.close()

dict_type = xmltodict.parse(html)

gold_info = dict_type['html']['body']['div']
gold_info_df = pd.DataFrame(gold_info[0]['quotation']['data'])

gold_info_df.to_csv('gold_price.csv', index=False)