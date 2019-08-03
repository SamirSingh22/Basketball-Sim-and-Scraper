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



