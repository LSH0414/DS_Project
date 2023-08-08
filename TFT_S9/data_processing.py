import re
import json
import time
import pandas as pd
import streamlit as st
from db_connect import *
from collections import Counter

with open('./data/tft_S9_dict.json', 'r') as f:
    tft_dict = json.load(f)

def eng_to_kor(name, col):
    for data in tft_dict[col]:
        if data['apiName'] == name:
            return data['name']

def del_None(data):
    txt = re.sub('(None)+', '', data)
    return re.sub(',{2,}', ',', txt)


def unix_to_local(data):
    result  = time.localtime(int(data)/ 1000)
    result = time.strftime('%Y-%m-%dT%H', result)
    return result

def div_aug(df):
    augments = []
    for _, row in df.groupby(['game_time'], as_index=False).agg({'augment_1': ','.join, 'augment_2' : ','.join, 'augment_3' : ','.join}).iterrows():
        tmp = []
        aug1, aug2, aug3 = del_None(row['augment_1']), del_None(row['augment_2']), del_None(row['augment_3'])
        for aug in aug1.split(','):
            if aug != '':
                tmp.append(aug)

        for aug in aug2.split(','):
            if aug != '':
                tmp.append(aug)

        for aug in aug3.split(','):
            if aug != '':
                tmp.append(aug)


        augments.append(tmp)

    result = pd.DataFrame(df.groupby('game_time')['match_id'].count())
    result['augments'] = augments
    result.reset_index(inplace=True)
    

    return result

def basic_df(target):
    df = pd.DataFrame()
    for csv_path in get_csv_data(target, version='all'):
        tmp = pd.read_csv(csv_path)
        df = pd.concat([df, tmp])
    df = df.drop_duplicates(subset=['match_id','placement'])
    df['game_time'] = pd.to_datetime(df['game_time'].apply(unix_to_local))    

    return df


def augment_line_df(div_flag, version):

    df = pd.DataFrame()
    for csv_path in get_csv_data('augments', version=version):
        tmp = pd.read_csv(csv_path)
        df = pd.concat([df, tmp])
    df = df.drop_duplicates(subset=['match_id','placement'])
    df['game_time'] = pd.to_datetime(df['game_time'].apply(unix_to_local))    

    result = pd.DataFrame()

    aug_all = div_aug(df)
    if  div_flag == 'winner':
        df_winner = df[df['placement'] == 1] #  승리
        result = div_aug(df_winner)

    elif div_flag == 'save_rank':
        df_save = df[df['placement'] < 5]  # 순방
        result = div_aug(df_save)
    
    if div_flag == 'all':
        line_df = make_line_df(aug_all, result, div_flag, slice_num=0)
    else:
        line_df = make_line_df(aug_all, result, div_flag)

    return line_df


def make_line_df(raw_df, df, div_flag, slice_num = 3):
    
    

    line_df = pd.DataFrame()

    if div_flag == 'all':
        for _, row in raw_df.iterrows():
            tmp = pd.DataFrame(Counter(row['augments']), index = [0]).transpose().reset_index()
            tmp.columns = ['augments', 'cnt']
            tmp['game_time'] = row['game_time']
            # tmp['ratio'] = tmp['cnt'] / row['match_id']
            tmp['match_cnt'] = row['match_id']/8

            if slice_num == 0:
                tmp = tmp.set_index('game_time').sort_values('cnt', ascending=False)
            else:
                tmp = tmp.set_index('game_time').sort_values('cnt', ascending=False)[:slice_num]

            line_df = pd.concat([line_df, tmp])
        
    else:
        for idx, row in df.iterrows():
            tmp = pd.DataFrame(Counter(row['augments']), index = [0]).transpose().reset_index()
            tmp.columns = ['augments', 'cnt']
            tmp['game_time'] = row['game_time']

            row_all = raw_df.iloc[idx]
            tmp_all = Counter(row_all['augments'])
            total_cnt = [tmp_all[aug] for aug in tmp['augments']]

            tmp['total_cnt'] = total_cnt
            tmp['ratio'] = tmp['cnt'] / tmp['total_cnt']

            tmp = tmp.set_index('game_time')

            line_df = pd.concat([line_df, tmp])

        
        
    line_df['augments'] = line_df.apply(lambda x : eng_to_kor(x['augments'], 'augments'),axis=1)

    return line_df


