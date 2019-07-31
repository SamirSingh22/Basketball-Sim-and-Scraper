from scraper import *
import csv
import os

def csv_data(data, type_stats, year, season_type, data_type):
	with open('Player_Data/%s_data_%s_%s_%s.csv' % (type_stats, year, season_type, data_type), mode='w') as player_data:
		fieldnames = list(data[10].keys())
		writer = csv.DictWriter(player_data, fieldnames=fieldnames)
		writer.writeheader()
		for player in data:
			try:
				if type_stats is not 'opponent':
					num = int(player['AGE'])
				writer.writerow(player)
			except:
				pass

def read_player_data():
	player_name, year, season, type_data, stats = data_input(True)
	player_dict = {}
	if not os.path.isfile('Player_Data/%s_data_%s_%s_%s.csv' % (stats, year, season, type_data)):
		input_and_save_data(year, season, stats, type_data)
	with open('Player_Data/%s_data_%s_%s_%s.csv' % (stats, year, season, type_data), mode='r') as player_data:
		csv_data = csv.DictReader(player_data)
		for row in csv_data:
			if row['PLAYER'] == player_name:
				player_dict = dict(row)
	return player_dict

def read_player_data_sim(player_name, year_in):
	year_str = str(year_in)
	if str(year_in)[3] == '9':
		year_end_str = '0'
	else:
		year_end_str = str(int(year_str[3]) + 1)
	year = year_str + '-' + year_str[2] + year_end_str
	season = 'Regular Season'
	type_data_trad = 'PerGame'
	type_data_shoot = 'zone'

	player_dict_trad = {}
	player_dict_shoot = {}

	if not os.path.isfile('Player_Data/%s_data_%s_%s_%s.csv' % ('traditional', year, season, type_data_trad)):
		input_and_save_data(year, season, 'traditional', type_data_trad)
	if not os.path.isfile('Player_Data/%s_data_%s_%s_%s.csv' % ('shooting', year, season, type_data_shoot)):
		input_and_save_data(year, season, 'shooting', type_data_shoot)
	with open('Player_Data/%s_data_%s_%s_%s.csv' % ('traditional', year, season, type_data_trad), mode='r') as player_data:
		csv_data = csv.DictReader(player_data)
		for row in csv_data:
				player_dict_trad = dict(row)
	with open('Player_Data/%s_data_%s_%s_%s.csv' % ('shooting', year, season, type_data_shoot), mode='r') as player_data:
		csv_data = csv.DictReader(player_data)
		for row in csv_data:
			if row['PLAYER'] == player_name:
				player_dict_shoot = dict(row)
	return player_dict_trad, player_dict_shoot

def input_and_save_data(year, season, stats, type_data=None):
	
	data = []

	if stats == 'traditional' or stats == 'scoring' or stats == 'misc' or stats == 'opponent' or stats == 'defense':
		url = 'https://stats.nba.com/players/%s/?sort=PLAYER_NAME&dir=-1&Season=%s&SeasonType=%s&PerMode=%s' % (stats, year, season, type_data)
		data = stat_scraper_all(url, stats)

	elif stats == 'shooting':
		extra_data = ''
		if type_data == 'zone':
			extra_data = '&DistanceRange=By Zone'
		elif type_data == '5ft':
			extra_data = '&DistanceRange=5ft Range'
		else:
			extra_data = '&DistanceRange=8ft Range'
		url = 'https://stats.nba.com/players/shooting/?sort=PLAYER_NAME&dir=-1&Season=%s&SeasonType=%s%s' % (year, season, extra_data)

		data = stat_scraper_all(url, type_data)
	elif stats == 'advanced' or stats == 'usage':
		url = 'https://stats.nba.com/players/%s/?sort=PLAYER_NAME&dir=-1&Season=%s&SeasonType=%s' % (stats, year, season)
		data = stat_scraper_all(url, stats)

	csv_data(data, stats, year, season, type_data)

def data_input(player):
	year_list = ['1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2007-08',
	 '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19']
	type_season = ['Preseason', 'Regular Season', 'Playoffs']
	data_type = ['Totals', 'PerGame', 'Per100Pos', 'Per100Plays', 'Per48', 'Per40', 'Per36', 'PerMinute', 'PerPos', 'PerPlay', 'MinutesPer', 'zone', '5ft', '8ft']
	type_stats = ['scoring', 'traditional', 'shooting']

	print('Pick a number corresponding to a season:')
	for i in range(len(year_list)):
		print(str(i + 1) + ': ' + year_list[i])
	year = int(input('Input: ')) - 1

	print('Pick a number corresponding to a part of a season:')
	for i in range(len(type_season)):
		print(str(i + 1) + ': ' + type_season[i])
	season_type = int(input('Input: ')) - 1

	print('Pick a number corresponding to how you want the stats formatted:')
	for i in range(len(data_type)):
		print(str(i + 1) + ': ' + data_type[i])
	dat = int(input('Input: ')) - 1

	if dat > 10:
		typ = 2
	else:
		print('Pick a number corresponding to which type of stats you want:')
		for i in range(len(type_stats)):
			print(str(i + 1) + ': ' + type_stats[i])
		typ = int(input('Input: ')) - 1

	if player:
		print('Type in the name of the player you want stats of')
		player_name = input('Input: ')
		return player_name, year_list[year], type_season[season_type], data_type[dat], type_stats[typ]

	return year_list[year], type_season[season_type], data_type[dat], type_stats[typ]