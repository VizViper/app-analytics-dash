#!/usr/bin/env python
# coding: utf-8

# Importing Dependencies

from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint
import time
import os
import numpy as np
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
import psycopg2
import traceback
import sqlalchemy_utils



user = os.getenv('USER')
password = os.getenv('password')
db_pass = os.getenv('db_pass')
executable_path = {'executable_path': 'chromedriver.exe'}


browser = Browser('chrome', **executable_path, headless=True)


def checker(func,go=None):
    #func is a 'is_present' boolean
    for i in range(3):
        if func:
            go
            break
        else:
            browser.reload()
            time.sleep(2)

def pull_ios():
    try:
        #Visit the website in 'url'
        url = 'https://www.appannie.com/dashboard/home'
        browser.visit(url)

        #Enter login info
        time.sleep(2)
        browser.find_by_name(name = 'username').type(user)
        browser.find_by_css('input')[1].type(password)
        browser.find_by_tag('button').click()



        #SET THE NUMBER OF DAYS OF DATA TO EXTRACT -> USED FOR BOTH EXTRACTORS
        retro_days = 2

        #Check for presence of 'Top Chart' tab, click tab
        time.sleep(5)
        browser.find_by_text('Top Charts').click()

        #Create date range
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(retro_days)]


        #Grab the the top 300 rows of iOS app rankings from
        #https://www.appannie.com/apps/ios/top-chart?country=US&category=36&device=iphone&date=2020-12-01&feed=All&page_number=0&page_size=500&rank_sorting_type=rank
        #Create list of dictionaries, each one a different day
        list_of_builds = []
        checkindex = 0
        for moment in dates:
            #get top chart info
            url = f'https://www.appannie.com/headless/apps/ios/top-chart/?country=US&category=36&device=iphone&date={moment}&feed=All&rank_sorting_type=rank&market_slug=ios&page_number=0&page_size=300&headless=yes&table_selections='
            browser.visit(url)
            time.sleep(5)
            html = browser.html
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find('div', attrs = {'class':'aa-dashboard-table-container'})
            checker(browser.is_element_present_by_css('table'))
            all_trs = soup.table.tbody.find_all('tr')
            build_df = {'rank':[],'date': moment,'free':[],'paid':[],'grossing':[]}
            for _ in all_trs:
                current_rank_apps = [elem.text for elem in _.select('a span')]

                toss, app_id1, app_id2, app_id3 = [i.get('data-appid') for i in _.find_all('td')]

                rank_num = _.span.text
                build_df['rank'].append((rank_num))
                build_df['free'].append([current_rank_apps[0],current_rank_apps[1],app_id1])
                build_df['paid'].append([current_rank_apps[2],current_rank_apps[3],app_id2])
                build_df['grossing'].append([current_rank_apps[4],current_rank_apps[5],app_id3])

            list_of_builds.append(build_df)
            print(checkindex)
            checkindex += 1

        #concatenate all dataframes
        builds_to_concat = [pd.DataFrame(_).set_index('date') for _ in list_of_builds]
        pull = pd.concat(builds_to_concat)
    except Exception as e:
        browser.quit()
        print(e)
        traceback.print_exc()
    finally:
        browser.quit()

    return pull

