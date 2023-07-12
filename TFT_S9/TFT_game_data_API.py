import pandas as pd
import numpy as np

import requests
from urllib import parse
import json

import time
import datetime
import re
import os

import db_connect

from tqdm import tqdm
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)

import warnings

warnings.filterwarnings('ignore')

api_path = '' # txt file
with open(api_path, 'r') as f:
    api_keys = [re.sub('\n', '', key) for key in f.readlines()]

headers = {
    "Accept-Language": "ko,en-US;q=0.9,en;q=0.8,es;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com/",
}

# 소환사 정보 가져오기

def tft_summoner_info_summonerName(summonerName, api_idx): #닉네임으로 탐색
    encodingName = parse.quote(summonerName)
    url = f'https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-name/{encodingName}'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers=headers)

def tft_summoner_info_summonerId(summonerId, api_idx): # 소환사 ID로 탐색
    url = f'https://kr.api.riotgames.com/tft/summoner/v1/summoners/{summonerId}'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers = headers)

def tft_summoner_info_puuid(puuid, api_idx): # puuid로 탐색
    url =  f'https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers = headers)

# 타겟 소환사의 게임 id 가져오기. 기본 50 게임 조회
def tft_match_ids(puuid, api_idx, count=50):
    url = f'https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={count}'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers=headers)

def tft_get_Game_info(matchId, api_idx):
    url = f'https://asia.api.riotgames.com/tft/match/v1/matches/{matchId}'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers=headers)


def tft_tier_summoners(tier, division, api_idx, page=1):
    url = f'https://kr.api.riotgames.com/tft/league/v1/entries/{tier}/{division}?page={page}'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers=headers)


# 챌린저, 그마, 마스터 티어는 따로 가져와야함
# 3개의 상위 티어는 페이지 구분없이 해당 티어의 모든 유저의 정보를 넘겨줌

def tft_challenger_summoners(api_idx):
    url = f'https://kr.api.riotgames.com/tft/league/v1/challenger'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers=headers)

def tft_grandmaster_summoners(api_idx):
    url = f'https://kr.api.riotgames.com/tft/league/v1/grandmaster'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers=headers)

def tft_master_summoners(api_idx):
    url = f'https://kr.api.riotgames.com/tft/league/v1/master'
    headers["User-Agent"] =  ua.random
    headers["X-Riot-Token"] = api_keys[api_idx]
    return requests.get(url, headers=headers)

#나머지 티어 정보 가져오기

def getSummoner_df(): 
    
    results = [pd.DataFrame() for _ in range(5)]

    tiers = ['C', 'GM', 'M', 'DIAMOND','PLATINUM','GOLD', 'SILVER', 'BRONZE', 'IRON']
    divisions = ['I', 'II', 'III', 'IV']

    for tier in tqdm(tiers):

        if tier in ['C']:
            
            summoners = []
            if tier in ['C']:
                if tier == 'C': #챌린저
                    for i in range(4):
                        summoners.append(tft_challenger_summoners(i))
                
                for idx, summoner in enumerate(summoners):
                    if idx == 0:
                        print(summoner.json())
                        texts = summoner.json()
                        # 대표 DF
                        top_tier_df = pd.DataFrame(texts['entries'])
                        top_tier_df.sort_values('leaguePoints', ascending=False, inplace=True)
                        top_tier_df['tier'] = texts['tier']
                        top_tier_df['leagueId'] = texts['leagueId']
                        top_tier_df['queueType'] = texts['queue']

                        results[idx] = pd.concat([results[idx], top_tier_df])

                    else:
                        texts = summoner.json()
                        
                        tier_df = pd.DataFrame(texts['entries'])
                        tier_df.sort_values('leaguePoints', ascending=False, inplace=True)
                        
                        tier_df = tier_df[['summonerId', 'summonerName']]
                        
                        results[idx] = pd.concat([results[idx], tier_df])
                
            else:
                div_df = [pd.DataFrame() for _ in range(5)]
                
                for division in divisions:
                    for page in range(1,20):
                        tmp = []
                        for i in range(5):
                            tmp.append(tft_tier_summoners(tier, division, i, page))

                        #소환사 정보가 없는 페이지 확인
                        if tmp[0].text == '[]':
                            break
                        else:
                            for i in range(5):
                                div_df[i] = pd.concat([div_df[i], pd.DataFrame(tmp[i].json())])

                        #요청 제한 시간 범위 때문에 딜레이 설정
                        time.sleep(1)
                        
                for i in range(5):
                    if i == 0:
                        results[i] = pd.concat([results[i], div_df[i]])
                    else:
                        tmp = div_df[i][['summonerId', 'summonerName']]
                        results[i] = pd.concat([results[i], tmp])
        else:
            pass  
    return results

