import requests
import os, sys, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser

def stat_scraper_general(url, type):
	driver = webdriver.Firefox()
	driver.get(url)
	player_dict_list = []
	while True:
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		stats = soup.find('div', attrs={'class':'nba-stat-table__overflow'})
		try:
			if type == 'traditional' or type == 'advanced' or type == 'estimated-advanced':
				player_stats_find = stats.find_all('tr', attrs={'data-ng-repeat':'(i, row) in page track by ::row.$hash'})
			else:
				player_stats_find = stats.find_all('tr', attrs={'data-ng-repeat':'(i, row) in page track by row.$hash'})
		except Exception as e:
			print(repr(e))
			sys.exit()
		type_stats = stats.find_all('th', attrs={'data-dir':'-1'})
		stat_name_list_app = ['PLAYER', 'TEAM', 'AGE']
		if type == 'opponent':
			stat_name_list_app = stat_name_list_app[:2]
		elif type == 'estimated-advanced':
			stat_name_list_app = stat_name_list_app[:1]
		stat_name_list = []
		pages = soup.find('div', attrs={'class':'stats-table-pagination__info'})
		tot_pages = pages.contents[2]
		tot_pages = int(tot_pages[8:])
		page_num = pages.find('option', attrs={'selected':'selected'})
		curr_page_num = int(page_num.contents[0])
		for stat in type_stats:
			stat_name_list.append(stat['data-field'])
		if type == 'opponent':
			stat_name_list = stat_name_list_app[:] + stat_name_list
			stat_name_list.append('PLUS_MINUS')
		else:
			stat_name_list = stat_name_list_app[:] + stat_name_list[:]
		for player in player_stats_find:
			stat_list = []
			player_dict = {}
			dws = 0
			if type == 'defense':
			    dws = player.find('span').contents[0]
			for stat in player:
				try:
					if stat.contents and stat.contents is not None:
						if stat.find('a').contents:
							stat_list.append(stat.find('a').contents[0])
						else:
							pass
				except:
					try:
						if stat.contents:
							stat_list.append(stat.contents[0])
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