def pull_android():
    try:

        #Visit the website in 'url'
        url = 'https://www.appannie.com/dashboard/home'
        browser.visit(url)

        #Enter login info
        time.sleep(1)
        browser.find_by_name(name = 'username').type(os.getenv('user'))
        browser.find_by_css('input')[1].type(os.getenv('password'))
        browser.find_by_tag('button').click()


        #Check for presence of 'Top Chart' tab, click tab
        time.sleep(5)
        browser.find_by_text('Top Charts').click()

        #Create date range
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(retro_days)]



        #https://www.appannie.com/apps/ios/top-chart?country=US&category=36&device=iphone&date=2020-12-01&feed=All&page_number=0&page_size=500&rank_sorting_type=rank
        #list of dictionaries, each one a different day
        list_of_builds = []

        for moment in dates:
            #get top chart info
            url = f'https://www.appannie.com/headless/apps/google-play/top-chart/?country=US&category=1&device=&date={moment}&feed=All&rank_sorting_type=rank&market_slug=google-play&page_number=0&page_size=300&headless=yes&table_selections='
            browser.visit(url)
            time.sleep(5)
            html = browser.html
            soup = BeautifulSoup(html,'html.parser')

            checker(browser.is_element_present_by_css('table'))

            all_trs = soup.table.tbody.find_all('tr')
            build_df = {'rank':[],'date': moment,'free':[],'paid':[],'grossing':[]}
            count = 0
            for _ in all_trs:
                current_rank_apps = [elem.text for elem in _.select('a span')]
                toss, app_id1, app_id2, app_id3, app_id4, app_id5 = [i.get('data-appid') for i in _.find_all('td')]

                rank_num = _.span.text
                #print(current_rank_apps)
                build_df['rank'].append((rank_num))
                build_df['free'].append([current_rank_apps[0],current_rank_apps[1],app_id1])
                build_df['paid'].append([current_rank_apps[2],current_rank_apps[3],app_id2])
                build_df['grossing'].append([current_rank_apps[4],current_rank_apps[5],app_id3])


            list_of_builds.append(build_df)

        #concatenate all dataframes
        builds_to_concat = [pd.DataFrame(_).set_index('date') for _ in list_of_builds]
        current_pull_google_play = pd.concat(builds_to_concat)
    except Exception as e:
        browser.quit()
        print(e)
        traceback.print_exc()
    finally:
        browser.quit()
    return current_pull_google_play

def check_publisher(element, element_list):
    if element not in element_list:
        element_list.append(element)

def check_app(element, cat, element_list, cat_list, lookup_table, pub_id_list, app_id_list):
    if element[2] not in element_list:
        element_list.append(element[0])
        cat_list.append(cat)
        app_id_list.append(element[2])
        pub_id_list.append(int(lookup_table[lookup_table['publisher_name'] == element[1]]['publisher_id']))

def check_pub_exec(new_df_list):
    publisher_list = []
    for df in new_df_list:
        for index, row in df.iterrows():
            check_publisher(row['free'][1], publisher_list)
            check_publisher(row['grossing'][1], publisher_list)
            check_publisher(row['paid'][1], publisher_list)

    return publisher_list


def partition(new_df_list):
    app_list = []
    cat_list = []
    pub_id = []
    app_id = []

    for df in new_df_list:
        for index, row in df.iterrows():
            # If the app is not in the list yet, insert it into the list and insert the category on the cat_list: 1(Free), 2(Grossing), 3(Paid)
            check_app(row['free'], 1, app_list, cat_list, df_publisher, pub_id, app_id)
            check_app(row['grossing'], 2, app_list, cat_list, df_publisher, pub_id, app_id)
            check_app(row['paid'], 3, app_list, cat_list, df_publisher, pub_id, app_id)
    return app_list, cat_list, pub_id, app_id


def scrubber_duck(new_df):
    df_free = pd.DataFrame(new_df['free'].to_list(), columns = ['app_name', 'publisher', 'app_id'])
    df_free_cleaned = new_df[['date','rank']].merge(df_free[['app_id']], left_index = True, right_index = True)
    df_free_cleaned['category_id'] = 1


    df_paid= pd.DataFrame(new_df['paid'].to_list(), columns = ['app_name', 'publisher', 'app_id'])
    df_paid_cleaned = new_df[['date','rank']].merge(df_paid[['app_id']], left_index = True, right_index = True)
    df_paid_cleaned['category_id'] = 3

    df_grossing = pd.DataFrame(new_df['grossing'].to_list(), columns = ['app_name', 'publisher', 'app_id'])
    df_grossing_cleaned = new_df[['date','rank']].merge(df_grossing[['app_id']], left_index = True, right_index = True)
    df_grossing_cleaned['category_id'] = 2


    df_full = df_free_cleaned.append(df_grossing_cleaned, ignore_index=True)
    df_full = df_full.append(df_paid_cleaned, ignore_index=True)
    return df_full


def make_platform():
    platform_dict = {'platform_id':[1,2], 'platform':['iOS','Android']}
    df_platform = pd.DataFrame(data = platform_dict)
    return df_platform

