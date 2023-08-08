import os
import streamlit as st
import webbrowser
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as pyplot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import json
import time
import datetime

from PIL import Image
import requests
from io import BytesIO

import data_processing as data_p
import draw_plots  as draw_p
import db_connect

traits_list1 = ['공허', '그림자 군도', '녹서스', '다르킨', '데마시아', '방랑자', '슈리마', '아이오니아', '요들', '자운', '타곤', '프렐요드', '필트오버']
traits_list2 = ['구원자', '기원자', '난동꾼', '도전자', '마법사', '발명의 대가', '백발백중', '불한당', '사수', '여제', '연쇄마법사', '요새', '전쟁기계', '책략가', '학살자']
# db_connect.getChallengers()

def eng_to_kor(name, col):
    for data in tft_dict[col]:
        if data['apiName'] == name:
            return data['name']

def kor_to_eng(name, col):
    for data in tft_dict[col]:
        if data['name'] == name:
            return data['apiName']
def kor_to_eng_lst(lst):
    result = []
    for name in lst.split(','):
        result.append(eng_to_kor(name, 'traits'))
    return result

def isLegends(aug):
    result = True if aug in list(legends_augments.keys()) else False
    
    if result:
        return legends_augments[aug]
    else:
        return None

def find_legends_divRow(row):
    def eng_to_kor_aug(name):
        for data in tft_dict['augments']:
            if data['apiName'] == name:
                return data['name']
        
    legends = []

    kor_name = eng_to_kor_aug(row['augment_1'])
    results = isLegends(kor_name)

    if results != None:
        for result in results:
            result = legends_augments['names'][result]
            legends.append(result)
        results = None

    kor_name = eng_to_kor_aug(row['augment_2'])
    results = isLegends(kor_name)

    if results != None:
        for result in results:
            result = legends_augments['names'][result]
            legends.append(result)
        results = None

    kor_name = eng_to_kor_aug(row['augment_3'])
    results = isLegends(kor_name)

    if results != None:
        for result in results:
            result = legends_augments['names'][result]
            legends.append(result)
        results = None

    if len(legends) == 0:
        return None

    return list(set(legends))


style_html = """
<style>
    .row {
    display: -ms-flexbox; 
    display: flex;
    -ms-flex-wrap: wrap; 
    flex-wrap: wrap;
    padding: 0 4px;
    }
    img
    {display: block;width:80%;height:100%;margin: auto;}
</style>
    """

st.set_page_config(
    page_title="KAN_TFT",
    page_icon="✅",
    layout="wide",    
    )

@st.cache_data(show_spinner = ' 사전 데이터 불러오는 중...')
def data_info_load():

    with open('./data/tft_S9_dict.json', 'r') as f:
        tft_dict = json.load(f)

    with open('./img/tft_s9_imgURLs.json', 'r') as f:
        img_urls = json.load(f)

    with open('./img/base_items.json', 'r') as f:
        base_items = json.load(f)

    with open('./img/trait_dict.json', 'r') as f:
        trait_imgs = json.load(f)

    with open('./data/puuid_dict.json', 'r') as f:
        puuid_info = json.load(f)

    with open('./data/tft_S9_legends.json', 'r') as f:
        legends_augments = json.load(f)

    return tft_dict, img_urls, base_items, trait_imgs, puuid_info, legends_augments

tft_dict, img_urls, base_items, trait_imgs, puuid_info, legends_augments = data_info_load()

reverse_trait_imgs = dict()
for key1, value1 in trait_imgs.items():

    if not re.search('[a-zA-Z]+' , key1):
        tmp = {value2 : key2 for key2, value2 in value1.items()}

        reverse_trait_imgs[key1] = tmp

@st.cache_data(show_spinner = '게임 데이터 불러오는 중... 잠시만 기다려주세요.')
def load_data():
    version = 'ver13.13'
    aug_df = data_p.basic_df('augments')
    df = data_p.augment_line_df('all',version)
    df_all = data_p.augment_line_df('all', 'all')
    df_save_rank = data_p.augment_line_df('save_rank',version).reset_index()
    df_winner = data_p.augment_line_df('winner',version).reset_index()

    top5_winner = df_winner.groupby('augments').agg({'cnt' : 'sum'}).sort_values('cnt', ascending=False).reset_index()['augments'].values[:5]
    top5_save = df_save_rank.groupby('augments').agg({'cnt' : 'sum'}).sort_values('cnt', ascending=False).reset_index()['augments'].values[:5]

    df_winner = df_winner.groupby(['game_time','augments']).agg({'cnt' : 'sum', 'total_cnt' : 'sum', 'ratio' : 'mean'}).reset_index()
    df_save_rank = df_save_rank.groupby(['game_time','augments']).agg({'cnt' : 'sum', 'total_cnt' : 'sum', 'ratio' : 'mean'}).reset_index()

    df_winner = df_winner[df_winner['augments'].isin(top5_winner)].reset_index().set_index('game_time')
    df_save_rank = df_save_rank[df_save_rank['augments'].isin(top5_save)].reset_index().set_index('game_time')


    aug_names = list(df.sort_values('augments')['augments'].unique())

    select_augs = []
    for name in aug_names:
        if name:
            modify_name = re.sub('[^가-힣 ]+', '', name).strip()
            
            if modify_name not in select_augs:
                select_augs.append(modify_name)

    # 유닛 데이터 로딩
    unit_df = data_p.units_tier_df()

    unit_names = list(unit_df.sort_values('name')['name'].unique())
    
    select_unit = []
    for name in unit_names:
        if name:
            select_unit.append(name)

    # 특성 데이터 로딩
    traits_df = data_p.traits_tier_df()

    aug_df['isLegends'] = aug_df.apply(lambda x : find_legends_divRow(x), axis=1)
    

    return df, df_all, df_save_rank, df_winner, select_augs, unit_df, select_unit, traits_df, aug_df


aug_df, aug_all_ver, aug_save_rank, aug_winner, select_augs, unit_df, select_unit, traits_df, basic_aug_df = load_data()