def getPuuids(df, tier):

    with open('/Users/seokholee/lsh/Project/TFT_S9/data/puuid_dict.json', 'r') as f:
        puuid_dict = json.load(f)
    result = []
    
    flag = df['tier'] == tier
    summonerId_list = ['summonerId', 'summonerId_1', 'summonerId_2', 'summonerId_3']
    
    target = df[flag]
    
    if tier in ['CHALLENGER', 'GRANDMASTER']:
        pass
    
    api_idx = 0
    cnt = 0
    for _, row in target.iterrows():
        
        if cnt > 90:
            if api_idx==3:
                api_idx=0
            else:
                api_idx+=1
            
            cnt = 0
                
        summonerId = row[summonerId_list[api_idx]]
        
        try:
            response = tft_summoner_info_summonerId(summonerId, api_idx)
            
            result.append(response.json()['puuid'])

            
            if response.json()['puuid'] not in list(puuid_dict.keys()):
                puuid_dict[response.json()['puuid']] = response.json()['name']
        except Exception as e:
            print(e)
            # print(row)
            # print(response)
            # break
        cnt+=1
        time.sleep(0.05)

    with open('/Users/seokholee/lsh/Project/TFT_S9/data/puuid_dict.json', 'w') as f:
        json.dump(puuid_dict, f)
    return result

def getGameIds(puuids, game_count = 30):
    result = []
    
    api_idx = 0
    api_idxs = [0,1,2,3]
    cnt = 0
    for puuid in puuids:
            
        flag = True
        while flag:
            try:
                response = tft_match_ids(puuid, api_idx, game_count)
                if response.status_code != 200:
                    raise
                else:
                    result = result + response.json()
                    flag = False
            except:
                api_idx = np.random.choice(api_idxs, size=1, replace=False)[0]
                time.sleep(1)

        cnt+=1
        time.sleep(0.05)
        
        result = list(set(result))

    return result

def getGamesDataDf(game_ids, S9_UPDATE_DATE = '2023-06-28 06:23:00'):
    result = dict()

    # unix timestamp 
    S9_UPDATE_DATE = datetime.datetime.strptime(S9_UPDATE_DATE,'%Y-%m-%d %H:%M:%S').timestamp()

    api_idxs = [0,1,2,3]
    api_idx = 0
    error_cnt = 0
    game_idx = 0

    for gameId in tqdm(game_ids):
        
        #게임 데이터 가져오기 - 정보 가져올 수 있는 api_key 값 찾기(랜덤 샘플링)
        flag = True
        while flag:
            try:
                res = tft_get_Game_info(gameId, api_idx)
                game_data = res.json()['info']
                flag = False
            except:
                api_idx = np.random.choice(api_idxs, size=1, replace=False)[0]
                
                error_cnt+=1

                if error_cnt > 10:
                    print('ERROR CNT OVER')    
                    error_cnt = -1
                    break
                time.sleep(1)

        if error_cnt == -1:
            error_cnt = 0
            continue
        # Millisecond -> second
        game_time = (game_data['game_datetime'] / 1000)

        # 시즌 8 게임이 아니라면 패스
        if S9_UPDATE_DATE > game_time:
            # print(game_time)
            continue

        else:
            # game_participants = game_data['participants']

           #게임 데이터 추가
            result[game_idx] = res.json()
            game_idx+=1