def units_tier_df():

    version = 'all'

    df = pd.DataFrame()
    for csv_path in get_csv_pyspark('units', version=version):
        print(csv_path)
        tmp = pd.read_csv(csv_path, encoding='utf8')
        df = pd.concat([df, tmp])
    df = df.drop_duplicates(subset=['match_id','placement','name'])
    return df 


def traits_tier_df():

    version = 'all'

    df = pd.DataFrame()
    for csv_path in get_csv_pyspark('traits', version=version):
        print(csv_path)
        tmp = pd.read_csv(csv_path, encoding='utf8')
        df = pd.concat([df, tmp])
    df = df.drop_duplicates(subset=['match_id','placement','name'])
    return df 

def get_select_unit_item(unit_df, target_name, div_type, sort_type):
    def div_items(txt):
        return [item for item in txt.split(',') if not 'None' in item]    
    
    placement = 8
    if sort_type == '1등':
        placement = 1
    elif sort_type == '순방':
        placement = 4

    if div_type == 'units':
        unit_frist = unit_df[unit_df['placement']<=placement]
        unit_frist['game_time'] = pd.to_datetime(unit_frist['game_time'].apply(unix_to_local))

        unit_frist = unit_frist.groupby(['name','game_time'], as_index=False).agg({'item_1': ','.join, 'item_2' : ','.join, 'item_3' : ','.join})

        unit_frist['items'] = unit_frist['item_1'] + unit_frist['item_2'] + unit_frist['item_3']

        unit_frist = unit_frist[['name','game_time','items']]

        target = unit_frist[unit_frist['name'] == target_name]   
    


        target['items'] = target['items'].apply(div_items)

        item_df = pd.DataFrame()
        for idx, row in target.iterrows():
            tmp = pd.DataFrame(Counter(row['items']), index = [0]).transpose().reset_index()
            tmp.columns = ['items', 'cnt']
            tmp['game_time'] = row['game_time']
            tmp = tmp.set_index('game_time')
            tmp = tmp.sort_values('cnt', ascending=False)[:5]

            item_df = pd.concat([item_df, tmp])
                
        item_df['items'] = item_df.apply(lambda x : eng_to_kor(x['items'], 'items'),axis=1)
    
    elif div_type == 'items':
        unit_frist = unit_df[unit_df['placement']<=placement]
        flag = (unit_frist['item_1'] == target_name) | \
                (unit_frist['item_2'] == target_name) | \
                (unit_frist['item_3'] == target_name)

        item_df = unit_frist[flag]

    return item_df

def groping_item(df):
    def type_set(item_1, item_2, item_3):
        result = []
        if item_1 != 'None':
            result.append(item_1)
        if item_2 != 'None':
            result.append(item_2)
        if item_3 != 'None':
            result.append(item_3)
        return ",".join(list(set(result)))
    # df['items'] = df['item_1'] + df['item_2'] + df['item_3']
    df['items'] = df.apply(lambda x : type_set(x['item_1'], x['item_2'], x['item_3']), axis=1)

    df = df[['name','placement','game_time','items']]

    return df

def make_streamlit_col(champ_cnt):
    if champ_cnt == 1:
        col_1= st.columns(champ_cnt)
        return [col_1]
    if champ_cnt == 2:
        col_1,col_2 = st.columns(champ_cnt)
        return [col_1,col_2]
    if champ_cnt == 3:
        col_1,col_2,col_3 = st.columns(champ_cnt)
        return [col_1,col_2,col_3]
    if champ_cnt == 4:
        col_1,col_2,col_3,col_4 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4]
    if champ_cnt == 5:
        col_1,col_2,col_3,col_4,col_5 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5]
    if champ_cnt == 6:
        col_1,col_2,col_3,col_4,col_5,col_6 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6]
    if champ_cnt == 7:
        col_1,col_2,col_3,col_4,col_5,col_6,col_7 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6, col_7]
    if champ_cnt == 8:
        col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8]
    if champ_cnt == 9:
        col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9]
    if champ_cnt == 10:
        col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10]
    if champ_cnt == 11:
        col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11]
    if champ_cnt == 12:
        col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11,col_12 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11,col_12]
    if champ_cnt == 13:
        col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11,col_12,col_13 = st.columns(champ_cnt)
        return [col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11,col_12,col_13]