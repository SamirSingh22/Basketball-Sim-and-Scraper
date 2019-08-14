from NBA_scraper import *
import csv

url_list = ['GeneralRange', 'ShotClockRange', 'DribbleRange', 'TouchTimeRange', 'CloseDefDistRange']
list_stat = list(type_stats_shot_dashboard.keys())

def csv_data_shot_dashboard(data, year, part_season, stat, type_stat, per_type='PerGame'):
	if part_season == 'Pre Season':
		part_season = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season = 'Regular_Season'

	type_stat = type_stat.replace(' ', '_')

	with open('CSV_stats/%s/%s/shot-dashboard/%s/%s_data_%s.csv' % (year, part_season, stat, type_stat, per_type), mode='w') as player_data:
		fieldnames = list(data[10].keys())
		writer = csv.DictWriter(player_data, fieldnames=fieldnames)
		writer.writeheader()
		for player in data:
			try:
				writer.writerow(player)
			except:
				pass



def save_data_shot_dashboard(year, part_season, stat, type_stat, per_type='PerGame'):
	id_num = list_stat.index(stat)
	if id_num == 5:
		id_num = 4
	stat_id = url_list[id_num]
	url = 'https://stats.nba.com/players/%s/?Season=%s&SeasonType=%s&%s=%s&sort=PLAYER_NAME&dir=-1' % (stat, year, part_season, stat_id, type_stat)
	data = stat_scraper(url, stat)
	csv_data_shot_dashboard(data, year, part_season, stat, type_stat, per_type)
	


def read_data_shot_dashboard(year, part_season, stat, type_stat, per_type='PerGame'):
	
	part_season_mod = part_season
	if part_season == 'Pre Season':
		part_season_mod = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season_mod = 'Regular_Season'

	if not is_data_shot_dashboard(year, part_season, stat, type_stat, per_type):
		save_data_shot_dashboard(year, part_season, stat, type_stat, per_type)
	
	player_dict = {}
	player_list = []

	type_stat = type_stat.replace(' ', '_')
	with open('CSV_stats/%s/%s/shot-dashboard/%s/%s_data_%s.csv' % (year, part_season, stat, type_stat, per_type), mode='r') as player_data:
		csv_data = csv.DictReader(player_data)
		for row in csv_data:
			player_dict = dict(row)
			player_list.append(player_dict)
			
	return player_list

def is_data_shot_dashboard(year, part_season, stat, type_stat, per_type='PerGame'):
	part_season_mod = part_season
	if part_season == 'Pre Season':
		part_season_mod = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season_mod = 'Regular_Season'
	type_stat = type_stat.replace(' ', '_')

	if os.path.isfile('CSV_stats/%s/%s/shot-dashboard/%s/%s_data_%s.csv' % (year, part_season, stat, type_stat, per_type)):
		return True
	return False
