import pandas as pd
import numpy as np
import pickle

import re

import plotly.express as px
import plotly.graph_objects as go

import  seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.colors as mcl
import matplotlib.patches as mpt
import matplotlib.ticker as mticker
plt.style.use('ggplot')

from tqdm import tqdm
from collections import Counter, defaultdict
from ast import literal_eval

import warnings
warnings.filterwarnings('ignore')

champ_cost_df = pd.read_csv('./data/champ_cost.csv', index_col=0)
tiers = ['CHALLENGER', "GRANDMASTER", 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', "IRON"]
kor_tier_dict = {
    0 : '챌린저',
    1 : '그랜드마스터',
    2 : '마스터',
    3 : '다이아',
    4 : '플래티넘',
    5 : '골드',
    6 : '실버',
    7 : '브론즈',
    8 : '아이언'
}

word_dict = {
    'augments' : '증강',
    'units' : '챔피언',
    'items' : '아이템',
    'placement' : '등 수',
    'traits' : '시너지'
}

tier_dict = {i : x for i, x in enumerate(tiers)}

with open('./data/tft_dict.pkl', 'rb') as f:
    tft_dict = pickle.load(f)


#함수
def string_to_dict(s):
    return literal_eval(s)


# 사전 반전
def swap_dict(dicts):
    return {v:k for k,v in dicts.items()}


#시각화 함수
def printTierBasicInfo(df):
    fig = px.bar(data_frame=df, x='tier', y = 'games', title='티어별 게임수', text = 'games')
    fig.update_traces(texttemplate='%{text:,}', textposition='auto')

    fig.show()
    # fig.show('svg')

    fig = go.Figure(data=[
            go.Bar(name = '승리', x = df['tier'], y = df['wins'], text = df['wins'],  textposition='auto', texttemplate = "%{text:,}"),
            go.Bar(name = '패배', x = df['tier'], y = df['losses'], text = df['losses'],  textposition='auto', texttemplate = "%{text:,}")
    ])
    fig.update_layout(barmode='group',
                    title = "티어별 승/패")

    fig.show() 
    # fig.show('svg')



def printCols(df, col, tier_idx ,grade = [1,2,3,4,5,6,7,8]):
    
    concat_df = pd.DataFrame()
    
    for g in grade:
        con = df['placement'] == g
        con_df = df[con][col]
    
        counts = Counter(con_df.sum())
        count_df = pd.DataFrame({
            'code' : counts.keys(),
            'cnt' : counts.values(),
            'placement' : g
        })
        
        concat_df = pd.concat([concat_df, count_df])
    
    top10_list = concat_df.sort_values(['placement','cnt'], ascending=[True, False])['code'].unique()[:10]
    # concat_df.sort_values('cnt', ascending=False, inplace=True)
    concat_df.sort_values(['placement','cnt'], ascending=[True, False], inplace=True)
    
    # top10_list = concat_df['code'].unique()[:10]

    top10 = concat_df[concat_df['code'].isin(top10_list)]
    top10 = top10[top10['placement'] < 5]
    
    plt.figure(figsize=(15,10), dpi=150)
    
    kor_X = [tft_dict[col].iloc[x]['korName'] for x in top10['code']]
    
    sns.barplot(data=top10, x = kor_X, y='cnt', hue='placement')
    
    plt.title(word_dict[col] + ' 1~4등 통계')

    plt.legend(title = word_dict['placement'])

    plt.ylabel("사용 횟수")

    plt.savefig('./img/'+str(col)+"_"+tier_dict[tier_idx]+".png")

    plt.show()

    return concat_df

def getTotalGames(code, df):
    return df[df['code']==code]['cnt'].values[0]


def draw_1Place(df, col, isBest = True):
    asc = not isBest
    tmp = df.groupby('code')['cnt'].sum().reset_index()
    tmp = tmp[tmp['cnt']>100].reset_index()
    using_code = tmp['code'].values
    
    df_1place = df[df['placement'] == 1]
    df_1place = df_1place[df_1place['code'].isin(using_code)]
    df_1place['placeRatio'] = (df_1place['cnt'] / df_1place['code'].apply(getTotalGames, args=[tmp]))*100
    
    df_1place.reset_index(drop=True, inplace=True)
    
    if col == 'augments':
        top_list = df_1place.sort_values(['cnt', 'code'], ascending=[asc, True])['code'].unique()[:8]
    elif col == 'units':
        top_list = df_1place.sort_values(['cnt', 'code'], ascending=[asc, True])['code'].unique()[:8]
    elif col == 'traits':
        top_list = df_1place.sort_values(['cnt', 'code'], ascending=[asc, True])['code'].unique()[:10]
    
    plt.figure(figsize=(16,8))

    word = 'Best'
    if asc:
        word = 'Wrost'

    plt.title('사용수' + word + word_dict[col] + ' 승률')

    graph_df = df_1place[df_1place['code'].isin(top_list)]

    if col == 'traits':
        graph_df.drop(index = graph_df[graph_df['code'].str.contains('Set7')].index, inplace=True)
        graph_df['code'] = [tft_dict[col][tft_dict[col]['apiName'] == x]['korName'].values[0] for x in graph_df['code'].values]
    else:
        graph_df['code'] = [tft_dict[col].iloc[x]['korName'] for x in graph_df['code'].values]

    x_kor = [kor_tier_dict[swap_dict(tier_dict)[x]] for x in graph_df['tier'].values]

    sns.lineplot(data=graph_df, x = x_kor, y = 'placeRatio', hue='code', markers=True, style='code')

    plt.legend(title = word_dict[col])
    plt.ylabel("승률")
    
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f %%'))

    plt.savefig('./img/1Place_'+ str(col) +'.png')
    
    plt.show()


def checkin(col, target):
    if target in col:
        return True
    else:
        return False
    
def getUnitAugs(df, unit, grade = 1):
    target = df[df['units'].apply(checkin, args=[unit])]
    
    con = target['placement'] == 1
    con_df = target[con]['augments']

    counts = Counter(con_df.sum())
    count_df = pd.DataFrame({
        'code' : counts.keys(),
        'cnt' : counts.values(),
    })

    count_df = count_df[count_df['cnt']>100]
    count_df.sort_values(['cnt'], ascending=False, inplace=True)
    
    return count_df

def drawUnitAgus(df, unit):
    
    tmp = df.groupby('code')['cnt'].sum().reset_index()
    tmp = tmp[tmp['cnt']>300].reset_index()
    using_code = tmp['code'].values

    df_1place = df[df['code'].isin(using_code)]
    df_1place['placeRatio'] = (df_1place['cnt'] / df_1place['code'].apply(getTotalGames, args=[tmp]))*100

    df_1place.reset_index(drop=True, inplace=True)

    top_list = df_1place.sort_values(['placeRatio'], ascending=[False])['code'].unique()[:10]

    graph_df = df_1place[df_1place['code'].isin(top_list)]

    graph_df['code'] = [tft_dict['augments'].iloc[x]['korName'] for x in graph_df['code'].values]
    x_kor = [kor_tier_dict[swap_dict(tier_dict)[x]] for x in graph_df['tier'].values]

    
    plt.figure(figsize=(12,6))
    plt.title(tft_dict['units'].iloc[unit]['korName'] + ' 승률 Top10')
    sns.lineplot(data=graph_df, x = x_kor, y = 'placeRatio', hue='code', markers=True, style='code')
    
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f %%'))

    plt.savefig('./img/UnitAugs_'+ tft_dict['units'].iloc[unit]['korName'] +'.png')
    
    plt.show()



def unionChampItems(units, items):
    result = dict()
    for idx, unit in enumerate(units):
        result[unit] = items[idx]
    return result

def getTargetUnit(df, unit_code):
    if unit_code in df.keys():
        return df[unit_code]
    else:
        return ''
    
def unitItemStatic(df, target_unit):
    result = []

    unit_items = getTargetUnit(df, target_unit)
    
    for item in unit_items:
        result.append(item)

    return result

def printUnitItems(df, target, idx, grade = [1,2,3,4]):
    
    concat_df = pd.DataFrame()
    
    for g in grade:
        con = df['placement'] == g
        con_df = df[con]

        con_df['unit_items'] = con_df.apply(lambda x: unionChampItems(x['units'], x['items']), axis=1)


        target_items = (con_df['unit_items'].apply(unitItemStatic, args=[target]))

        counts = Counter(target_items.sum())

        count_df = pd.DataFrame({
            'code' : counts.keys(),
            'cnt' : counts.values(),
            'placement' : g
        })
        
        count_df = count_df.sort_values('cnt', ascending=False)[:5]

        concat_df = pd.concat([concat_df, count_df])
        
    drawPiePlot(concat_df, idx)

def drawPiePlot(df, idx):
    freq_col = 'cnt'
    outer_col = 'placement'
    inner_col = 'code'

    size = 0.3 ## 바깥쪽, 안쪽 도넛 조각 조각의 반지름 비율을 0.3으로 한다.
    threshold = 4 ## 상한선 백분율

    color = sns.color_palette('hls',len(df[outer_col].unique())) ## 바깥쪽 도넛의 색상설정

    summary = df.groupby(outer_col)[freq_col].sum().reset_index() ## 등수별 아이템 사용횟수 집계
    outer_data = summary[freq_col] ## 바깥쪽 도넛에 해당하는 데이터
    inner_data = [] ## 안쪽 도넛에 대응하는 데이터
    for s in summary[outer_col]:
        inner_data += list(df[df[outer_col] == s]['cnt'].values)

    fig = plt.figure(figsize=(8,8)) ## 캔버스 생성
    fig.set_facecolor('white') ## 캔버스 배경색을 하얀색으로 설정
    ax = fig.add_subplot() ## 프레임 생성

    ## 바깥쪽 도넛 조각 차트 출력
    out_pie = ax.pie(outer_data,
                 radius=1,
                 colors=color,
                 wedgeprops=dict(width=size,edgecolor='w'))

    ## 바깥쪽 도넛 백분율 텍스트 출력
    total = np.sum(outer_data) ## 바깥쪽 빈도수의 총합

    sum_pct = 0 ## 백분율 초기값

    for i in range(len(outer_data)):
        ang1, ang2 = out_pie[0][i].theta1, out_pie[0][i].theta2 ## 각1, 각2
        out_r = out_pie[0][i].r ## 원의 반지름

        x = ((2*out_r-size)/2)*np.cos(np.pi/180*((ang1+ang2)/2)) ## 바깥쪽 도넛 조각의 중앙쪽 x좌표
        y = ((2*out_r-size)/2)*np.sin(np.pi/180*((ang1+ang2)/2)) ## 바깥쪽 도넛 조각의 중앙쪽 y좌표

        if i < len(outer_data) - 1:
            sum_pct += float(f'{outer_data[i]/total*100:.2f}') ## 백분율을 누적한다.
            ax.text(x,y,f'{outer_data[i]/total*100:.2f}%',ha='center',va='center') ## 백분율 텍스트 표시
        else: ## 총합을 100으로 맞추기위해 마지막 백분율은 100에서 백분율 누적값을 빼준다.
            ax.text(x,y,f'{100-sum_pct:.2f}%',ha='center',va='center')

    outer_color = [] ## 바깥쪽 도넛 조각의 색상을 hsv 컬러로 담을 리스트
    for p in out_pie[0]:
        outer_color.append(p.get_facecolor()) ## 바깥쪽 도넛 조각을 rgb 컬러로 가져온다.
    outer_color_hsv = [mcl.rgb_to_hsv(x[:3]) for x in outer_color] ## rgb를 hsv로 바꾼다.
    outer_color_hsv = [(x[0],x[1],1) for x in outer_color_hsv] ## 색상 채도만 가져오고 명도는 1로 고정한다.

    inner_color = [] ## 안쪽 도넛 조각의 색상을 담는 리스트
    for i, g in enumerate(summary[outer_col]):
        num_sub_group = len(df.query('{0}==@g'.format(outer_col))) ## 하위 그룹 개수
        jump = outer_color_hsv[i][1]/(num_sub_group+1) ## 채도 등분점 간격
        temp_list = []
        temp_s = np.arange(0,outer_color_hsv[i][1],jump) 
        temp_s = temp_s[1:] ## 채도 등분점
        for t in temp_s:
            h = outer_color_hsv[i][0] ## 색상
            s = t ## 채도
            v = outer_color_hsv[i][2] ## 명도
            temp_list.append((h,s,v))
        inner_color += temp_list[::-1] ## 순서를 바꿈

    inner_color = [mcl.hsv_to_rgb(x) for x in inner_color] #3 hsv를 다시 rgb로 바꾼다.

    ## 안쪽 도넛 차트 출력
    inner_pie = ax.pie(inner_data,
           radius=1-size,
           colors=inner_color,
           wedgeprops=dict(width=size,edgecolor='w'))

    ## 안쪽 도넛 백분율 텍스트 출력
    bbox_props = dict(boxstyle='square',fc='w',ec='w',alpha=0) ## annotation 박스 스타일
    config = dict(arrowprops=dict(arrowstyle='-'),bbox=bbox_props,va='center')

    inner_sum_pct = 0 ## 안쪽 도넛 백분율 초기값
    for i in range(len(inner_data)):
        ang1, ang2 = inner_pie[0][i].theta1, inner_pie[0][i].theta2 ## 안쪽 각1, 안쪽 각2
        r = inner_pie[0][i].r ## 안쪽 도넛의 반지름

        x = ((2*r-size)/2)*np.cos(np.pi/180*((ang1+ang2)/2)) ## 안쪽 도넛 조각의 중앙쪽 x좌표
        y = ((2*r-size)/2)*np.sin(np.pi/180*((ang1+ang2)/2)) ## 안쪽 도넛 조각의 중앙쪽 y좌표

        if i < len(inner_data) - 1:
            inner_sum_pct += float(f'{inner_data[i]/total*100:.2f}') ## 백분율을 누적한다.
            text = f'{inner_data[i]/total*100:.2f}%' ## 백분율 텍스트 표시
        else: ## 총합을 100으로 맞추기위해 마지막 백분율은 100에서 백분율 누적값을 빼준다.
            text = f'{100-inner_sum_pct:.2f}%'

        ## 비율 상한선보다 작은 것들은 Annotation으로 만든다.
        if inner_data[i]/total*100 < threshold:
            ang = (ang1+ang2)/2 ## 중심각
            x = out_r*np.cos(np.deg2rad(ang)) ## Annotation의 끝점에 해당하는 x좌표
            y = out_r*np.sin(np.deg2rad(ang)) ## Annotation의 끝점에 해당하는 y좌표

            ## x좌표가 양수이면 즉 y축을 중심으로 오른쪽에 있으면 왼쪽 정렬
            ## x좌표가 음수이면 즉 y축을 중심으로 왼쪽에 있으면 오른쪽 정렬
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang) ## 시작점과 끝점 연결 스타일
            config["arrowprops"].update({"connectionstyle": connectionstyle}) ## 
            ax.annotate(text, xy=((out_r-size)*x, (out_r-size)*y), xytext=(1.5*x, 1.2*y),
                        horizontalalignment=horizontalalignment, **config)
        else:
            x = ((2*r-size)/2)*np.cos(np.pi/180*((ang1+ang2)/2)) ## 텍스트 x좌표
            y = ((2*r-size)/2)*np.sin(np.pi/180*((ang1+ang2)/2)) ## 텍스트 y좌표
            ax.text(x,y,text,ha='center',va='center')

    ## 범례
    ## 범례는 2줄로 만든다. 왼쪽 줄에는 상위 그룹을 표시하고 오른쪽 줄에는 하위 그룹을 표시한다.
    inner_pie_index = -1 ## 안쪽 도넛 차트의 데이터에 접근할 인덱스 초기값
    right_legend_patches = [] ## 오른쪽 범례 칼럼에 들어가는 요소
    left_legend_patches = [] ## 왼쪽 범례 칼럼에 들어가는 요소
    right_labels = [] ## 오른쪽 범례 칼럼에 들어가는 라벨
    left_labels = [] ## 왼쪽 범례 칼러에 들어가는 라벨
    for i in range(len(outer_data)):
        left_legend_patches.append(out_pie[0][i])

        outer_label = summary[outer_col][i] ## 바깥쪽 도넛 차트 라벨

        left_labels.append(outer_label)
        temp_data = df.query('{0}==@outer_label'.format(outer_col)) ## 바깥쪽 라벨에 대응하는 안쪽 도넛 데이터
        temp_data = temp_data.reset_index(drop=True)

        temp_number = len(temp_data)-1

        ## 오른쪽 범례 개수와 맞추기 위해 빈 범례를 만듬
        for k in range(temp_number):
            rect = mpt.Rectangle((0,0),1,1.1,facecolor='None')
            left_legend_patches.append(rect)
            left_labels.append('')

        ## 오른쪽 범례 칼럼을 만든다.
        for j in range(len(temp_data)):
            inner_pie_index += 1

            right_legend_patches.append(inner_pie[0][inner_pie_index])
            right_labels.append(temp_data[inner_col][j])

        ## 범례 요소와 라벨을 합친다.
        legend_patches = left_legend_patches+right_legend_patches

    right_labels = [tft_dict['items'].iloc[rl]['korName'] for rl in right_labels]
    labels = left_labels + right_labels

    ## 범례 출력
    plt.legend(legend_patches,
               labels,
               ncol=2,
               loc='upper left',
               handleheight=1, ## 범례 줄 맞춤
               labelspacing=0.5, ## 범례 줄 간격
               bbox_to_anchor=(1.2,1),
                fontsize=8)

    plt.savefig('./img/Pie_' + tier_dict[idx] + ".png")
    plt.show()