def trait_imgs_html(lst):
    # bronze / sliver / gold / chromatic
    def make_trait_html(tier_lst, trait_lst):
        start_html = '<div class="container"><div class="row">'
        end_html = '</div></div>'

        content_html = ''
        for idx in range(len(tier_lst)):
            tier, trait = tier_lst[idx], trait_lst[idx]
            text = f'<div class="col" style="background: url(&quot;//cdn.dak.gg/tft/images2/tft/traits/background/{tier}.svg&quot;) center center / cover no-repeat; width: 36px; height: 36px;" ><img id="img" src="{trait}" class="img-" /></div>'
            content_html += text
        
        return start_html + content_html + end_html

    tier_lst = []
    trait_lst = []
    for div_trait in lst.split(','):
        test_trait, test_tier = div_trait.split('+')
        test_tier = int(test_tier)
        test_tier -= 1
        # if test_trait == '학살자' and test_tier == 4:
        #     test_tier = 5

        if re.search('[a-zA-Z]',test_trait): 
            test_trait = eng_to_kor(test_trait, 'traits')

        lst_tier = list(trait_imgs[test_trait].values())
        tier_lst.append(lst_tier[test_tier])
        trait_lst.append(trait_imgs['img'][test_trait])
    
    txt = make_trait_html(tier_lst, trait_lst)
    return txt

def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="메인메뉴",  
            options=["MAIN", "챌린저 - 증강", "챌린저 - 전설", '챌린저 - 유닛', '챌린저 - 시너지', '커스텀 검색(작업중)','KHAN'],  
            icons=['balloon-heart','clipboard-data-fill', 'controller', 'clipboard-data-fill', 'clipboard-data-fill', 'controller','twitch'],
            menu_icon="file-play",
            default_index=0,
            styles={ "icon": {"color": "red", "font-size": "25px"}, 
                    "nav-link-selected": {"background-color": "#b1c8fa"}}

        )
    return selected

selected = streamlit_menu()

if selected == "MAIN":
    st.markdown("**<p align='center'> <font size = '8'> TFT 통계 </font></p>**", unsafe_allow_html=True)
    st.markdown("**<p align='left'> <font size = '6'> 데이터로 바라보는 TFT </font></p>**", unsafe_allow_html=True)
    ment = """
    컴퓨터 화면에 기준으로 만들었습니다. 모바일에서 보실수 있지만 많이 불편하실거라 컴퓨터로 보시는걸 추천드립니다. \n
    TFT를 직접 플레이 하지 않지만 방장의 TFT를 응원하면서 만들어 봤습니다. 피드백은 언제나 환영입니다!
    """
    st.write(ment)
    

if selected == '챌린저 - 전설':

    div_legend = st.radio('그래프 유형을 선택해주세요.',['전체', '선택' , 'test'])
    versions = ['전체']
    patch_versions = unit_df['game_version'].unique()
    for ver in patch_versions:
        if ver[:5] not in versions:
            versions.append(ver[:5])
    version_type = st.radio('보고 싶은 통계를 선택해주세요. (전체 데이터 선택시 데이터 불러오는데 시간이 약간 소요됩니다.)', versions, horizontal=True)

    if version_type != '전체':
        legend_df = basic_aug_df[basic_aug_df['game_version'] > version_type]
    else:
        legend_df = basic_aug_df.copy()

    if div_legend == '전체':

        def div_legends_row(df):
            # game_time, isLegends, legend_trait
            result_lst = []
            for _, row in df.iterrows():
                for legend in row['isLegends']:
                    result_lst.append(pd.DataFrame({
                        'game_time' : row['game_time'],
                        'isLegends' : legend
                    }, index=[0]))
            return pd.concat(result_lst).reset_index(drop=True)
        
        legend_df = legend_df.dropna(subset=['isLegends'])
        winner_legend = legend_df[legend_df['placement'] == 1]
        rank_save = legend_df[legend_df['placement'] <= 4]

        legend_df = div_legends_row(legend_df)
        winner_legend = div_legends_row(winner_legend)
        rank_save = div_legends_row(rank_save)
        
        legend_df = legend_df.groupby(['game_time', 'isLegends']).size().reset_index().set_index('game_time')
        legend_df = legend_df.rename(columns = {0 : 'cnt'})
        
        
        winner_legend = winner_legend.groupby(['game_time', 'isLegends']).size().reset_index().set_index('game_time')
        winner_legend = winner_legend.rename(columns = {0 : 'cnt'})

        
        rank_save = rank_save.groupby(['game_time', 'isLegends']).size().reset_index().set_index('game_time')
        rank_save = rank_save.rename(columns = {0 : 'cnt'})

        st.plotly_chart(draw_p.legend_trends(legend_df, '1~8등'), use_container_width = True)
        st.plotly_chart(draw_p.legend_trends(winner_legend, '우승(1등)'), use_container_width = True)
        st.plotly_chart(draw_p.legend_trends(rank_save, '순방(1~4등)'), use_container_width = True)
    
    if div_legend == '선택':
        legneds_lst = [legend_name for legend_name in legends_augments['names'].values() if legend_name != None]
        select_legend = st.selectbox('전설을 선택해주세요.', sorted(legneds_lst))

        if '포로' in select_legend:
            st.write('포로는 고유 증강이 없습니다.')
        else:
            target_cnt = dict()
            
            
            # target = basic_aug_df[basic_aug_df['isLegends'] == select_legend]

            def find_legend_trait(row):

                legends = []
                def eng_to_kor_aug(name):
                    for data in tft_dict['augments']:
                        if data['apiName'] == name:
                            return data['name']
                    
                def isLegends(aug):
                    result = True if aug in list(legends_augments.keys()) else False
                    
                    if result:
                        return aug
                    else:
                        return None

                kor_name = eng_to_kor_aug(row['augment_1'])
                result = isLegends(kor_name)

                if result != None:
                    legends.append(result)
                    result = None

                kor_name = eng_to_kor_aug(row['augment_2'])
                result = isLegends(kor_name)

                if result != None:
                    legends.append(result)
                    result = None
                
                kor_name = eng_to_kor_aug(row['augment_3'])
                result = isLegends(kor_name)

                if result != None:
                    legends.append(result)
                    result = None
                
                return legends
            
            def isinRow(row, value):
                if value in row['isLegends']:
                    return True
                else:
                    return False
                
            def div_augs_row(df):
                # game_time, isLegends, legend_trait
                result_lst = []
                for _, row in df.iterrows():
                    for legend in row['legend_trait']:
                        result_lst.append(pd.DataFrame({
                            'game_time' : row['game_time'],
                            'legend_trait' : legend
                        }, index=[0]))
                return pd.concat(result_lst).reset_index(drop=True)
            
            target = legend_df.dropna(subset=['isLegends'])
            winner_legend = target[target['placement'] == 1]

            flag = target.apply(lambda x : isinRow(x, select_legend), axis=1)
            target = target[flag]

            flag = winner_legend.apply(lambda x : isinRow(x, select_legend), axis=1)
            winner_legend = winner_legend[flag]
            
            target['legend_trait'] = target.apply(lambda x : find_legend_trait(x), axis=1)
            target = div_augs_row(target)

            winner_legend['legend_trait'] = winner_legend.apply(lambda x : find_legend_trait(x), axis=1)
            winner_legend = div_augs_row(winner_legend)
            
            legend_df = target.groupby(['game_time', 'legend_trait']).size().reset_index().set_index('game_time')
            legend_df = legend_df.rename(columns = {0 : 'cnt', 'legend_trait' : 'isLegends'})        

            winner_legend = winner_legend.groupby(['game_time', 'legend_trait']).size().reset_index().set_index('game_time')
            winner_legend = winner_legend.rename(columns = {0 : 'cnt', 'legend_trait' : 'isLegends'})

            def is_target_traits(tarit, target):
                reverse_dict = {value : key for key, value in legends_augments['names'].items()}
                if reverse_dict[target] in legends_augments[tarit['isLegends']]:
                    return True
                else:
                    return False
            
            target_filter = legend_df.apply(lambda x : is_target_traits(x, select_legend), axis=1)
            legend_df = legend_df[target_filter]

            target_filter = winner_legend.apply(lambda x : is_target_traits(x, select_legend), axis=1)
            winner_legend = winner_legend[target_filter]        
            
            st.plotly_chart(draw_p.legend_trends(legend_df, '1~8등'), use_container_width = True)
            st.plotly_chart(draw_p.legend_trends(winner_legend, '우승(1등)'), use_container_width = True)
    

