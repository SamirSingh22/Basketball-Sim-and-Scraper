from CSV_data import *
from matplotlib import pyplot as plt
import numpy as np
from operator import itemgetter

def graph_top_ten():
	player_list = read_data()
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
    for i in range(len(type_stats)):
        print('%d: %s' % (i, type_stats[i]))
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
            data = read_data(season, type_season[int(part_season)], type_stats[int(stat)])
        else:
	        data = read_data(season, type_season[int(part_season)], type_stats[int(stat)], data_type[int(per_type)])
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
        



