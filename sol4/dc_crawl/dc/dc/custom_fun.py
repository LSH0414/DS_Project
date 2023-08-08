import time
import requests, re
from bs4 import BeautifulSoup

from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

from datetime import datetime, timedelta

from tqdm import tqdm

import pandas as pd

import warnings
warnings.filterwarnings('ignore')

headers = {
    'user-agent' : ua.random
}

#갤러리 타입 가져오기(마이너, 일반)
def get_gallery_type(dc_id):
    #url로 requests를 보내서 redirect시키는지 체크한다.
    url = f'https://gall.dcinside.com/board/lists/?id={dc_id}'
    result = url
    
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")
    if "location.replace" in str(soup):
        redirect_url = str(soup).split('"')[3]
        result = redirect_url
    if "mgallery" in result:
        result = "mgallery/board"
    else:
        result = "board"
        
    return result

def make_galleryURL(gall_id):
    base_url = "https://gall.dcinside.com/"
    url = base_url + get_gallery_type(gall_id) + "/lists?id=" + gall_id

    return url