if selected == '챌린저 - 증강':
    
    st.markdown("**<p align='center'> <font size = '8'> TFT 챌린저 통계(증강) </font></p>**", unsafe_allow_html=True)
    st.markdown("**<p align='LEFT'> <font size = '6'> 시간별 인기 증강 </font></p>**", unsafe_allow_html=True)
    show_type = st.radio('통계 기준', ['전체', '선택'], horizontal=True)
    date_type = st.radio('기간 설정 (전체 선택시 로딩 시간이 있습니다.)', ['최근 3일', '전체'], horizontal=True)

    if date_type == '최근 3일':
        result  = datetime.datetime.now()
        result = result - pd.to_timedelta('3d')
        before_5day = str(result.year)+'-'+str(result.month)+'-'+str(result.day)
        aug_dfs = aug_df[aug_df.index >= before_5day]
        aug_all_ver_df = aug_all_ver[aug_all_ver.index >= before_5day]
        aug_save_rank_df = aug_save_rank[aug_save_rank.index >= before_5day]
        aug_winner_df = aug_winner[aug_winner.index >= before_5day]

    else:
        aug_dfs = aug_df.copy()
        aug_all_ver_df = aug_all_ver.copy()
        aug_save_rank_df = aug_save_rank.copy()
        aug_winner_df = aug_winner.copy()

    if show_type == '전체':
        st.write('모든 증강의 시간대별 선택 현황을 보여드립니다.(드래그를 통해 확대 가능합니다.)')
        st.plotly_chart(draw_p.draw_linePlot(aug_dfs, 'augments'),use_container_width = True)

    elif show_type == '선택':
        select_aug = st.selectbox('선택한 증강의 모든 티어 데이터를 보여드립니다.', select_augs)

        select_df = aug_all_ver_df.dropna(subset=['augments'])
        select_df = select_df[select_df['augments'].str.contains(select_aug)].sort_index()
        
        st.plotly_chart(draw_p.draw_linePlot(select_df, 'augments', raw_df = aug_all_ver_df),use_container_width = True)
        # st.dataframe(select_df.rename(columns = {'cnt' : '선택수', 'match_cnt' : '진행 게임수'}) ,use_container_width = True)
 

    st.markdown("**<p align='LEFT'> <font size = '6'> 증강 순방률 </font></p>**", unsafe_allow_html=True)
    st.write('선택수가 높은 상위 5개 증강을 보여줍니다.')

    st.plotly_chart(draw_p.draw_save_linePlot(aug_save_rank_df, 'augments', 'save_rank'),use_container_width = True)
    

    st.markdown("**<p align='LEFT'> <font size = '6'> 증강 승률 </font></p>**", unsafe_allow_html=True)
    st.write('선택수가 높은 상위 5개 증강을 보여줍니다.')
    st.plotly_chart(draw_p.draw_save_linePlot(aug_winner_df, 'augments', 'winner'),use_container_width = True)
    


