import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

from collections import Counter


# 코드북 데이터 가져오기
codeBook = pd.read_excel('./data/codeBook_v3.xlsx')
cols = codeBook['컬럼명'].unique()

# NPA_CL
station = dict()

# EVT_STAT_CD
event_state = dict()

# EVT_CL_CD
event_species = dict()

#RPTER_SEX
sex = dict()

for col in cols:
    tmp = codeBook[codeBook['컬럼명'] == col]
    for name, code, in zip(tmp['코드명'].tolist(), tmp['코드값'].tolist()):
        if col == 'NPA_CL':
            station[code] = name
        elif col == 'EVT_STAT_CD':
            event_state[code] = name    
        elif col == 'EVT_CL_CD':
            event_species[code] = name    
        elif col == 'RPTER_SEX':
            sex[code] = name

col_dict = {'경찰청' : station,
                '사건상태' : event_state,
                '사건종' : event_species,
                '신고자성별' : sex}

def get_swap_dict(d):
    return {v: k for k, v in d.items()}

def getCode(col, keyword, col_dict=col_dict):
    return get_swap_dict(col_dict[col])[keyword]

def getName(col, code, col_dict=col_dict):
    return col_dict[col][code]

# 모든 년도 비교
def compareYears(df, col, col_dict = col_dict):

    

    df20 = df[df['접수완료일'].str[:4]=='2020'][col].dropna().values
    df21 = df[df['접수완료일'].str[:4]=='2021'][col].dropna().values
    df22 = df[df['접수완료일'].str[:4]=='2022'][col].dropna().values
    df23 = df[df['접수완료일'].str[:4]=='2023'][col].dropna().values


    df20 = pd.DataFrame.from_dict(Counter(df20), orient='index').rename(columns={0:'cnt'})
    df21 = pd.DataFrame.from_dict(Counter(df21), orient='index').rename(columns={0:'cnt'})
    df22 = pd.DataFrame.from_dict(Counter(df22), orient='index').rename(columns={0:'cnt'})
    df23 = pd.DataFrame.from_dict(Counter(df23), orient='index').rename(columns={0:'cnt'})

    # year_df = [df20,df21,df22,df23]


    # for year in year_df:
    #     for idx in year.index:
    #         year.rename(index={ idx : col_dict[col][idx]}, inplace=True)
    
    
    df20 = df20.sort_values('cnt', ascending=False)
    df21 = df21.sort_values('cnt', ascending=False)
    df22 = df22.sort_values('cnt', ascending=False)
    df23 = df23.sort_values('cnt', ascending=False)

    
    plot1 = go.Bar(
             x = df20.index,
             y = df20['cnt'],
             name = "2020")

    plot2 = go.Bar(
             x = df21.index,
             y = df21['cnt'],
             name = "2021")
    
    plot3 = go.Bar(
             x = df22.index,
             y = df22['cnt'],
             name = "2022")
    
    plot4 = go.Bar(
             x = df23.index,
             y = df23['cnt'],
             name = "2023")
    
    data = [plot1, plot2, plot3, plot4]

    layout = go.Layout(title = col,
                        xaxis_title = col)
    
    fig = go.Figure(data=data, layout=layout)

    pyo.iplot(fig)


# 지정 항목 신고 수 시각화
def printCountData(df,col, drop_col = [], col_dict = col_dict):
    
    array = df[col].values
    target_dict = col_dict[col]

    show_df = pd.DataFrame.from_dict(Counter(array), orient='index').rename(columns={0:'cnt'})

    for idx in show_df.index:
        show_df.rename(index={ idx : target_dict[idx]}, inplace=True)
    
    show_df = show_df.sort_values('cnt', ascending=False)
    
    if len(drop_col):
        show_df.drop(index = drop_col, inplace=True)
    
    fig = px.bar(data_frame = show_df,
             x = show_df.index,
             y = 'cnt')
    
    fig.update_xaxes(tickangle=45)
    
    fig.update_layout(title = '사건 수',
                      xaxis_title = '사건 항목')
    

    fig.show()

# 지정년도 변화 비교
def printChangeRatio(df, year1, year2, col, drop_col = [], col_dict = col_dict):
    
    df1 = df[df['year']==year1]
    df2 = df[df['year']==year2]
        
    array1 = df1[col].values
    array2 = df2[col].values

    show_df1 = pd.DataFrame.from_dict(Counter(array1), orient='index').rename(columns={0:str(year1)})
    show_df2 = pd.DataFrame.from_dict(Counter(array2), orient='index').rename(columns={0:str(year2)})

    concat_df = show_df1.join(show_df2, how='inner')
    
    concat_df['ratio'] = ((concat_df[str(year2)] / concat_df[str(year1)]).round(2) - 1) * 100

    
    try:
        target_dict = col_dict[col]
        for idx in concat_df.index:
            concat_df.rename(index={ idx : target_dict[idx]}, inplace=True)
    except:
        pass

    concat_df = concat_df.sort_values('ratio', ascending=False)
    
    if len(drop_col):
        concat_df.drop(index = drop_col, inplace=True)
    
    fig = px.bar(data_frame = concat_df,
             x = concat_df.index,
             y = 'ratio')

    fig.update_xaxes(tickangle=45)

    fig.update_layout(title = '변화율(%)',
                      xaxis_title = '목록',
                      yaxis_title = '(%)')
    

    fig.show()


def getMonthilyData(df):
    monthily_event = df.groupby(['접수완료일']).size().reset_index().rename(columns={0:'cnt'})

    monthily_event['year'] = monthily_event['접수완료일'].str[:4]
    monthily_event['month'] = monthily_event['접수완료일'].str[5:7]

    monthily_event = monthily_event.drop('접수완료일', axis=1)

    result = pd.DataFrame()
    
    for i in range(1,13):
        
        tmp = monthily_event[monthily_event['month'].astype('int') == i].pivot_table(index=['month','year'], values=['cnt'], aggfunc='sum', fill_value=0).reset_index()

        result = pd.concat([result,tmp])

    return result

def printMonthly(month_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for y in month_df['year'].unique():
        target_df = month_df[month_df['year']==y]
        fig.add_trace(go.Line(x=target_df['month'].astype('int').values, y=target_df['cnt'].values, name=str(y)),secondary_y=False)

    fig.update_layout(
        title_text = '월별 보이스 피싱 신고 수',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [x for x in range(1,13)],
            ticktext = [str(x)+'월' for x in range(1,13)]
        )
    )

    fig.show()  