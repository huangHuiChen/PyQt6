from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime
import yaml


def DB_link(query1:str):
    # 設置資料庫
    with open('db_info.yaml','r') as info:
        db_info = yaml.safe_load(info)
        server = db_info['DB_addr']
        dbname = db_info['DB_name']
        user = db_info['DB_User']
        paswd = db_info['DB_paswd']

    connection_string = f"mssql+pymssql://{user}:{paswd}@{server}/{dbname}"
    # 創建引擎 & 執行查詢語句
    engine1 = create_engine(connection_string)
    
    df1 = pd.read_sql(query1, engine1)
    return df1


def switch_example(cond_V):
    switcher = {
        'A': "Ace",
        'B': "Two",
        'C': "Three",
    }
    return switcher.get(cond_V, "未知的值")

def create_SQL( date_b, date_e:int):
    """
    用來產生SQL語句
    date_b, date_e格式:yyyymmdd
    cond: A、B、C
    """
    s1=f"""
        select  stock_set.stockId  AS st_id , stock_set.stockNa as st_na, 
        stock_recode.tdate, stock_record.signal, sum(stock_record.qty* stock_record.price) as tot_price
        from stock_set with(nolock) left join stock_record with(nolock)  on stock_set.stockId=stock_record.stockId
        WHERE stock_record.tdate >= '{date_b}' AND stock_record.tdate <= '{date_e}'
        group by  stock_set.stockId, stock_set.stockNa, stock_recode.tdate, stock_record.signal;
        """
    
    return s1

def deal_date(date1, date2: int, cond:str, dir_name: str):
    """
    date1, date2資料格式:yyyymmdd
    cond 欄位1
    將撈取到的資料進行分類並計算
    """
    cond01 = switch_example(cond)
    sql1 =  create_SQL(date1,date2)
    data_df = DB_link(sql1)
    data_df['st_id'] = data_df['st_id'].astype(str)
    data_df['st_na'] = data_df['st_na'].astype(str)
    data_df['tdate'] = pd.to_datetime(data_df['tdate'], format='%Y%m%d')
    data_df['signal'] = data_df['signal'].astype(str)
    data_df['tot_price'] = data_df['tot_price'].astype('int64')
    
    col = ['代號', '名稱', '日期', ' 訊號+', '金額', '訊號-', '金額', '總計']
    result_df = pd.DataFrame(columns=col)
    n = 0
    for i in data_df['tdate']:
        df_copy = data_df
        df_UP = data_df[(data_df['st_id']==cond01)&(data_df['tdate']==i)&(data_df['signal']=="U")]
        df_Down = data_df[(data_df['st_id']==cond01)&(data_df['tdate']==i)&(data_df['signal']=="D")]
        U_tot =  df_UP['tot_price'].sum()
        D_tot =  df_Down['tot_price'].sum()
        result_df.loc[n] = [cond01, df_copy['st_na'], i, '+', U_tot, '-', D_tot ]
        n = n+1
    
    result_df.to_excel(f'{dir_name}\{date1}-{str(date2)[4:]}_{cond01}計算_{datetime.now().strftime("%H%M%S")}.xlsx', index=False)
    
if __name__ == '__main__':
   deal_date('20240511','20240520','A')
    