if selected == '챌린저 - 유닛':
    st.markdown("**<p align='center'> <font size = '8'> TFT 챌린저 통계(유닛 or 아이템) </font></p>**", unsafe_allow_html=True)
    st.write(f" **<p align='LEFT'> <font size = '3' color = 'red'> !! 라이즈에 대한 통계가 포함되어 있긴하나 라이즈가 게임에서 선택된 차원문에 따라 각각 다른 유닛으로 인식되어 라이즈를 기준으로 데이터를 분리하는데 문제가 있어 현재 목록에서 빠져있습니다. </font></p>** ", unsafe_allow_html=True)
    show_type = st.radio('기준을 선택해주세요. ', ['유닛', '아이템'], horizontal=True)
    patch_versions = unit_df['game_version'].unique()
    versions = ['전체']
    for ver in patch_versions:
        if ver[:5] not in versions:
            versions.append(ver[:5])
    version_type = st.radio('보고 싶은 통계를 선택해주세요. (전체 데이터 선택시 데이터 불러오는데 시간이 약간 소요됩니다.)', versions, horizontal=True)
    sort_type = st.radio('보고 싶은 통계를 선택해주세요. (전체 데이터 선택시 데이터 불러오는데 시간이 약간 소요됩니다.)', ['1등', '순방', '전체'], horizontal=True)

    if version_type != '전체':
        unit_item_df = unit_df[unit_df['game_version'].str.contains(version_type)]
    else:
        unit_item_df = unit_df.copy()

    st.markdown(f"**<p align='LEFT'> <font size = '6'> {show_type} 통계 </font></p>**", unsafe_allow_html=True)

    select_unit_kor = []
    # print(select_unit)
    for name in select_unit:
        kor_name = eng_to_kor(name,'units')
        if kor_name == None : continue
        if kor_name == 'T-헥스' or kor_name == '라이즈': continue
        select_unit_kor.append(kor_name)

    if show_type == '유닛':

        selectbox_unit = st.selectbox('유닛을 선택해주세요.', sorted(select_unit_kor))
        item_df = data_p.get_select_unit_item(unit_item_df, kor_to_eng(selectbox_unit, 'units'), 'units', sort_type)

        top10_item = item_df.groupby('items')[['cnt']].sum().sort_values('cnt', ascending=False).reset_index()[:5]
        top10_item.rename(columns = {'items' : '아이템', 'cnt' : '사용 횟수'}, inplace=True)

        st.markdown(f"**<p align='LEFT'> <font size = '6'> {selectbox_unit} 추천 아이템(사용수) </font></p>**", unsafe_allow_html=True)
        if len(top10_item):
            recommand_1, recommand_2, recommand_3, recommand_4, recommand_5 = st.columns(5)

            with recommand_1 : st.write('추천 1')
            with recommand_2 : st.write('추천 2')
            with recommand_3 : st.write('추천 3')
            with recommand_4 : st.write('추천 4')
            with recommand_5 : st.write('추천 5')
        
            img_lst = []
            name_lst = []
            for _, row in top10_item.reset_index()[:5].iterrows():    
                tmp = []
                name_tmp = []
                
                img_url = img_urls[row['아이템']]
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))

                img_lst.append(img)
                name_lst.append(row['아이템'] + '(' + str(int(row["사용 횟수"])) + ')')
            img_1, img_2, img_3, img_4, img_5 = st.columns(5)

            cols = [img_1,img_2,img_3,img_4,img_5]

            for idx in range(len(img_lst)):
                with cols[idx] : st.image(img_lst[idx], width = 80, caption = name_lst[idx])

        # st.dataframe(top10_item.set_index('아이템'), use_container_width = True)
        st.plotly_chart(draw_p.draw_line_unit(item_df[item_df['items'].isin(top10_item['아이템'].unique())], 'items', mode='lines'),use_container_width = True)
    
    if show_type =='아이템':
        st.write(f" 완성 아이템의 조합 통계를 보여드립니다. (조합의 사용 횟수가 5m회 이상인 통계만 보여드립니다.) ", unsafe_allow_html=True)
        tmp = list(set(list(unit_item_df['item_1'].values) + list(unit_item_df['item_2'].values) + list(unit_item_df['item_3'].values)))
        select_item_kor = []
        for name in tmp:
            kor_name = eng_to_kor(name,'items')
            if kor_name == None : continue
            if kor_name in base_items.keys() : continue
            if '<br>' in kor_name : 
                # print(kor_name)
                kor_name = re.sub('(<br>)' ,'', kor_name) 
                # print(kor_name)
            select_item_kor.append(kor_name)

        select_col_1, select_col_2 = st.columns(2)
        with select_col_1:
            selectbox_item = st.selectbox('아이템을 선택해주세요.', sorted(select_item_kor))
        with select_col_2:
            selectbox_unit = st.selectbox('챔피언을 선택해주세요.', ['전체'] + sorted(select_unit_kor))

        item_df = data_p.get_select_unit_item(unit_item_df, kor_to_eng(selectbox_item, 'items'), 'items' , sort_type)
        
        if selectbox_unit != '전체':
            item_df = item_df[item_df['name'] == (kor_to_eng(selectbox_unit, 'units'))]

        items_cnt = dict()
        check_lst = []
        cnt_lst = [0 for _ in range(200)]

        if selectbox_unit != '전체':
            for _, row in item_df.iterrows():
                item_1, item_2, item_3 = row['item_1'], row['item_2'], row['item_3']

                flag = ((item_df['item_1'] == item_1) | (item_df['item_2'] == item_1) | (item_df['item_3'] == item_1)) & \
                        ((item_df['item_1'] == item_2) | (item_df['item_2'] == item_2) | (item_df['item_3'] == item_2)) & \
                        (item_df['item_1'] == item_3) | (item_df['item_2'] == item_3) | (item_df['item_3'] == item_3)
                
                # cnt = len(item_df[flag])
                
                item_compos = set([item_1, item_2, item_3])
                if item_compos not in check_lst:
                    check_lst.append(item_compos)
                else:
                    cnt_lst[check_lst.index(item_compos)] +=1
            # break
        
        def kor_to_eng_lst(lst):
            result = []
            for name in lst.split(','):
                result.append(eng_to_kor(name, 'items'))
            return result
        
        common_items = data_p.groping_item(item_df).groupby(['items'], as_index=False).agg({'game_time' : 'size', 'placement' : 'mean'}).round(2)
        common_items.rename(columns = {'items' : '아이템 조합', 'game_time' : '횟수', 'placement' : '평균등수'}, inplace=True)
        
        common_items['아이템 조합'] = common_items['아이템 조합'].apply(kor_to_eng_lst)
        common_items = common_items[common_items['횟수'] > 4].set_index('아이템 조합').sort_values('횟수', ascending=False)
        st.write(f" **<p align='LEFT'> <font size = '2' color = 'gray'> 추천 기준 : 횟수(50%), 등수(50%) </font></p>** ", unsafe_allow_html=True)
        # st.dataframe(recommand_df)    
        if len(common_items):
            recommand_df = common_items.copy()
            max_cnt = max(recommand_df['횟수'])
            min_cnt = min(recommand_df['횟수'])
            recommand_df['ratio'] = (recommand_df['횟수']/(max_cnt + min_cnt)) * 0.5 + (1 - recommand_df['평균등수'] * 0.5)  
        
            recommand_1, recommand_2, recommand_3, recommand_4, recommand_5 = st.columns(5)

            with recommand_1 : st.write('추천 1')
            with recommand_2 : st.write('추천 2')
            with recommand_3 : st.write('추천 3')
            with recommand_4 : st.write('추천 4')
            with recommand_5 : st.write('추천 5')
        
            img_lst = []
            name_lst = []
            for _, row in recommand_df.sort_values('ratio' ,ascending=False).reset_index()[:5].iterrows():    
                tmp = []
                name_tmp = []
                for name in row['아이템 조합']:
                    img_url = img_urls[name]
                    response = requests.get(img_url)
                    img = Image.open(BytesIO(response.content))
                    tmp.append(img)
                    name_tmp.append(name)
                img_lst.append(tmp)
                name_lst.append(name_tmp)
            img_1, img_2, img_3, img_4, img_5 = st.columns(5)

            cols = [img_1,img_2,img_3,img_4,img_5]

            for idx in range(len(img_lst)):
                with cols[idx] : st.image(img_lst[idx], width = 50, caption = name_lst[idx])
        

        st.dataframe(common_items,use_container_width = True)

        # st.dataframe(unit_df)


        # st.write(f" 이미지 구현은 아직 작업중입니다. (_._) ", unsafe_allow_html=True)

        
        
