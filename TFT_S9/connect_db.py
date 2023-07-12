import  mysql.connector
import pandas as pd 
import os
import re
import requests
import json
import numpy as np

from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

with open('/Users/seokholee/lsh/Project/TFT_S9/api_keys.txt', 'r') as f:
    api_keys = [re.sub('\n', '', key) for key in f.readlines()]

# DB 연결 함수
def init_mysql():
    aws = mysql.connector.Connect(
        database = '',
        host = "",
        port = 3306,
        user = '',
        password = ''
    )
    return aws

def getDataSQL(query):
    
    sql = init_mysql()
    df = pd.read_sql_query(query, sql)
    sql.close()

    return df

def getDataRaw(query):
    print(query)
    sql = init_mysql()
    cur = sql.cursor()
    cur.execute(query)
    result = cur.fetchall()
    sql.close()
    return result

def get_csv_data(dir, version):
    master_path = f'/Users/seokholee/lsh/Project/TFT_S9/data/csv/{dir}/'
    os.chdir(master_path)

    if version == 'all':
        csv_files = [master_path + file for file in os.listdir() if re.search('(.csv)$',file)]
    else:
        csv_files = [master_path + file for file in os.listdir() if version in file]
    os.chdir('/Users/seokholee/lsh/Project/TFT_S9')


    return csv_files


def get_csv_pyspark(dir, version):
    dir_path = f"/Users/seokholee/lsh/Project/TFT_S9/data/csv/{dir}"
    
    csv_files = []
    for (root, directories, files) in os.walk(dir_path):

        for file in files:
            if version == 'all':
                if re.search('(.csv)$',file):
                    csv_files.append(root + '/' + file)
            else:
                if version in file:
                    csv_files.append(file)
    
    return csv_files

# 챌린저 정보 가져오기 RIOT API
def tft_challenger_summoners(api_idx):

    headers = {
    "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,es;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com/",
    }

    url = f'https://kr.api.riotgames.com/tft/league/v1/challenger'
    headers["User-Agent"] =  ua.random
  
    while True:
        headers["X-Riot-Token"] = api_keys[api_idx]
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise
            else:
                return response.json()
        except:
            api_idx = np.random.choice(len(api_keys), size=1, replace=False)[0]

            

def getChallengers(): 
    
    max_len = len(api_keys)
    results = dict()

    summoners = []

    for i in range(max_len):
        summoners.append(tft_challenger_summoners(i))
                
    for idx, summoner in enumerate(summoners):
        
        texts = summoner['entries']

        for data in texts:
            results[data['summonerId']] = data['summonerName']

    with open('./data/Challenger_user.json', 'w') as f:
        json.dump(results, f)