#         time.sleep(0.1)

    return result

import  mysql.connector

# DB 연결 함수 - 각자 DB사용
def init_mysql():
    aws = mysql.connector.Connect(
        database = '',
        host = "",
        port = 3306,
        user = '',
        password = ''
    )
    return aws

# DB에 데이터 삽입
def excecuteDB(df, table_name):
    aws = init_mysql()
    cur = aws.cursor()
    cols = df.columns
    insert_cols = ",".join(cols)
    
    for idx, row in df.iterrows():
        insert_value = ['"'+str(row[col])+'"' for col in cols]
        insert_value = ",".join(map(str,insert_value))
             
        query = f'INSERT INTO {table_name}('+ insert_cols +') VALUES('+ insert_value +');'
            
        if query != '':
            cur.execute(query)
        
    aws.commit()
    aws.close()

def match_table(data):
    match_id = data['metadata']['match_id']

    # 게임 시간
    game_time = data['info']['game_datetime'] # unixtime * 1000

    # 게임 진행 시간(M)
    game_length = data['info']['game_length']

    # 게임 버전
    game_version = re.search('Version [0-9.]+', data['info']['game_version']).group(0).replace('Version', '').strip()

    df = pd.DataFrame({
        'match_id' : match_id,
        'game_time' : game_time,
        'game_length' : game_length,
        'game_version' : game_version
    },index=[0])
    excecuteDB(df, 'match_table')
    

def match_basic_data(data):
    match_id = data['metadata']['match_id']

    augment_1, augment_2, augment_3 = [], [], []
    gold_left, level, placement, kill_players = [], [], [], []
    dead_time, total_damaged, last_round, puuid = [], [], [], []

    for user_data in (data['info']['participants']):
        # 증강
        augments = [None, None, None]

        for idx, aug in enumerate(user_data['augments']):
            augments[idx] = aug

        # augment_1, augment_2, augment_3 = augments[0], augments[1], augments[2]
        augment_1.append(augments[0])
        augment_2.append(augments[1])
        augment_3.append(augments[2])


        # 남은 골드
        # gold_left = user_data['gold_left']
        gold_left.append(user_data['gold_left'])

        # 최종라운드
        # last_round = user_data['last_round']
        last_round.append(user_data['last_round'])

        # 레벨
        # level = user_data['level']
        level.append(user_data['level'])

        #등수
        # placement = user_data['placement']
        placement.append(user_data['placement'])

        # 마무리 횟수
        # kill_players = user_data['players_eliminated']
        kill_players.append(user_data['players_eliminated'])

        #puuids(고유 아이디)
        # puuid = user_data['puuid']
        puuid.append(user_data['puuid'])

        # 죽은 시간
        # dead_time = user_data['time_eliminated']
        dead_time.append(user_data['time_eliminated'])

        # 가한 데미지
        # total_damaged = user_data['total_damage_to_players']
        total_damaged.append(user_data['total_damage_to_players'])
    
    df = pd.DataFrame({
        'puuid' : puuid,
        'augment_1' : augment_1,
        'augment_2' :  augment_2,
        'augment_3' :  augment_3,
        'gold_left' :  gold_left,
        'last_round' : last_round,
        'level'  : level,
        'placement' : placement,
        'kill_players' :  kill_players,
        'dead_time' : dead_time,
        'total_damaged' : total_damaged
    })
    
    df['match_id'] = match_id

    excecuteDB(df, 'match_basic_info')
    