def most_traits_trend(df):
    target = df[df['placement']==1].drop_duplicates(subset=['match_id','name'])
    target = target[target['tier_current'] > 0]
    div_dates = []
    now = datetime.datetime.now()
    for date_diff in range(1,6):
    
        
        tmp_day = now - pd.to_timedelta(f'{str(date_diff)}d')
        target_day = str(tmp_day.year)+'-'+str(tmp_day.month)+'-'+str(tmp_day.day)

        if date_diff == 1:
            before_day = str(tmp_day.year)+'-'+str(tmp_day.month)+'-'+str(tmp_day.day+1)
    
        target['local_time'] = pd.to_datetime(target['game_time'].apply(data_p.unix_to_local))    
        target = target.set_index('local_time')
        if date_diff == 1:
            flag = (target.index > target_day) 
        else:
            flag = (target.index > target_day) & (target.index < before_day)
        tmp = target[flag]
        tmp = tmp.sort_values(['game_time','tier_current', 'tier_total'], ascending=[False, False, True])

        tmp['name'] = tmp['name'].apply(kor_to_eng_lst)

        tmp['tier_current'] = tmp['tier_current'].astype(str)

        game_ids = tmp['match_id'].unique()
        
        trait_cnt = []
        for game_id in game_ids:
            div_df = tmp[tmp['match_id'] == game_id]

            trait = []
            for _, row in div_df.iterrows():
                txt = row['name'][0] + '+' + str(row['tier_current'])
                trait.append(txt)
            sorted(trait)

            trait_cnt.append(",".join(trait))
        
        from collections import Counter
        tt = Counter(trait_cnt).most_common(5)
        div_date_df = pd.DataFrame(tt)
        div_date_df['date'] = before_day
        div_dates.append(div_date_df)
        before_day = target_day
    return pd.concat(div_dates).set_index('date')

