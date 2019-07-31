from Player import *
from save_player_data import *
from random import randint
import os, sys
#1 is RA
#2 is paint but not in RA
#2 is midrange
#3 is a three
player = Player_Scrape(str(sys.argv[1] + ' ' + sys.argv[2]), int(sys.argv[3]))


def typeshot(player):
    num = randint(0, 100)
    if(num < player.RA_PREF):
        return 'RA_PCT'
    if(num < (player.RA_PREF + player.PAINT_NON_RA_PREF)):
        return 'PAINT_NON_RA_PCT'
    if(num < (player.RA_PREF + player.PAINT_NON_RA_PREF + player.MID_RANGE_PREF)):
        return 'MID_RANGE_PCT'
    return 'THREE_PCT'

def makeshot(player, shot):
    num = randint(0, 100)
    if num < player.stat_dict[shot] and shot == 'THREE_PCT':
        return 3
    if num < player.stat_dict[shot]:
        return 2
    return 0

def sim(player, point_limit):
    points = 0
    FGA = 0
    FGM = 0
    THREE_FGA = 0
    THREE_FGM = 0
    print_list_good = [player.name + ' made a layup for 2 points!', player.name + ' made a shot in the paint for 2 points!',
    player.name + ' made a midrange shot for 2 points!', player.name + ' made a three for 3 points!']
    print_list_bad = [player.name + ' missed a layup!', player.name + ' missed a shot in the paint!', 
    player.name + ' missed a midrange shot!', player.name + ' missed a three!']
    while points < point_limit:
        shot = typeshot(player)
        bucket = makeshot(player, shot)
        FGA += 1
        if bucket:
            FGM += 1
            if shot == 'RA_PCT':
                print(print_list_good[0])
                points += 2
            elif shot == 'PAINT_NON_RA_PCT':
                print(print_list_good[1])
                points += 2
            elif shot == 'MID_RANGE_PCT':
                print(print_list_good[2])
                points += 2
            else:
                THREE_FGA += 1
                THREE_FGM += 1
                print(print_list_good[3])
                points += 3
        else:
            if shot == 'RA_PCT':
                print(print_list_bad[0])
            elif shot == 'PAINT_NON_RA_PCT':
                print(print_list_bad[1])
            elif shot == 'MID_RANGE_PCT':
                print(print_list_bad[2])
            else:
                THREE_FGA += 1
                print(print_list_bad[3])
    if THREE_FGA == 0:
        print(player.name + ' scored ' + str(points) + ' points on %d/%d (%.2f%%) shooting and %d/%d from three!' % (FGM, FGA, (100*(float(FGM)/FGA)), THREE_FGM, THREE_FGA))
    else:
        print(player.name + ' scored ' + str(points) + ' points on %d/%d (%.2f%%) shooting and %d/%d (%.2f%%) from three!' % (FGM, FGA, (100*(float(FGM)/FGA)), THREE_FGM, THREE_FGA, (100*(float(THREE_FGM)/THREE_FGA))))
    print(player.name + ' usually shoots ' + player.player_stats_trad['FG3_PCT'] + '%' + ' from three')
    print(player.name + ' usually shoots ' + player.player_stats_trad['FG_PCT'] + '%' + ' from the field')
sim(player, int(sys.argv[4]))

