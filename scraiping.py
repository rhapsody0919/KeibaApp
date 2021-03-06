import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

# infoからスクレイピングしてくるためのurlを作成
def make_url(info):

    info = ''.join(info)
    tansyo_url = 'https://nar.netkeiba.com/odds/index.html?type=b1&race_id='+info+'&rf=shutuba_submenu'
    umatan_url = 'https://nar.netkeiba.com/odds/index.html?type=b6&race_id='+info+'&housiki=c0&rf=shutuba_submenu'

    return tansyo_url, umatan_url

# スクレイピング
class Scraiping:

    def __init__(self, tansyo_url, umatan_url):

        self.t_url = tansyo_url
        self.u_url = umatan_url
    
    #　単勝オッズと馬単オッズをスクレイピングしてくる
    def get(self):
        
        # 単勝オッズをスクレイピング
        r = requests.get(self.t_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        div = soup.find('div', id = 'odds_tan_block')
        try :
            table = div.find('table', class_ = 'RaceOdds_HorseList_Table')

            horse_name = [td.text for td in table.find_all('td', class_ = 'Horse_Name')]
            horse_number = [str(i) for i in range(1, len(horse_name)+1)]
            # 取消になったらそこをnanにする
            odds = [float(td.text) if len(list(td.text)) > 0 and list(td.text)[0] != '取' else np.nan for td in table.find_all('td', class_ = 'Odds')]
            sc_df = pd.DataFrame({'馬番' : horse_number, '名前' : horse_name, '単勝' : odds})
            sc_df = sc_df.set_index('馬番')

            time.sleep(2)
            
            # 馬単オッズをスクレイピング
            r = requests.get(self.u_url)
            soup = BeautifulSoup(r.content, 'html.parser')

            table = soup.find_all('table', class_ = 'Odds_Table')
            for i in range(len(table)):
                #　取消になったらそこをnanにする
                odds = [float(td.text) if len(list(td.text)) > 0 and list(td.text)[0] != '取' else np.nan for td in table[i].find_all('td', class_ = 'Odds')]
                odds.insert(i, None)
                sc_df[str(i+1)] = odds

            time.sleep(2)
            print(sc_df)
            return sc_df
        except:
            return pd.DataFrame(index=[], columns=[])