if selected == '챌린저 - 시너지':
    st.markdown("**<p align='center'> <font size = '8'> TFT 챌린저 통계(시너지) </font></p>**", unsafe_allow_html=True)
    
    
    page_type = st.radio('추천', ['추천 데이터(MAIN)', '세부 추천'])

    if page_type == '추천 데이터(MAIN)':
        st.markdown("**<p align='left'> <font size = '5'> 최근 5일간의 우승(1등) 조합 추이 </font></p>**", unsafe_allow_html=True)
        trend_df = most_traits_trend(traits_df)
        trend_df = trend_df.rename(columns = {0 : '시너지', 1:'우승 횟수'})

        
        st.plotly_chart(draw_p.draw_trend_df(trend_df),use_container_width = True)
        st.dataframe(trend_df,use_container_width = True)

    elif page_type == '세부 추천':

        date_type = st.radio('데이터 기준을 선택해주세요.', ['패치버전', '날짜'], horizontal=True)

        if date_type == '패치버전':
            g_version = st.radio('게임 버전을 선택해주세요.', list(traits_df['game_version'].unique()), horizontal=True)

        if date_type == '날짜':
            date_diff = st.radio('몇일전 데이터까지 보시겠습니까?', [1,2,3,4,5], horizontal=True)
        
        target = traits_df[traits_df['placement']==1].drop_duplicates(subset=['match_id','name'])
        target = target[target['tier_current'] > 0]

        if date_type == '패치버전':
            target = target[target['game_version'] == g_version]
        elif date_type == '날짜':
            now = datetime.datetime.now()
            tmp_day = now - pd.to_timedelta(f'{str(date_diff)}d')
            before_5day = str(tmp_day.year)+'-'+str(tmp_day.month)+'-'+str(tmp_day.day)
            
            
            target['local_time'] = pd.to_datetime(target['game_time'].apply(data_p.unix_to_local))    
            target = target[target.set_index('local_time').index > before_5day]

        target = target.sort_values(['game_time','tier_current', 'tier_total'], ascending=[False, False, True])

        
        target['name'] = target['name'].apply(kor_to_eng_lst)

        target['tier_current'] = target['tier_current'].astype(str)

        game_ids = target['match_id'].unique()
        
        
        trait_cnt = []
        main_traits = []
        for game_id in game_ids:
            tmp = target[target['match_id'] == game_id]

            trait = []
            for _, row in tmp.iterrows():
                txt = row['name'][0] + '+' + str(row['tier_current'])
                trait.append(txt)
            sorted(trait)

            trait_cnt.append(",".join(trait))
            main_traits.append(trait[0])
        
        from collections import Counter
        tt = Counter(trait_cnt).most_common(3)

        st.write(style_html, unsafe_allow_html=True)
        
        t_lst = []
        cnt_lst = []
        for key, value in Counter(main_traits).items():
            t_lst.append(key)
            cnt_lst.append(value)
        winners = pd.DataFrame({'trait' : t_lst, 'cnt' :cnt_lst})
        st.write(winners)
        st.write((winners['cnt'].sum()))
        rec_trait_1,rec_trait_2,rec_trait_3 = st.columns(3)
        trait_col_1,trait_col_2,trait_col_3 = st.columns(3)

        rec_cols = [rec_trait_1,rec_trait_2,rec_trait_3]
        trait_cols = [trait_col_1,trait_col_2,trait_col_3]

        for idx, col in enumerate(rec_cols):
            with col : 
                st.write(f'추천 {idx+1}' + f" \n **<p align='left'> <font size = '2'>  {re.sub(',', ', ', tt[idx][0])} </font></p>**", unsafe_allow_html=True)
                
        for most_traits, t_cols in zip(tt, trait_cols):
            with t_cols:
                st.write(trait_imgs_html(most_traits[0]), unsafe_allow_html=True)

        player_1,player_2,player_3,player_4,player_5 = st.columns(5)

        player_cols = [player_1,player_2,player_3,player_4,player_5]

        st.write("**<p align='left'> <font size = '6'>  최근 5게임 </font></p>**", unsafe_allow_html=True)
        select_rec_game = st.radio('', ['추천1','추천2','추천3'], horizontal=True)

        if select_rec_game == '추천1':
            show_traits = tt[0][0]
        elif select_rec_game == '추천2':
            show_traits = tt[1][0]
        elif select_rec_game == '추천3':
            show_traits = tt[2][0]

        tmp_traits = []
        tmp_tiers = []
        for txt in show_traits.split(','):
            tmp_trait, tmp_tier = txt.split('+')
            tmp_traits.append(tmp_trait.strip())
            tmp_tiers.append(tmp_tier)

        
        filter_df = target.groupby(['game_time', 'match_id','puuid'], as_index=False).agg({'name': 'sum', 'tier_current' : ','.join})
        filter_df = filter_df.reset_index().sort_values('game_time', ascending=False)
        flag = (filter_df['name'].isin([tmp_traits])) & (filter_df['tier_current'] == (','.join(tmp_tiers)))

        st.write("**<p align='left'> <font size = '3'>  사용 챔피언, 아이템 </font></p>**", unsafe_allow_html=True)
        for p_idx, row in filter_df[flag][:5].reset_index(drop=True).iterrows():
            
            game_time = row['game_time']/1000
            game_time = time.strftime('%Y-%m-%d %H:%M:00', time.localtime(game_time))
            nickname = puuid_info[row['puuid']] if row['puuid'] in puuid_info.keys() else ''
            # nickname = re.sub(' ', '%20', nickname)
            game_name = row['match_id']
            url = f'https://tactics.tools/player/kr/{re.sub(" ", "%20", nickname)}/{game_name}'
            st.write(f"**<p align='left'> <font size = '2'> {nickname} - {game_time}  [게임 정보]({url})</font></p>**", unsafe_allow_html=True)

            unit_query = f'select * from match_detail_units where match_id = "{row["match_id"]}" and puuid = "{row["puuid"]}";'
            trait_query = f'select * from match_detail_traits where match_id = "{row["match_id"]}" and puuid = "{row["puuid"]}" and tier_current > 0;'
            aug_query = f'select * from match_basic_info where match_id = "{row["match_id"]}" and puuid = "{row["puuid"]}";'

            
            # detail_unit_df = db_connect.getDataSQL(unit_query)
            # detail_trait_df = db_connect.getDataSQL(trait_query).sort_values(['tier_current', 'tier_total'], ascending=[False, True])
            detail_aug_df = db_connect.getDataSQL(aug_query)
            

            unit_flag = (unit_df['match_id'] == row['match_id']) & (unit_df['puuid'] == row['puuid'])
            trait_flag = (traits_df['match_id'] == row['match_id']) & (traits_df['puuid'] == row['puuid'])
            detail_unit_df = (unit_df[unit_flag].reset_index(drop=True))
            detail_trait_df = (traits_df[trait_flag].reset_index(drop=True))
            detail_trait_df = detail_trait_df[detail_trait_df['tier_current']>0]
            
            # st.dataframe(detail_unit_df)
            # st.dataframe(detail_trait_df)

            trait_txt = ''
            for _, row in detail_trait_df.iterrows():
                trait_txt = trait_txt + eng_to_kor(row['name'], 'traits') + '+' + str(row['tier_current']) + ','
            trait_txt = trait_txt[:-1]

            aug_imgs = []
            legend_champ = ''
            for _, row in detail_aug_df.iterrows():
                if row['augment_1'] != 'None':
                    tmp_aug1 = eng_to_kor(row['augment_1'], 'augments')
                    aug_imgs.append(trait_imgs['augments'][tmp_aug1])
                    if legend_champ == '' :
                        if tmp_aug1 in trait_imgs['legend_augments'].keys():
                            legend_champ = trait_imgs['legend_augments'][tmp_aug1]
                if row['augment_2'] != 'None':
                    tmp_aug2 = eng_to_kor(row['augment_2'], 'augments')
                    aug_imgs.append(trait_imgs['augments'][tmp_aug2])
                    if legend_champ == '' :
                        if tmp_aug2 in trait_imgs['legend_augments'].keys():
                            legend_champ = trait_imgs['legend_augments'][tmp_aug2]
                if row['augment_3'] != 'None':
                    tmp_aug3 = eng_to_kor(row['augment_3'], 'augments')
                    aug_imgs.append(trait_imgs['augments'][tmp_aug3])
                    if legend_champ == '' :
                        if tmp_aug3 in trait_imgs['legend_augments'].keys():
                            legend_champ = trait_imgs['legend_augments'][tmp_aug3]

            
            champ_cols = data_p.make_streamlit_col(len(detail_unit_df['name'])+2)
            
            with player_cols[p_idx]:
                with champ_cols[0] : #시너지
                    st.write(trait_imgs_html(trait_txt), unsafe_allow_html=True)
                
                with champ_cols[1] : #증강
                    st.image(aug_imgs, width = 30)
                    st.write(f"**<p align='left'> <font size = '2'> {legend_champ} </font></p>**", unsafe_allow_html=True)

                for idx, row in detail_unit_df.iterrows():
                    with champ_cols[idx+2]:
                        if re.search('[a-zA-Z]+', row['item_1']):
                            img_url = trait_imgs['champ'][eng_to_kor(row['name'], 'units')]
                        else:
                            img_url = trait_imgs['champ'][row['name']]
                        response = requests.get('http:' + img_url)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, width=60)
                        
                        img_lst = []
                        if row['item_1'] != 'None':
                            if re.search('[a-zA-Z]+', row['item_1']):
                                # print(row['item_1'])
                                img_url = img_urls[eng_to_kor(row['item_1'], 'items')]
                            else:
                                img_url = img_urls[row['item_1']]
                            response = requests.get(img_url)
                            img = Image.open(BytesIO(response.content))
                            img_lst.append(img)
                        if (row['item_2'] != 'None'):
                            if (row['item_2'] != 'TFT_Item_EmptyBag'): 
                                if re.search('[a-zA-Z]+', row['item_2']):
                                    img_url = img_urls[eng_to_kor(row['item_2'], 'items')]
                                else:
                                    img_url = img_urls[row['item_2']]
                                response = requests.get(img_url)
                                img = Image.open(BytesIO(response.content))
                                img_lst.append(img)
                        if (row['item_3'] != 'None'):
                            if (row['item_3'] != 'TFT_Item_EmptyBag'):
                                if re.search('[a-zA-Z]+', row['item_3']):
                                    img_url = img_urls[eng_to_kor(row['item_3'], 'items')]
                                else:
                                    img_url = img_urls[row['item_3']]
                                response = requests.get(img_url)
                                img = Image.open(BytesIO(response.content))
                                img_lst.append(img)
                        st.image(img_lst, width = 20)
                
                        # break
            # break
        # st.dataframe(tmp_df)
                        
        
        
    
    # st.dataframe(tmp[['name', 'num_units', 'tier_current', 'tier_total']].sort_values('tier_current', ascending=False))

