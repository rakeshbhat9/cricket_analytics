# Std Lib
import requests
import logging
import sqlite3 as sql
from datetime import datetime
import time

# 3rd Party Lib
from bs4 import BeautifulSoup
import pandas as pd
import click

#Config
log_file = f"/logs/cric_etl_{datetime.today().strftime('%Y%m%d')}.log"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.StreamHandler(),logging.FileHandler(log_file)])

# --------------------------------------------------------------------------------------------

def extract_data(url):

    logging.info("Sourcing data")

    r = requests.get(url)

    if r.status_code != 200:
        logging.info(f"Request failed with code {r.status_code}")
        return
    
    soup = BeautifulSoup(r.content, 'html.parser')

    over_nums = soup.find_all("span",attrs={'class':"match-comment-over"})
    over_nums_text = [x.text for x in over_nums] 

    comm_short = soup.find_all("div",attrs={'class':"match-comment-short-text"})
    comm_short_text = [x.text for x in comm_short] 
    
    comm_long = soup.find_all("div",attrs={'class':"match-comment-long-text",'itemprop':"articleBody"})
    comm_long_text = [x.text for x in comm_long]

    published_time = soup.find_all("time",attrs={'itemprop':'datePublished'})
    published_time_text = [x['datetime'] for x in published_time]

    data = zip(published_time_text,over_nums_text,comm_short_text,comm_long_text)
    logging.info("Data sourced")

    return data

# --------------------------------------------------------------------------------------------

def transform_data(data):

    logging.info("Transforming data")

    df = pd.DataFrame(data,columns=['publishedTime','over','shortComm','longComm'])
    df['publishedTime'] = pd.to_datetime(df['publishedTime'])

    df['ball'] = df['over'].apply(lambda x: x.split(".")[-1])
    df['ball'] = df['ball'].astype('int')

    df['over'] = df['over'].apply(lambda x: x.split(".")[0])
    df['over'] = df['over'].astype('int')

    df['bowler'] = df['shortComm'].apply(lambda x: x.split("to")[0].strip())
    df['batsman'] = df['shortComm'].apply(lambda x: x.split("to")[-1].split(",")[0].strip())

    df['runScored'] = df['shortComm'].apply(lambda x: x.split(",")[-1].replace("run","").replace("no",'0').strip())
    
    max_over = df['over'].max()
    logging.info(f"Latest over recieved is {max_over}")

    latest_over_balls = df[df['over'] == max_over].shape[0]
    if latest_over_balls != 6:
        df = df[df['over'] != df['over'].max()]
        logging.info(f"Dropping data from over {max_over}, as over is not complete")
    
    logging.info("Data transformed")

    return df

# --------------------------------------------------------------------------------------------


def save_data(df):

    if df.empty:
        logging.info("No data to update")
        return
    
    with sql.connect('/database/cricinfo_raw.db')  as conn:
        list_of_tables = pd.read_sql('''SELECT name from sqlite_master where type= "table"''',conn)['name'].unique().tolist()
    
    # ToDo: Create a unique table name per match and remove 'raw'

        if 'raw' not in list_of_tables:
            logging.info("Table doesn't exist hence creating a new one")
            df.to_sql('raw',conn,if_exists='append',index=False)
            logging.info(f"Saved data as of {df['over'].max()} over")
    
        else:
            latest_over = pd.read_sql('''SELECT max(over) as last_over FROM raw ''',conn)['last_over'].values[0]
            logging.info(f"Latest over saved in DB is {latest_over}")
            df = df[(df['over']>latest_over)]
            if df.empty:
                logging.info("No additional data to update")
            else:
                df.to_sql('raw',conn,if_exists='append',index=False)
                logging.info(f"Saved data as of {df['over'].max()} over")
    
    return
# --------------------------------------------------------------------------------------------

def time_check(start,finish):
    
    test_live = False
    hour_now = datetime.now().hour
    if  hour_now>=start and hour_now<=finish:
        test_live = True
    
    return test_live

#  --------------------------------------------------------------------------------------------
@click.command()
@click.option('--url', default=None, help='Full commentary URL from cricinfo site')
@click.option('--start',default=4,help='Starting hour for script to trigger, default 4 i.e. 4 AM')
@click.option('--finish',default=14,help='Ending hour for script to stop, default 14, i.e. 2 PM')
def run_script(url,start,finish):
    logging.info(f"Running job for {url}")
    while True:
        if time_check(start,finish):
            logging.info("Test is live, attempting to get data")
            raw_data = extract_data(url)
            tfmd_data = transform_data(raw_data)
            save_data(tfmd_data)
        else:
            logging.info("Test is not live.")
        
        logging.info("Sleeping for 2 mins")
        time.sleep(120)
    
    return

# --------------------------------------------------------------------------------------------
if __name__ == "__main__":
    run_script()