def match_detail_traits(data):
    total_df = pd.DataFrame()
    match_id = data['metadata']['match_id']

    for i in range(len(data['info']['participants'])):
        puuid = data['info']['participants'][i]['puuid']

        name, num_units, tier_current, tier_total = [], [], [], []
        # 시너지
        for datas in data['info']['participants'][i]['traits']:
            name.append(datas['name']) # 시너지 명
            num_units.append(datas['num_units']) # 유닛수
            # style = datas['style'] #?
            tier_current.append(datas['tier_current']) # 활동화 시너지 단계
            tier_total.append(datas['tier_total']) # 시너지 맥시점 단계

        df = pd.DataFrame({
            'name' : name,
            'num_units' : num_units,
            'tier_current' : tier_current,
            'tier_total' : tier_total,
            'puuid' : puuid
        })
        df['match_id'] = match_id
        total_df = pd.concat([total_df, df])
                    
    excecuteDB(total_df, 'match_detail_traits')


def match_detail_units(data):
    total_df = pd.DataFrame()
    match_id = data['metadata']['match_id']

    for i in range(len(data['info']['participants'])):
        puuid = data['info']['participants'][i]['puuid']


        champ_name, item_1, item_2, item_3 = [], [], [], []
        rarity, tier = [], []
        # 기물 정보
        for datas in data['info']['participants'][i]['units']:
            champ_name.append(datas['character_id']) # 챔피언 이름

            # 아이템 정보
            items = datas['itemNames']
            if len(items) != 3:
                while len(items) < 3:
                    items.append(None)
            
            item_1.append(items[0])
            item_2.append(items[1])
            item_3.append(items[2])


            # 기물 등급
            rarity.append(datas['rarity'])

            # 1성, 2성, 3성(기물 합치기)
            tier.append(datas['tier'])

        df = pd.DataFrame({
            'name' : champ_name,
            'item_1' : item_1,
            'item_2' : item_2,
            'item_3' : item_3,
            'rarity' : rarity,
            'tier' : tier,
            'puuid' : puuid
        })

        total_df = pd.concat([total_df, df])

    total_df['match_id'] = match_id
    excecuteDB(total_df, 'match_detail_units')
            

def challenger_api():
    print('Starting challenger_api')

    print('Get Challeger Summoners')
    summoners_list = getSummoner_df()[:4]
    
    
    for idx, df in enumerate(summoners_list):
        
        df = df.drop_duplicates(['summonerName'])
        if idx == 0:
            summoner_to_csv = df
        else:
            df = df.rename(columns={'summonerId' : 'summonerId_'+str(idx)})
            
            summoner_to_csv = summoner_to_csv.merge(right=df, how='inner', on = 'summonerName')
    
    print('Get Challeger Summoners Puuid')
    tier_puuids = dict()
    tiers = ['CHALLENGER',]
    for tier in tqdm(tiers):
        tier_puuids[tier] = getPuuids(summoner_to_csv, tier)

    game_ids = []

    print("Get Challeger Summoner's Gmaes")
    for value in tier_puuids.values():
        tmp = getGameIds(value, game_count = 10)
        game_ids.append(tmp)

    with open('./data/db_update_time.txt', 'r') as f:
        S9_UPDATE_DATE = f.readline()
    
    now = time.time()
    with open('./data/db_update_time.txt', 'w') as f:
        f.write(time.strftime('%Y-%m-%d %H:%m:00', time.localtime(now)))

    print("Get Challeger Summoner's Gmaes Data")
    CHALL_GAMES = getGamesDataDf(game_ids[0], S9_UPDATE_DATE = S9_UPDATE_DATE)

    with open(f'./data/CHALLENGER_GAMES_{now}.json', 'w') as f:
        json.dump(CHALL_GAMES, f)

    path = f'./data/CHALLENGER_GAMES_{now}.json'
    with open('./data/recent_game_data.txt', 'w') as f:
        f.write(path)

    print("Get Challeger Summoner's Gmae Data FIN")

    return now


def insert_data(data):
    match_table(data)
    match_basic_data(data)
    match_detail_traits(data)
    match_detail_units(data)

from pyspark.sql import SparkSession


def get_recent_version():

    with open ('./data/recent_version.txt', 'r') as f:
        ver = f.readline()
    
    return str(ver)

