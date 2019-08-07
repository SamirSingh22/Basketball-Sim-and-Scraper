from NBA_scraper import *
import csv


def csv_data_shooting(data, year, part_season, dist_range, per_type='PerGame'):
	if part_season == 'Pre Season':
		part_season = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season = 'Regular_Season'

	dist_range = dist_range.replace(' ', '_')

	with open('CSV_stats/%s/%s/shooting/%s_data_%s.csv' % (year, part_season, dist_range, per_type), mode='w') as player_data:
		fieldnames = list(data[10].keys())
		writer = csv.DictWriter(player_data, fieldnames=fieldnames)
		writer.writeheader()
		for player in data:
			try:
				writer.writerow(player)
			except:
				pass



def save_data_shooting(year, part_season, dist_range, per_type='PerGame'):
	url = 'https://stats.nba.com/players/shooting/?sort=PLAYER_NAME&dir=-1&SeasonType=%s&PerMode=%s&DistanceRange=%s&Season=%s' % (part_season, per_type, dist_range, year)
	data = stat_scraper(url, dist_range)
	csv_data_shooting(data, year, part_season, dist_range, per_type)
	


def read_data_shooting(year, part_season, dist_range, per_type='PerGame'):
	
	part_season_mod = part_season
	if part_season == 'Pre Season':
		part_season_mod = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season_mod = 'Regular_Season'

	if not is_data_shooting(year, part_season, dist_range, per_type):
		save_data_shooting(year, part_season, dist_range, per_type)
	
	player_dict = {}
	player_list = []

	dist_range = dist_range.replace(' ', '_')
	with open('CSV_stats/%s/%s/shooting/%s_data_%s.csv' % (year, part_season_mod, dist_range, per_type), mode='r') as player_data:
		csv_data = csv.DictReader(player_data)
		for row in csv_data:
			player_dict = dict(row)
			player_list.append(player_dict)
			
	return player_list

def is_data_shooting(year, part_season, dist_range, per_type='PerGame'):
	part_season_mod = part_season
	if part_season == 'Pre Season':
		part_season_mod = 'Pre_Season'
	elif part_season == 'Regular Season':
		part_season_mod = 'Regular_Season'
	dist_range = dist_range.replace(' ', '_')

	if os.path.isfile('CSV_stats/%s/%s/shooting/%s_data_%s.csv' % (year, part_season_mod, dist_range, per_type)):
		return True
	return False
