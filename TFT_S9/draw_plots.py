import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

basic_word_dict = {
    'augments' : '증강',
    'units' : '챔피언',
    'traits' : '시너지',
    'items' : '아이템'
}

def draw_linePlot(df, col, raw_df = pd.DataFrame()):

    col_to_kor = basic_word_dict[col]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    draw_cols = df[col].unique()

    
    
    if len(raw_df):
        dot_df = pd.DataFrame(raw_df.reset_index().groupby('game_time')['match_cnt'].max())

        fig.add_trace(go.Bar(
            x = dot_df.index,
            y = dot_df['match_cnt'],
            # line= dict(dash='dot', width=2, color = 'skyblue'),
            name = '전체 게임수',
            hovertemplate = '<i>게임 진행 횟수</i>: %{y}',
            opacity=0.6,
        ),secondary_y = False)
    else:
        dot_df = pd.DataFrame(df.reset_index().groupby('game_time')['match_cnt'].max())
        fig.add_trace(go.Bar(
            x = dot_df.index,
            y = dot_df['match_cnt'],
            # line= dict(dash='dot', width=2, color = 'skyblue'),
            name = '전체 게임수',
            hovertemplate = '<i>증게임 진행 횟수</i>: %{y}',
            opacity=0.6,
        ),secondary_y = False)

    for target in draw_cols:
        tmp = df[df['augments'] == target]
        fig.add_trace(go.Scatter(
            x = tmp.index,
            y = tmp['cnt'],
            mode='markers+lines',
            name = target,
            hovertemplate =
            f'<i>{col_to_kor}</i>: {target}'+
            '<br><b>증강 선택수</b>: %{y}<br>',
            # f'<b>게임수 : {target["cnt"]}</b>',
            # text = ['Custom text {}'.format(i + 1) for i in range(5)],
            # showlegend = False
            ),secondary_y = True)
        
    if len(raw_df):
        fig.update_layout(
        legend=dict(
            orientation="h", # 가로 방향으로
            yanchor="top", y=1.13, # y축 방향 위치 설정
            xanchor="left", x=0.01, # x축 방향 위치 설정
        ))

    fig.update_layout(hovermode="x")
    
    fig.update_layout(title=dict(
        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음
        text='전체 게임수(좌) / 증강 선택수 (우)',
        x=0.5,
        xanchor = 'center',
        font=dict(
            family="Arial",
            size=25
        )))
    return fig


def draw_histPlot(df, col):
    col_to_kor = basic_word_dict[col]

    fig = go.Figure()

    draw_cols = df[col].unique()

    for target in draw_cols:
        tmp = df[df['units'] == target]
        fig.add_trace(go.Bar(
            x = tmp['items'],
            y = tmp['cnt'],
            # mode='markers+lines',
            name = target,
            hovertemplate =
            f'<i>{col_to_kor}</i>: {target}'+
            '<br><b>아이템</b>: %{x}<br>'+
            '<b> 사용수 : %{y}</b>',
            # text = ['Custom text {}'.format(i + 1) for i in range(5)],
            # showlegend = False
            ))
        
    fig.update_layout(yaxis2_tickformat = '%d')
    
    fig.update_layout(hovermode="x")
    
    return fig


def draw_line_unit(df, col, mode = 'markers+lines'):

    col_to_kor = basic_word_dict[col]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    draw_cols = df[col].unique()
    
    
    fig = go.Figure()

    for value in draw_cols:
        target = df[df['items'] == value]
        fig.add_trace(go.Scatter(
            x = target.index,
            y = target['cnt'],
            mode = mode,
            name =  value,
        ))
    fig.update_layout(hovermode="x")

    return fig

def draw_save_linePlot(df, col, type):

    col_to_kor = basic_word_dict[col]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    draw_cols = df[col].unique()

    text = '순방' if type == 'save_rank' else '승'


    # colors = ['green', 'orange', 'blue', 'red', 'purple']
    colors = ['mediumpurple', 'deepskyblue', 'lightsalmon', 'darkolivegreen',
                'dimgray']
    
    for idx,target in enumerate(draw_cols):
        tmp = df[df['augments'] == target]

        fig.add_trace(go.Bar(
            x = tmp.index,
            y = tmp['total_cnt'],
            name =  target,
            opacity=0.8,
            marker_color = colors[idx]
        ),secondary_y = False)

        fig.add_trace(go.Scatter(
            x = tmp.index,
            y = tmp['ratio'],
            mode='markers+lines',
            name = target,
            marker=dict(
                color=colors[idx]),
            hovertemplate =
            f'<i>{col_to_kor}</i>: {target}'+
            f'<br><b>{text}률</b>:' + '%{y:.2%}<br>',
            showlegend=False
            # f'<b>게임수 : {target["cnt"]}</b>',
            # text = ['Custom text {}'.format(i + 1) for i in range(5)],
            # showlegend = False
            ),secondary_y = True)

    fig.update_layout(yaxis2_tickformat = '.0%')
    fig.update_layout(
	legend=dict(
        orientation="h", # 가로 방향으로
        yanchor="top", y=1.1, # y축 방향 위치 설정
        xanchor="left", x=0.01, # x축 방향 위치 설정
	))

    fig.update_layout(title=dict(
        # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음
        text= f'전체 게임수 - 막대(우) / {text}률 - 꺽은선(우)',
        x=0.5,
        xanchor = 'center',
        font=dict(
            family="Arial",
            size=20
        )))
    fig.update_layout(hovermode="x")
    
    return fig

def draw_trend_df(df):

    draw_cols = df['시너지'].unique()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    for idx,target in enumerate(draw_cols):
        tmp = df[df['시너지'] == target]

        fig.add_trace(go.Scatter(
            x = tmp.index,
            y = tmp['우승 횟수'],
            mode='markers+lines',
            opacity= 0.6 + idx * 0.025,
            name = target
        ))
    fig.update_layout(hovermode="x")
    return fig

def legend_trends(df, title, mode = 'markers+lines'):

    # fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = go.Figure()

    draw_cols = sorted(list(df['isLegends'].unique()))

    colors = px.colors.qualitative.Plotly + px.colors.qualitative.D3
    
    for idx, value in enumerate(draw_cols):
        target = df[df['isLegends'] == value].resample('1D').sum()
        fig.add_trace(go.Scatter(
            x = target.index,
            y = target['cnt'],
            mode = mode,
            marker=dict(
                color=colors[idx]),
            name =  value,
        ))
    fig.update_layout(
        title=dict(text= title, font=dict(size=20), automargin=True, yref='paper')
    )
    fig.update_layout(hovermode="x")

    return fig


def streamer_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = df.index,
        y = df['placement'],
        text = df['placement'],
        textposition='auto',
        textfont_color="white",

    ))

    fig.update_traces(marker_color='gray')

    return fig

def streamer_chart_traits(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x = df.index,
        y = df['cnt'],
        text = df['cnt'],
        textposition='auto',
        textfont_color="white",

    ))

    fig.update_traces(marker_color='gray')

    return fig