def sumTraits(rows):
    result = pd.DataFrame()
    cnt = 0
    for row in rows:
        if len(row) == 0:
            continue
        tmp = pd.DataFrame(row)
        
        tmp = tmp[tmp['style'] != 0].sort_values('style', ascending=False).reset_index(drop=True)
        
        tmp['group'] = cnt
        tmp['detail'] = ''
        tmp['detail'][0], tmp['detail'][1:] = 1, 2
        cnt+=1
        result = pd.concat([result, tmp])
        
    return result
        
    
def getTraitsCnt(df, tier):
    result = pd.DataFrame()
    grade = df['placement'].unique()
    
    for g in grade:
        place_df = df[df['placement'] == g]
        place_df['traits'] = place_df['traits'].apply(string_to_dict)

        traits_df = sumTraits(place_df['traits'])

        counts = Counter(traits_df['name'].values)

        count_df = pd.DataFrame({
            'code' : counts.keys(),
            'cnt' : counts.values(),
            'placement' : g,
            'tier' : tier
        })
        count_df.sort_values(['cnt'], ascending=False, inplace=True)
        
        result = pd.concat([result, count_df])
        
    return result
    
def printTraits(df):
    col = 'traits'
    
    df.sort_values(['placement','cnt'], ascending=[True, False], inplace=True)
    top10_list = df['code'].unique()[:10]

    top10 = df[df['code'].isin(top10_list)]
    top10 = top10[top10['placement'] < 5]
    
    plt.figure(figsize=(15,10), dpi=150)
    
    kor_X = [tft_dict[col][tft_dict[col]['apiName']==x]['korName'].values[0] for x in top10['code']]
    
    sns.barplot(data=top10, x = kor_X, y='cnt', hue='placement')
    
    plt.title(word_dict[col] + ' 1~4등 통계')

    plt.legend(title = word_dict['placement'])

    plt.ylabel("사용 횟수")

    plt.show()