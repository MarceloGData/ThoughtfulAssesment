import os
import random
import requests
import pandas as pd
from datetime import datetime

class Output:
    def __init__(self, out_folder='output', imgs_folder='imgs', data_file='output'):
        self.__out_folder = out_folder
        self.__imgs_folder = os.path.join(self.__out_folder, imgs_folder)
        self.__data_file = data_file

        if(not os.path.exists(self.__out_folder)):
            os.makedirs(self.__out_folder)
        
        if(not os.path.exists(self.__imgs_folder)):
            os.makedirs(self.__imgs_folder)

    def save_imgs(self, dict_news):
        global img_folder, out_folder
        
        for news in dict_news:
            if(news['img_path'] != ''):
                tries_made = 0

                while(True):
                    try:
                        response = requests.get(news['img_path'], timeout = 3)
                        break
                    except:
                        tries_made += 1
                        #print('Failed ' + str(tries_made) + ' times to download image')

                        if(tries_made >= 3):
                            print('Failed too many times (' + str(tries_made) + ') to download image, try again later')
                            break
                        
                with open(os.path.join(self.__imgs_folder, news['img_name']), "wb") as f:
                    f.write(response.content)

    def save_news(self, dict_news, search_phrase, sections):
        df_news = pd.DataFrame(dict_news)
        
        if(len(df_news) == 0):
            return

        df_news['run_time'] = datetime.now()
        df_news['search_phrase'] = search_phrase
        df_news['sections'] = ';'.join(sections)
        
        excel_file_path = os.path.join(self.__out_folder, self.__data_file + '.xlsx')

        if(os.path.isfile(excel_file_path)):
            df_old_news = pd.read_excel(excel_file_path, sheet_name = 0, index_col = 0)
            df_news = pd.concat([df_old_news, df_news]).reset_index(drop=True)

        df_news.to_excel(excel_file_path)