
from NBA_scraper import *
import csv
import os

per_type_list = ['traditional', 'misc', 'defense', 'opponent']

def csv_data_gen(data, year, part_season, stats, per_type):
	if part_season == 'Pre Season':
		part_season = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season = 'Regular_Season'
	with open('CSV_stats/%s/%s/%s/%s_data_%s.csv' % (year, part_season, stats, stats, per_type), mode='w') as player_data:
		fieldnames = list(data[10].keys())
		writer = csv.DictWriter(player_data, fieldnames=fieldnames)
		writer.writeheader()
		for player in data:
			try:
				writer.writerow(player)
			except:
				pass

def read_data_gen(year=None, part_season=None, stats=None, per_type=None):
	if year == None:
		year, part_season, stats, per_type = info_input(False)
	part_season_mod = part_season
	if part_season == 'Pre Season':
		part_season_mod = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season_mod = 'Regular_Season'

	if not os.path.isfile('CSV_stats/%s/%s/%s/%s_data_%s.csv' % (year, part_season_mod, stats, stats, per_type)):
		save_data_gen(year, part_season, stats, per_type)
	
	player_dict = {}
	player_list = []

	with open('CSV_stats/%s/%s/%s/%s_data_%s.csv' % (year, part_season_mod, stats, stats, per_type), mode='r') as player_data:
		csv_data = csv.DictReader(player_data)
		for row in csv_data:
			player_dict = dict(row)
			player_list.append(player_dict)
			
	return player_list

def save_data_gen(year, part_season, stats, per_type=None):
	data = []
	url = 'https://stats.nba.com/players/%s/?sort=PLAYER_NAME&dir=-1&Season=%s&SeasonType=%s' % (stats, year, part_season)
	if per_type is not None:
		url += '&PerMode=%s' % per_type
	print(url)
	try:
		data = stat_scraper(url, stats)
		csv_data_gen(data, year, part_season, stats, per_type)
	except Exception as e:
		print(repr(e))
		
def info_input(save=True):

	for i in range(len(type_stats_gen)):
		print('%d: %s' % (i, type_stats_gen[i]))
	stat = input('Type in a number corresponding to the stats you want: ')

	per_type = None
	if type_stats_gen[int(stat)] in per_type_list:
		for i in range(len(data_type)):
			print('%d: %s' % (i, data_type[i]))
		per_type = input('Type in a number corresponding to category you want: ')

	for i in range(len(type_season)):
		print('%d: %s' % (i, type_season[i]))
	part_season = input('Type in a number corresponding to the part of the season you want: ')

	for i in range(len(year_list)):
		print('%d: %s' % (i, year_list[i]))
	year = input('Type in a number corresponding to the year you want: ')

	if save:
		if per_type is None:
			save_data_gen(year_list[int(year)], type_season[int(part_season)], type_stats_gen[int(stat)])
		else:
			save_data_gen(year_list[int(year)], type_season[int(part_season)], type_stats_gen[int(stat)], data_type[int(per_type)])
	else:
		if per_type is None:
			return year_list[int(year)], type_season[int(part_season)], type_stats_gen[int(stat)], None
		else:
			return year_list[int(year)], type_season[int(part_season)], type_stats_gen[int(stat)], data_type[int(per_type)]
	return None

def is_data(year, part_season, stats, per_type=None):
	part_season_mod = part_season
	if part_season == 'Pre Season':
		part_season_mod = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season_mod = 'Regular_Season'
	
	if os.path.isfile('CSV_stats/%s/%s/%s/%s_data_%s.csv' % (year, part_season_mod, stats, stats, per_type)):
		return True
	return False

def all_years():

	for i in range(len(type_stats_gen)):
		print('%d: %s' % (i, type_stats_gen[i]))
	stat = input('Type in a number corresponding to the stats you want: ')

	per_type = None
	if int(stat) % 2 == 0:
		for i in range(len(data_type)):
			print('%d: %s' % (i, data_type[i]))
		per_type = input('Type in a number corresponding to category you want: ')

	for i in range(len(type_season)):
		print('%d: %s' % (i, type_season[i]))
	part_season = input('Type in a number corresponding to the part of the season you want: ')

	for season in year_list:
		if not is_data(season, type_season[int(part_season)], type_stats_gen[int(stat)], data_type[int(per_type)]):
			try:
				if per_type is None:
					save_data_gen(season, type_season[int(part_season)], type_stats_gen[int(stat)])
				else:
					save_data_gen(season, type_season[int(part_season)], type_stats_gen[int(stat)], data_type[int(per_type)])
			except Exception as e:
				print(repr(e))


def all_stats():

	for i in range(len(data_type)):
		print('%d: %s' % (i, data_type[i]))
	per_type = input('Type in a number corresponding to category you want: ')

	for i in range(len(type_season)):
		print('%d: %s' % (i, type_season[i]))
	part_season = input('Type in a number corresponding to the part of the season you want: ')

	for i in range(len(year_list)):
		print('%d: %s' % (i, year_list[i]))
	year = input('Type in a number corresponding to the year you want: ')

	for i, stat in enumerate(type_stats_gen):
		if not is_data(year_list[int(year)], type_season[int(part_season)], type_stats_gen[i], data_type[int(per_type)]):
			if int(year) < 10 and i == 4:
				continue
			try:
				if i % 2 == 1:
					save_data_gen(year_list[int(year)], type_season[int(part_season)], type_stats_gen[i])
				else:
					save_data_gen(year_list[int(year)], type_season[int(part_season)], type_stats_gen[i], data_type[int(per_type)])
			except Exception as e:
				print(repr(e))


"""
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
"""


