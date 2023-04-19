import pandas as pd
def read_data(file_path):

    return pd.read_csv(file_path)

def preprocessing(df):
    # 전처리
    # return df
    pass

def select_topic(df):
    flags = (df['content'].str.contains('gpt')) | (df['content'].str.contains('GPT')) |\
         (df['content'].str.contains('챗')) | (df['content'].str.contains('자연어'))

    return df[flags].reset_index(drop=True)
    

def summarize(df):
    # df['content'] 요약
    # return df['summarized_text']
    pass


import asyncio
class TelegramManager:
    def __init__(self):
        pass
        
        
    async def init_bot(self):
        self.token = '텔레그램 토큰 입력'  
        self.bot = telegram.Bot(self.token)
        self.chat_id = '알람 받을 id' #숫자 형태

    async def send_msg(self, text):
        if text == '':
            print('None GPT Contents')
            return 
        try:
            print(self.chat_id)
            for sending_id in self.chat_id:
                print(sending_id)
                self.bot.sendMessage(chat_id = sending_id, text = text, parse_mode = 'Markdown')
        except Exception as e:
            print(e)

        return 



async def init_telegram():
    bot = TelegramManager()

    await bot.init_bot()

    return bot

async def send_msg(bot, topics):

    send_text = ''
    for idx, row in topics.iterrows():
        main_text = row['title']
        url = row['url']
        writed_at = '(' + row['writed_at'] + ')\n\n'
        send_text += f"[{main_text}]({url})" + writed_at
        

    await bot.send_msg(send_text)

import pip 
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


import os
import json
def isModify():
    last_modify = os.path.getmtime('/home/ubuntu/news3/news.csv')
    try:
        with open('/home/ubuntu/news3/save_modify_time.json','r') as f:
            save_modify_time = json.load(f)['modify_time']
    except:
        save_modify_time = 0
    
    modify_time_dict = dict()


    if last_modify > save_modify_time:
        print('Modify csv file')
        modify_time_dict['modify_time'] = last_modify
        result = True
    else:
        print('Not Modify csv file')
        modify_time_dict['modify_time'] = save_modify_time
        result = False
    
    
    with open('/home/ubuntu/news3/save_modify_time.json','w') as f:
        json.dump(modify_time_dict, f, ensure_ascii=False, indent=4)

    return result


import time
import sys
if __name__ == '__main__':
    start_time = time.time()
    print("-"*30)
    location_time = time.localtime()
    print(f'Running Start : {str(location_time.tm_mon)} - {str(location_time.tm_mday)} / {str(location_time.tm_hour)} : {str(location_time.tm_min)}')
    print("-"*30)
    
    if isModify():
        try:
            import telegram
        except:
            print('Install Telegram')
            install('python-telegram-bot')
            import telegram
        
        csv_path = '/home/ubuntu/news3/news.csv'
        new_contents = read_data(csv_path)

        if len(new_contents) == 0:
            print('No Contents')
        
        else:
            # 키워드 뉴스 뽑아내기
            topics = select_topic(new_contents)
            print('GPT ARTICLE : ', len(topics))
            # 전처리
            # topics = preprocessing(topics)

            # # 요약
            # summarize = summarize(topics)

            # 텔레그램
            loop = asyncio.get_event_loop()
            push_article = loop.run_until_complete(init_telegram())

            loop.run_until_complete(send_msg(push_article, topics))
            loop.close()

        #delete csv
        # if os.path.isfile(csv_path):
        #     print('Remove CSV')
        #     os.remove(csv_path)

    print()
    print(f'Running Time :  {time.time() - start_time}')


   