if selected == '커스텀 검색(작업중)':
    st.markdown("**<p align='center'> <font size = '8'> TFT 챌린저 통계(커스텀 검색) </font></p>**", unsafe_allow_html=True)
    standard_type = st.radio('추천 기준을 선택해주세요. (시너지 통계는 우승(1등) 통계 기준으로 추천드립니다.)', ['증강', '시너지', '챔피언'], horizontal=True)
    if standard_type == '챔피언':
        # sort_type = st.radio('보고 싶은 통계를 선택해주세요. (전체 데이터 선택시 데이터 불러오는데 시간이 약간 소요됩니다.)', ['1등', '순방', '전체'], horizontal=True)
        select_unit_kor = []
        
        for name in select_unit:
            kor_name = eng_to_kor(name,'units')
            if kor_name == None : continue
            if kor_name == 'T-헥스' or kor_name == '라이즈': continue
            select_unit_kor.append(kor_name)

        select_champ_col1, select_champ_col2 = st.columns(2)
        with select_champ_col1:
            select_champ = st.selectbox('챔피언을 선택해주세요.', sorted(select_unit_kor))
        with select_champ_col2:
            select_champ_tier = st.selectbox('챔피언 티어(성)를 선택해주세요', ['전체',1,2,3])

        target_name = kor_to_eng(select_champ, 'units')

        unit_winner = unit_df[unit_df['placement']==1]
        if select_champ_tier != '전체':
            flag = (unit_winner['name'] == target_name) & (unit_winner['tier'] == select_champ_tier)
        else:
            flag = (unit_winner['name'] == target_name)
        st.dataframe(unit_winner[flag][:5])
    if standard_type == '증강':
        sort_type = st.radio('보고 싶은 통계를 선택해주세요. (전체 데이터 선택시 데이터 불러오는데 시간이 약간 소요됩니다.)', ['1등', '순방', '전체'], horizontal=True)

        if sort_type == '1등':
            search_placement = ' = 1'
        elif sort_type == '순방':
            search_placement = ' < 5'
        else:
            search_placement = ' < 9'

        aug_lst1 = list(trait_imgs['augments'].keys())
        aug_lst2 = list(trait_imgs['augments'].keys())
        aug_lst3 = list(trait_imgs['augments'].keys())

        select_col1,select_col2,select_col3 = st.columns(3)

        with select_col1:
            aug1_selected = st.selectbox('첫 증강을 선택해주세요.', aug_lst1)
            aug_lst2.remove(aug1_selected)
            aug_lst3.remove(aug1_selected)

        with select_col2:
            aug2_selected = st.selectbox('두번째 증강을 선택해주세요.', ['전체'] + aug_lst2)
            if aug2_selected != '전체' : 
                aug_lst3.remove(aug2_selected)

        with select_col3:
            aug3_selected = st.selectbox('세번째 증강을 선택해주세요.', ['전체'] + aug_lst3)

        search_aug1 = kor_to_eng(aug1_selected, 'augments')

        sub_query1 = 'select * from match_table where game_version = "13.13.518.0539"'
        aug_query = f'select mbi.match_id, puuid, augment_1, augment_2, augment_3 from match_basic_info mbi join ({sub_query1}) mt on mbi.match_id = mt.match_id where placement {search_placement}'
        where_query1 = f' and (augment_1 = "{search_aug1}" or augment_2 = "{search_aug1}" or augment_3 = "{search_aug1}")'
        aug_query = aug_query + where_query1

        if aug2_selected != '전체':
            search_aug2 = kor_to_eng(aug2_selected, 'augments')
            where_query2 = f' and (augment_1 = "{search_aug2}" or augment_2 = "{search_aug2}" or augment_3 = "{search_aug2}")'
            aug_query = aug_query + where_query2
    
        if aug3_selected != '전체':
            search_aug3 = kor_to_eng(aug3_selected, 'augments')
            where_query3 = f' and (augment_1 = "{search_aug3}" or augment_2 = "{search_aug3}" or augment_3 = "{search_aug3}")'
            aug_query = aug_query + where_query3
        

        custom_aug_df = db_connect.getDataSQL(aug_query)

        if len(custom_aug_df) != 0:
            st.dataframe(custom_aug_df)
        else:
            st.write('선택한 증강의 통계 데이터가 없습니다 ㅠ_ㅠ')

        


    if standard_type == '시너지':

        date_type = st.radio('데이터 기준을 선택해주세요.', ['패치버전', '날짜'], horizontal=True)

        if date_type == '패치버전':
            g_version = st.radio('게임 버전을 선택해주세요.', list(traits_df['game_version'].unique()), horizontal=True)

        if date_type == '날짜':
            date_diff = st.radio('몇일전 데이터까지 보시겠습니까?', [1,2,3,4,5], horizontal=True)


        main_trait_col, sub_trait_col = st.columns(2)

        main_trait_lst = [key for key in trait_imgs.keys() if not re.search('[a-zA-Z]+', key)]
        sub_trait_lst = [key for key in trait_imgs.keys() if not re.search('[a-zA-Z]+', key)]

        with main_trait_col:
            main_trait = st.selectbox('메인 시너지를 선택해주세요. (전체 데이터 선택시 데이터 로딩 시간이 있습니다.)',  main_trait_lst + ['전체'])

        if main_trait != '전체':
            trait_tiers = list(trait_imgs[main_trait].values())
            with sub_trait_col:
                trait_tier = st.selectbox('시너지 티어를 선택해주세요.', set(trait_tiers))

        
            search_tier = int(reverse_trait_imgs[main_trait][trait_tier])
            main_trait  = kor_to_eng(main_trait, 'traits')

        target = traits_df[traits_df['placement']==1].drop_duplicates(subset=['match_id','name'])
        target = target[target['tier_current'] > 0]
        if date_type == '패치버전':
            target = target[target['game_version'] == g_version]
        elif date_type == '날짜':
            now = datetime.datetime.now()
            tmp_day = now - pd.to_timedelta(f'{str(date_diff)}d')
            before_day = str(tmp_day.year)+'-'+str(tmp_day.month)+'-'+str(tmp_day.day)
            
            
            target['game_time'] = pd.to_datetime(target['game_time'].apply(data_p.unix_to_local))    
            target = target[target.set_index('game_time').index > before_day]
        
        # st.dataframe(target)
        if main_trait != '전체':
            flag = (target['name'] == main_trait) & (target['num_units'] >= search_tier)
            target_match_id = target[flag]['match_id'].values
            target = target[target['match_id'].isin(target_match_id)]
        target = target.sort_values(['game_time','tier_current', 'tier_total'], ascending=[False, False, True])

        def eng_to_kor_lst(name):
            
            return eng_to_kor(name, 'traits')
        
        target['name'] = target['name'].apply(eng_to_kor_lst, 'traits')

        
        game_ids = target['match_id'].unique()
        trait_cnt = []
        for game_id in game_ids:
            tmp = target[target['match_id'] == game_id]

            trait = []
            for _, row in tmp.iterrows():
                txt = row['name'] + '+' + str(row['tier_current'])
                trait.append(txt)
            sorted(trait)

            trait_cnt.append(",".join(trait))
        
        
        from collections import Counter
        counters = Counter(trait_cnt)
        tt = counters.most_common(5)
        
        st.write(style_html, unsafe_allow_html=True)

        rec_cols = data_p.make_streamlit_col(len(tt))
        trait_cols = data_p.make_streamlit_col(len(tt))

        for idx, col in enumerate(rec_cols):
            with col : 
                st.write(f'추천 {idx+1}' + f" \n **<p align='left'> <font size = '2'>  {re.sub(',', ', ', tt[idx][0])} </font></p>**", unsafe_allow_html=True)
                
        for most_traits, t_cols in zip(tt, trait_cols):
            with t_cols:
                st.write(trait_imgs_html(most_traits[0]), unsafe_allow_html=True)

        st.dataframe(pd.DataFrame({
            '조합' : list(counters.keys()),
            '우승 횟수' : list(counters.values())
        }).sort_values('우승 횟수', ascending=False).set_index('조합'),use_container_width = True)
        
        
