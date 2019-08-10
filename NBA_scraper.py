import requests
import os, sys, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser

year_list = ['1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2007-08',
             '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19']
type_season = ['Pre Season', 'Regular Season', 'Playoffs']
data_type = ['Totals', 'PerGame', 'Per100Possessions', 'Per100Plays', 'Per48', 'Per40', 'Per36', 'PerMinute', 'PerPossession', 'PerPlay', 'MinutesPer']
type_stats_gen = ['traditional', 'advanced', 'estimated-advanced', 'misc', 'scoring', 'opponent', 'usage' , 'defense']
type_stats_shooting = ['By Zone', '5ft Range', '8ft Range']

def get_table(soup):
    table = soup.find('div', attrs={'class':'nba-stat-table__overflow'})
    return table

def get_player_stats(type_stat, soup):
    if type_stat in type_stats_gen[0:3]:
        return soup.find_all('tr', attrs={'data-ng-repeat':'(i, row) in page track by ::row.$hash'})
    elif type_stat in type_stats_gen:
        return soup.find_all('tr', attrs={'data-ng-repeat':'(i, row) in page track by row.$hash'})
    elif type_stat in type_stats_shooting:
        return soup.find_all('tr', attrs={'ng-repeat':'(i, row) in page', 'aria-hidden':'false'})
    return None

def stat_names(type_stat, soup):
    stat_name_list = []
    stat_name_list_app = ['PLAYER', 'TEAM', 'AGE']

    if type_stat in type_stats_gen:
        stats = soup.find_all('th', attrs={'data-dir':'-1'})
        for stat in stats:
            stat_name_list_app.append(stat['data-field'])
        if type == 'opponent':
            stat_name_list = stat_name_list_app[:2] + stat_name_list
            stat_name_list.append('PLUS_MINUS')
        elif type == 'estimated-advanced':
            stat_name_list_app = stat_name_list_app[:1] + stat_name_list
        else:
            stat_name_list = stat_name_list_app[:] + stat_name_list[:]
    elif type_stat in type_stats_shooting:
        all_stats = soup.find_all('tr', attrs={'aria-hidden':'false'})
        stats= all_stats[1].find_all(attrs={'class':'grouped'})
        for stat in stats:
            stat_name_list.append(stat['data-field'])
        stat_name_list = stat_name_list_app[:] + stat_name_list[:]
    return stat_name_list

def get_pages(soup):
    pages = soup.find('div', attrs={'class':'stats-table-pagination__info'})
    tot_pages = pages.contents[2]
    tot_pages = int(tot_pages[8:])
    page_num = pages.find('option', attrs={'selected':'selected'})
    curr_page_num = int(page_num.contents[0])
    return tot_pages, curr_page_num

def stat_scraper(url, type):
    driver = webdriver.Firefox()
    driver.get(url)
    player_dict_list = []
    if type in type_stats_shooting:
        time.sleep(10)
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        stats = get_table(soup)
        player_stats_find = get_player_stats(type, stats)
        stat_name_list = stat_names(type, stats)

        tot_pages, curr_page_num = get_pages(soup)
        
        for player in player_stats_find:
            stat_list = []
            player_dict = {}
            dws = 0
            if type == 'defense':
                dws = player.find('span').contents[0]
            for stat in player:
                try:
                    if stat.find('a'):
                        stat_list.append(stat.find('a').contents[0])
                    elif stat.contents:
                        stat_list.append(stat.contents[0])
                    else:
                        pass
                except:
                    pass
            for i, num in enumerate(stat_list):
                player_dict[stat_name_list[i]] = stat_list[i]
            if type == 'defense':
                player_dict[stat_name_list[len(stat_list) - 1]] = dws
            player_dict_list.append(player_dict)
        if tot_pages == curr_page_num:
            print('Returning stats of any players found...')
            break
        
        button = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]/i')
        button.click()
    driver.quit()
    return player_dict_list
