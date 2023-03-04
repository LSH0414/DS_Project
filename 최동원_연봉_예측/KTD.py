import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# import sys
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('set_matplotlib_hangul.py'))))

pd.set_option('display.max_column',100)
pd.set_option('display.max_row',500)
import warnings 
warnings.filterwarnings("ignore")

# 키워드만 입력해도 팀 풀네임 찾아주기
def findTeamFullName(keyword, df):
    user_keyword = keyword

    return df[df['team'].str.contains(user_keyword)]['team'].unique()[0]


def getRank(df, team_df, col, year, asc):
    # print("In getRank Function : ", col, year)
    # tmp_df = kbo_df[kbo_df['year'] == year]
    # return int(tmp_df[col].rank(method='max')[tmp_df[tmp_df['team'] == team_df['team'].unique()[0]]['team'].index.values[0]])
    tmp_df = df[df['year'] == year][['team', col]].sort_values(col, ascending=asc)
    tmp_df = tmp_df.reset_index(drop=True)
    return tmp_df[tmp_df['team'] == team_df['team'].values[0]].index.values[0] + 1

def getFristYears(df,team_df, col, asc):
    start_year = team_df['year'].min()
    end_year = team_df['year'].max()

    result = []
    for y in range(start_year, end_year+1):
        if 1 == getRank(df, team_df, col, y, asc=asc):
            result.append(y)
    
    return result


def getSeasonStatic(df, team_df, col):

    ascending = ['average_age','runs_per_game', 'losses','ERA','run_average_9','hits','runs','earned_runs', 'home_runs', 'walks',
                        'intentional_walks','hit_batter','balks','wild_pitches','batters_faced','WHIP','hits_9','homeruns_9','walks_9']
    

    max_value = team_df[col].max()
    min_value = team_df[col].min()
    max_year = team_df[team_df[col] == team_df[col].max()]['year'].values[0]
    min_year = team_df[team_df[col] == team_df[col].min()]['year'].values[0]

    print("-" * 50)
    print("MAX Value, year : {:6}, {:4}" .format(max_value, max_year))
    print("MIN Value, year : {:6}, {:4}" .format(min_value, min_year))
    if '_age' in col:
        print("1st Ranking Years : {}" .format(getFristYears(df,team_df, col,(col in ascending))), end='\t')
        print("!!Age Data Younger is Positive")
    else:
        print("1st Ranking Years : {}" .format(getFristYears(df,team_df, col, (col in ascending))))


def printStaticInfo(df,team_df, col):
    print('DATA : {:10}'.format(col))
    getSeasonStatic(df,team_df, col)
    

def drawAvgPlot(team_df, col):
    
    sns.lineplot(data = team_df, x='year', y=col).set(title = col + ' AVG Graphs of year')
    

def drawAvgTeamData(team, df):
    team_df = df[df['team']==team]

    cols = np.delete(team_df.columns.values, (0,1,2))
    
    print("{:10}'s EDA ".format(team))
    for col in cols:
        plt.figure(figsize=(12,6))
        drawAvgPlot(team_df, col)
        plt.show()
        printStaticInfo(df,team_df, col)