def make_cat():
    cat_dict = {'category_id':[1,2,3],'category':['Free','Grossing','Paid']}
    df_cat = pd.DataFrame(data=cat_dict)
    return df_cat



# In[ ]:
def main():
    browser = Browser('chrome', **executable_path, headless=True)
    current_pull_ios = pull_ios()
    browser = Browser('chrome', **executable_path, headless=True)
    current_pull_google_play = pull_android()

    df_ios_new = current_pull_ios.reset_index()
    df_android_new =  current_pull_google_play.reset_index()

    df_list = [df_ios_new,df_android_new]

    publisher_list = check_pub_exec(new_df_list=df_list)

    publisher_id = np.arange(1, len(publisher_list)+1)
    df_publisher = pd.DataFrame(zip(publisher_id, publisher_list), columns=['publisher_id','publisher_name'])

    app_list, cat_list, pub_id, app_id = partition(new_df_list=df_list)

    df_app = pd.DataFrame(zip(app_id, app_list, cat_list, pub_id), columns=['app_id','app_name','category_id','publisher_id'])
    df_app = df_app.drop_duplicates(subset=['app_id'], keep = 'first')

    df_full_ios = scrubber_duck(new_df = df_ios_new)
    df_full_android = scrubber_duck(new_df = df_android_new)
    df_full_ios['platform_id'] = 1
    df_full_android['platform_id'] = 2
    df_full = df_full_ios.append(df_full_android, ignore_index = True)

    df_platform = make_platform()
    df_cat = make_cat()
    
        # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    

    # Extract host and port from db_host
   # Uncomment and set the following variables depending on your specific instance and database:
    connection_name = "appannie-303104:us-central1:vizviper"
    db_name = os.environ("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASS")

# If your database is MySQL, uncomment the following two lines:
#driver_name = 'mysql+pymysql'
#query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

# If your database is PostgreSQL, uncomment the following two lines:
    driver_name = 'postgres+pg8000'
    query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

# If the type of your table_field value is a string, surround it with double quotes.

    engine = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ))
    try:
        
    df_platform.to_sql('platform',engine, if_exists='replace', index=False)
    df_full.to_sql('ranking',engine, if_exists='replace', index=True)
    df_publisher.to_sql('publisher',engine, if_exists='replace', index=False)
    df_app.to_sql('application', engine, if_exists='replace', index=False)
    df_cat.to_sql('category', engine, if_exists='replace', index=False)
    
     except Exception as e:
        return 'Error: {}'.format(str(e))
    return 'ok'

        # engine.execute("""
    #     ALTER TABLE
    #         platform
    #     ADD PRIMARY KEY
    #         (platform_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         category
    #     ADD PRIMARY KEY
    #         (category_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         publisher
    #     ADD PRIMARY KEY
    #         (publisher_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         application
    #     ADD PRIMARY KEY
    #         (app_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         application
    #     ADD CONSTRAINT
    #         fk_parent_category_id
    #     FOREIGN KEY
    #         (category_id)
    #     REFERENCES
    #         category
    #         (category_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         application
    #     ADD CONSTRAINT
    #         fk_parent_publisher_id
    #     FOREIGN KEY
    #         (publisher_id)
    #     REFERENCES
    #         publisher
    #         (publisher_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         ranking
    #     ADD PRIMARY KEY
    #         (index)
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         ranking
    #     ADD CONSTRAINT
    #         fk_parent_app_id
    #     FOREIGN KEY
    #         (app_id)
    #     REFERENCES
    #         application
    #         (app_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         ranking
    #     ADD CONSTRAINT
    #         fk_parent_category_id
    #     FOREIGN KEY
    #         (category_id)
    #     REFERENCES
    #         category
    #         (category_id);
    # """);
    #
    # engine.execute("""
    #     ALTER TABLE
    #         ranking
    #     ADD CONSTRAINT
    #         fk_parent_platform_id
    #     FOREIGN KEY
    #         (platform_id)
    #     REFERENCES
    #         platform
    #         (platform_id);
    # """);
    #



if __name__ == '__main__':
    main()