if selected == '스트리머 통계':

    st.markdown("**<p align='center'> <font size = '8'> TFT 스트리머 통계 </font></p>**", unsafe_allow_html=True)


    title = """
<div class=&quot;p-2 text-left font-size-12&quot;>
<div class=&quot;mb-2&quot;>
필트오버
</div>  
<div class=&quot;text-gray&quot;>
<div class=&quot;text-mint&quot;>
(3) T-헥스 획득
</div>
<div class=&quot;&quot;>
(6) 매 라운드 추가 전리품 획득. 패배 시 2패로 간주
</div>
</div>
</div>
"""

    txt = """
<style>
.tooltip {
position: relative;
display: block;
}

.tooltip .tooltiptext {
visibility: hidden;      
width: 200px;            
background-color: black;
color: #fff;
text-align: center;
border-radius: 6px;
padding: 5px 0;

position: absolute;      
z-index: 1;
}

.tooltip:hover .tooltiptext {
visibility: visible;     
}
</style>

<div class="tooltip">Hover Me (LEFT)
"""
    txt = txt + f'<span class="tooltiptext tooltip-left" title={title}>왼쪽 툴팁</span> </div>'


    st.write(txt, unsafe_allow_html=True)


def get_s_names():
    json_path = '/Users/seokholee/lsh/Project/TFT_S9/data/streamer/puuids.json'
    with open(json_path, 'r') as f:
        s_puuids = json.load(f)
    
    s_names = list(s_puuids.keys())
    return s_names

def dsk_data(s_name):    

    path = '/Users/seokholee/lsh/Project/TFT_S9/data/streamer/'
    df_games = pd.read_csv(path + f'df_games_{s_name}.csv')
    df_traits = pd.read_csv(path + f'df_traits_{s_name}.csv')
    df_units = pd.read_csv(path + f'df_units_{s_name}.csv')

    return df_games, df_traits, df_units



if selected =='KHAN':
    s_names = get_s_names()
    
    s_name = st.radio('스트리머를 선택해주세요.', s_names, horizontal=True)
    dsk_games, dsk_traits, dsk_units = dsk_data(s_name)

    def change_time(t):

        m = int(t//60)
        s = int(t%60)
        result = str(m) + '분 ' + str(s) + '초'
        return result

    dsk_games['game_datetime'] = pd.to_datetime(dsk_games['game_datetime'].apply(data_p.unix_to_local))    
    dsk_games['죽은시간'] = dsk_games['time_eliminated'].apply(change_time)

    st.write(s_name + ' DATA!!')
    st.write(dsk_games['placement'].value_counts())
    st.write(dsk_games['placement'].value_counts().sum())
    draw_df = pd.DataFrame(dsk_games['placement'].value_counts())
    st.plotly_chart(draw_p.streamer_chart(draw_df))

    dsk_traits['name'] = dsk_traits.apply(lambda x : eng_to_kor(x['name'], 'traits'), axis=1)
    # st.dataframe(dsk_traits)
    s_traits = dsk_traits[dsk_traits['style']>=3].groupby('name').size().reset_index()
    s_traits1 = s_traits[s_traits['name'].isin(traits_list1)]
    s_traits2 = s_traits[s_traits['name'].isin(traits_list2)]
    s_traits1.set_index('name', inplace=True)
    s_traits2.set_index('name', inplace=True)
    
    s_traits1.rename(columns = {0 : 'cnt'}, inplace=True)
    s_traits2.rename(columns = {0 : 'cnt'}, inplace=True)
    
    st.plotly_chart(draw_p.streamer_chart_traits(s_traits1.sort_values('cnt', ascending=False)), use_container_width = True)
    st.plotly_chart(draw_p.streamer_chart_traits(s_traits2.sort_values('cnt', ascending=False)), use_container_width = True)

    dsk_units['character_id'] = dsk_units.apply(lambda x : eng_to_kor(x['character_id'], 'units'), axis=1)
    st.dataframe(dsk_units)

    items = []
    for _, row in dsk_units.iterrows():
        if row['item_1']:
            items.append(row['item_1'])
        if row['item_2']:
            items.append(row['item_2'])
        if row['item_3']:
            items.append(row['item_3'])

    item_df = pd.DataFrame({'name' : items}).dropna(subset=['name']).groupby('name').size().reset_index()
    item_df['name'] = item_df.apply(lambda x : eng_to_kor(x['name'], 'items'), axis=1)    
    item_df.set_index('name', inplace=True)
    st.dataframe(item_df)
    st.dataframe(dsk_units.groupby('character_id').size())



