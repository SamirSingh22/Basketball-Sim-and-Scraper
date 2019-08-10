from CSV_data_gen import *
from CSV_data_shooting import *
from matplotlib import pyplot as plt
import numpy as np
from collections import OrderedDict
from operator import itemgetter


def find_player(player_name, data):
    for player in data:
        if player['PLAYER'] == player_name:
            return player
    return None

def graph_top_ten():
	player_list = read_data_gen()
	stat_names = list(player_list[0].keys())
	for i, key in enumerate(stat_names):
		print('%s: %s' % (str(i), key))
	user_in = input('Pick a number corresponding to which statistic you want: ')
	stat = stat_names[int(user_in)]
	stats_list_dict = []
	for player in player_list:
		if int(player['GP']) > 40:
			stat_dict = {
			'PLAYER': player['PLAYER'],
			stat: float(player[stat])
			}
			stats_list_dict.append(stat_dict)
	stats_graph = sorted(stats_list_dict, reverse=True, key=itemgetter(stat))[:10]
	top_players = []
	top_stats = []
	for player in stats_graph:
		top_players.append(player['PLAYER'])
		top_stats.append(player[stat])
	y_pos = np.arange(10)
	plt.figure(figsize=(20, 10))
	plt.bar(y_pos, top_stats,align='center')
	plt.xticks(y_pos, top_players)
	plt.ylabel(stat)
	plt.title('Top 10 Players in %s' % stat)
	plt.show()

def graph_stats_over_time(player_name):
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
    player_stats_list = []
    years = []
    for season in year_list:
        data = []
        if per_type is None:
            data = read_data_gen(season, type_season[int(part_season)], type_stats_gen[int(stat)])
        else:
	        data = read_data_gen(season, type_season[int(part_season)], type_stats_gen[int(stat)], data_type[int(per_type)])
        for player in data:
            if player['PLAYER'] == player_name:
                years.append(season)
                player_stats_list.append(player)
    stat_names = list(player_stats_list[0].keys())
    for i in range(len(stat_names)):
        print('%s: %s' % (str(i), stat_names[i]))
    inp = input('Type the number corresponding to which stat you want: ')
    stat_in = stat_names[int(inp)]
    graph_dict = {}
    for i, player_season in enumerate(player_stats_list):
        graph_dict[years[i]] = float(player_season[stat_in])
    plt.plot(np.arange(len(years)), list(graph_dict.values()))
    plt.xticks(np.arange(len(years)), years, rotation='vertical')
    plt.xlabel('Seasons')
    plt.ylabel(stat_in)
    plt.title(player_name)
    plt.show()
        


def plot_shot_efficiency(player_name, season, part_season, dist_range):
    data = read_data_shooting(season, part_season, dist_range)
    player = find_player(player_name, data)
    list_keys = list(player.keys())
    dict_list = []
    for i in range(5, len(list_keys), 3):
        dict_data = {}
        if str(list_keys[i]) == 'Corner 3 FG PCT':
            continue
        key = list_keys[i]
        key_data = player[key]
        dict_data[key[:-6]] = key_data
        eff_data = 0
        if '3' in str(list_keys[i]):
            eff_data = round(float(key_data)*3 / 100, 2)
        else:
            eff_data = round(float(key_data)*2 / 100, 2)
        dict_data['Points Per Shot'] = eff_data
        dict_list.append(dict_data)
   
    sorted_stats = sorted(dict_list, reverse=True, key=itemgetter('Points Per Shot'))
    
    sorted_pts_per_shot = []
    sorted_names = []
    for stat_dict in sorted_stats:
        sorted_pts_per_shot.append(stat_dict['Points Per Shot'])
        sorted_names.append(list(stat_dict.keys())[0])
    
    y_pos = np.arange(len(sorted_names))
    plt.figure(figsize=(12, 8))
    plt.bar(y_pos, sorted_pts_per_shot,align='center')
    plt.xticks(y_pos, sorted_names)
    plt.ylabel('Points Per Shot')
    plt.xlabel('Type of Shot')
    plt.title('Efficiency of Shots by %s' % player_name)
    plt.show()

