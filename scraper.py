import requests
import os, sys, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser, pyperclip

def stat_scraper_general(url, type):
	driver = webdriver.Firefox()
	driver.get(url)
	player_dict_list = []
	while True:
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		stats = soup.find('div', attrs={'class':'nba-stat-table__overflow'})
		string = ''
		data = ''
		if type == 'traditional':
			string = ' track by ::row.$hash'
			data = 'data-'
		elif type == 'scoring':
			string = ' track by row.$hash'
			data = 'data-'
		player_stats = stats.find_all('tr', attrs={'%sng-repeat' % data:'(i, row) in page%s' % string})
		type_stats = stats.find_all('th', attrs={'data-dir':'-1'})
		stat_name_list = ['PLAYER', 'TEAM', 'AGE']
		pages = soup.find('div', attrs={'class':'stats-table-pagination__info'})
		tot_pages = pages.contents[2]
		tot_pages = int(tot_pages[8:])
		page_num = pages.find('option', attrs={'selected':'selected'})
		curr_page_num = int(page_num.contents[0])
		for stat in type_stats:
			stat_name_list.append(stat['data-field'])
		for player in player_stats:
			stat_list = []
			player_dict = {}
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

						elif stat:
							pass
					except:
						pass
			for i, num in enumerate(stat_list):
				player_dict[stat_name_list[i]] = stat_list[i]
			player_dict_list.append(player_dict)
		if tot_pages == curr_page_num:
			print('Returning stats of any players found...')
			break
		
		button = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]/i')
		button.click()
	return player_dict_list

def stat_scraper_shooting(url, type):
	driver = webdriver.Firefox()
	driver.get(url)
	player_dict_list = []
	time.sleep(10)
	while True:
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		stats = soup.find('div', attrs={'class':'nba-stat-table__overflow'})
		try:
			if type == '5ft':
				player_stats = stats.find_all('tr', attrs={'ng-show':'params.DistanceRange===\'5ft Range\''})
			elif type == 'zone':
				player_stats = stats.find_all('tr', attrs={'ng-show':'params.DistanceRange===\'By Zone\''})
			elif type == '8ft':
				player_stats = stats.find_all('tr', attrs={'ng-show':'params.DistanceRange===\'8ft Range\''})
		except Exception as e:
			print(repr(e))
			sys.exit()
		type_stats = stats.find_all('th', attrs={'class':'grouped'})
		stat_name_list_app = ['PLAYER', 'TEAM', 'AGE']
		stat_name_list = []
		pages = soup.find('div', attrs={'class':'stats-table-pagination__info'})
		tot_pages = pages.contents[2]
		tot_pages = int(tot_pages[8:])
		page_num = pages.find('option', attrs={'selected':'selected'})
		curr_page_num = int(page_num.contents[0])
		for stat in type_stats:
			stat_name_list.append(stat['data-field'])
		if type == '5ft':
			stat_name_list = stat_name_list_app[:] + stat_name_list[:18]
		elif type == 'zone':
			stat_name_list = stat_name_list_app[:] + stat_name_list[33:]
		elif type == '8ft':
			stat_name_list = stat_name_list_app[:] + stat_name_list[18:33]
		for player in player_stats:
			stat_list = []
			player_dict = {}
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

						elif stat:
							pass
					except:
						pass
			for i, num in enumerate(stat_list):
				player_dict[stat_name_list[i]] = stat_list[i]
			player_dict_list.append(player_dict)
		if tot_pages == curr_page_num:
			print('Returning stats of any players found...')
			break
		
		button = driver.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/a[2]/i')
		button.click()
	return player_dict_list



def stat_scraper_all(url, type):
	driver = webdriver.Firefox()
	driver.get(url)
	player_dict_list = []
	while True:
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		stats = soup.find('div', attrs={'class':'nba-stat-table__overflow'})
		try:
			if type == '5ft':
				player_stats_find = stats.find_all('tr', attrs={'ng-show':'params.DistanceRange===\'5ft Range\''})
			elif type == 'zone':
				player_stats_find = stats.find_all('tr', attrs={'ng-show':'params.DistanceRange===\'By Zone\''})
			elif type == '8ft':
				player_stats_find = stats.find_all('tr', attrs={'ng-show':'params.DistanceRange===\'8ft Range\''})
			elif type == 'traditional' or type == 'advanced' or type == 'estimated-advanced':
				player_stats_find = stats.find_all('tr', attrs={'data-ng-repeat':'(i, row) in page track by ::row.$hash'})
			elif type == 'scoring' or type == 'misc' or type == 'usage' or type == 'opponent' or type == 'defense':
				player_stats_find = stats.find_all('tr', attrs={'data-ng-repeat':'(i, row) in page track by row.$hash'})
		except Exception as e:
			print(repr(e))
			sys.exit()
		if type == '5ft' or type == 'zone' or type == '8ft':
			type_stats = stats.find_all('th', attrs={'class':'grouped'})
		else:
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
		if type == '5ft':
			stat_name_list = stat_name_list_app[:] + stat_name_list[:18]
		elif type == 'zone':
			stat_name_list = stat_name_list_app[:] + stat_name_list[33:]
		elif type == '8ft':
			stat_name_list = stat_name_list_app[:] + stat_name_list[18:33]
		elif type == 'opponent':
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