# make_unit_csv
def make_units():

    # Create SparkSession
    spark = SparkSession.builder \
           .appName('SparkByExamples.com') \
           .config("spark.jars", "mysql-connector-j-8.0.31.jar")\
           .getOrCreate()

    recent_ver = get_recent_version()

    with open('/Users/seokholee/lsh/Project/TFT_S9/data/load_time_pyspark.txt', 'r') as f:
        pyspark_time = f.readline()

    game_query =  f'select distinct * from match_table where game_time > {pyspark_time}'
    query = f'select mbi_tb.match_id match_id, mbi_tb.puuid puuid, game_time, game_length, game_version, placement, name, item_1, item_2, item_3, tier ' + \
    f'from (select mbi.match_id match_id, puuid, placement, game_time, game_length, game_version from match_basic_info mbi join ({game_query}) tb1 on mbi.match_id = tb1.match_id) mbi_tb join ' + \
     f'(select mdu.match_id match_id, puuid, name, item_1, item_2, item_3, tier from match_detail_units mdu join ({game_query}) tb2 on mdu.match_id = tb2.match_id) mdu_tb ' +\
     'on mbi_tb.match_id = mdu_tb.match_id and mbi_tb.puuid = mdu_tb.puuid'

    print(query)
    
    df = spark.read \
    .format("jdbc") \
    .option("driver","com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://[host]/[database]") \
    .option("query", query) \
    .option("user", '[user]') \
    .option("password", '[password]') \
    .load()
    
    save_path = f"./data/csv/units/pyspark_Ver{recent_ver}_{pyspark_time}"
    df.write.option("header",True).csv(save_path)
    
    for (root, directories, files) in os.walk(save_path):
        for file in files:
            if re.search('(.csv)$',file):
                csv_files = (root + '/' + file)

    last_data_time = max(pd.read_csv(csv_files)['game_time'])
    with open('/Users/seokholee/lsh/Project/TFT_S9/data/load_time_pyspark.txt', 'w') as f:
        f.write(str(last_data_time))
    


if __name__ == "__main__":
    csv_time = challenger_api()
    with open('./data/recent_game_data.txt') as f:
        recent_games_path = f.readline()
    with open(recent_games_path, 'r') as f:
        chall_games = json.load(f)

    print('GAME DATA INSERT  DB')
    for key,value in tqdm(chall_games.items()):
        insert_data(value)
    print('GAME DATA INSERT  DB FIN!!')

    print('MAKE TRAITS CSV FILE SQL')
    recent_ver = get_recent_version()
    with open('/Users/seokholee/lsh/Project/TFT_S9/data/load_time_pyspark.txt', 'r') as f:
        pyspark_time = f.readline()

    b_query = f'select mt.match_id match_id, puuid, placement, game_version, game_time from match_basic_info mbi join (select * from match_table where game_time > "{str(pyspark_time)}") mt on mbi.match_id = mt.match_id'

    query = f'select mdt.match_id match_id, mdt.puuid puuid, name, num_units, tier_current, tier_total, placement, game_version, game_time from match_detail_traits mdt join ({b_query}) tb on mdt.match_id = tb.match_id and mdt.puuid = tb.puuid '
    df = db_connect.getDataSQL(query)

    df.to_csv(f'./data/csv/traits/traits_{recent_ver}_{str(pyspark_time)}.csv', index=False)

    print('MAKE AUGMETS CSV FILE SQL')
    query = f'select distinct ' + \
        'mt.match_id match_id, game_time, game_length, game_version, placement, augment_1, augment_2, augment_3 ' + \
        f'from match_table mt join match_basic_info mbi on mt.match_id = mbi.match_id where  mt.game_time > "{str(pyspark_time)}";'
        
    df = db_connect.getDataSQL(query)

    df.to_csv(f'./data/csv/augments/augments_ver{recent_ver}_{pyspark_time}.csv', index=False)

    print('MAKE CSV FILE (Pyspark)')
    make_units()
    print('MAKE CSV FILE (Pyspark) FIN')

    print('ALL PROCESS FIN')