def ESV(season, part_season):
    data_shooting = read_data_shooting(season, part_season, 'By Zone')
    data_gen = read_data_gen(season, part_season, 'traditional', 'PerGame')
    list_ESV = []
    key_list_shooting = list(data_shooting[0].keys())
    ESV_list_dict = []
    print(season)
    for i, player in enumerate(data_shooting):
        player_gen = data_gen[i]
        ESV_dict = {}
        ESV_dict['PLAYER'] = player['PLAYER']
        ESV = 0
        FGA = 0
        print(player['PLAYER'])
        try:
            t = float(player['PLAYER'])
            continue
        except:
            pass
        for i in range(4, len(key_list_shooting), 3):
            key = key_list_shooting[i]
            if str(key) == 'Corner 3 FGA' or str(player[key]) == '-':
                continue

            FGA += float(player[key])

        if part_season == 'Regular Season' and (FGA < 5.0 or int(player_gen['GP']) < 20):
            continue
        else:
            if FGA < 5.0:
                continue
        for i in range(5, len(key_list_shooting), 3):
            data_name = key_list_shooting[i]
            eff_data = 0
            if str(data_name) == 'Corner 3 FG PCT' or str(player[data_name]) == '-':
                continue
            elif '3' in data_name:
                eff_data = float(player[data_name])*3 / 100
            else:
                eff_data = float(player[data_name])*2 / 100
            try:
                ESV += eff_data * (float(player[key_list_shooting[i-1]])/FGA)
            except:
                break
        ESV = round(ESV * 10, 2)
        ESV_dict['ESV'] = ESV
        ESV_list_dict.append(ESV_dict)
    sorted_ESV = sorted(ESV_list_dict, reverse=True, key=itemgetter('ESV'))

    part_season_mod = part_season
    if part_season == 'Pre Season':
        part_season_mod = 'Pre_Season'
    elif part_season == 'Regular Season':
        part_season_mod = 'Regular_Season'

    with open('ESV/%s/ESV_data_%s.csv' % (part_season_mod, season), mode='w') as ESV_csv:
        fieldnames = list(sorted_ESV[0].keys())
        writer = csv.DictWriter(ESV_csv, fieldnames=fieldnames)
        writer.writeheader()
        for player in sorted_ESV:
            try:
                writer.writerow(player)
            except:
                pass
    return sorted_ESV

def read_ESV(year, part_season):
    part_season_mod = part_season
    if part_season == 'Pre Season':
        part_season_mod = 'Pre_Season'
    elif part_season == 'Regular Season':
        part_season_mod = 'Regular_Season'

    if not os.path.isfile('ESV/%s/ESV_data_%s.csv' % (part_season_mod, year)):
        ESV(year, part_season)

    ESV_dict = {}
    ESV_list = []
    with open('ESV/%s/ESV_data_%s.csv' % (part_season_mod, year)) as ESV_data:
        csv_data = csv.DictReader(ESV_data)
        for row in csv_data:
            ESV_dict = dict(row)
            ESV_list.append(ESV_dict)
    return ESV_list

def plot_ESV(player_name, part_season='Regular Season'):
    ESV_year_list = []
    years = []
    for year in year_list:
        ESV_year = read_ESV(year, part_season)
        for player in ESV_year:
            if player['PLAYER'] == player_name:
                years.append(year)
                ESV_year_list.append(player)
    ESV_list = []
    for stat in ESV_year_list:
        ESV_list.append(float(stat['ESV']))
    plt.plot(np.arange(len(years)), ESV_list)
    plt.xticks(np.arange(len(years)), years, rotation='vertical')
    plt.xlabel('Seasons')
    plt.ylabel('Efficient Shot Value')
    plt.title(player_name + ' ESV Over Time')
    plt.show()

        