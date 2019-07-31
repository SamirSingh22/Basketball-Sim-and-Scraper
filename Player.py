from random import *
from scraper import *
from save_player_data import *

class Player_Scrape:
	def __init__(self, name, year):
		self.name = name
		self.year = year
		self.player_stats_trad, self.player_stats_shooting = read_player_data_sim(self.name, self.year)

		self.RA_PCT = float(self.player_stats_shooting['Restricted Area FG PCT'])
		self.PAINT_NON_RA_PCT = float(self.player_stats_shooting['In The Paint (Non-RA) FG PCT'])
		self.MID_RANGE_PCT = float(self.player_stats_shooting['Mid-Range FG PCT'])
		self.THREE_PCT = float(self.player_stats_trad['FG3_PCT'])
		self.RA_PREF = round((float(self.player_stats_shooting['Restricted Area FGA'])/float(self.player_stats_trad['FGA']))*100, 1)
		self.PAINT_NON_RA_PREF = round((float(self.player_stats_shooting['In The Paint (Non-RA) FGA'])/float(self.player_stats_trad['FGA']))*100, 1)
		self.MID_RANGE_PREF = round((float(self.player_stats_shooting['Mid-Range FGA'])/float(self.player_stats_trad['FGA']))*100, 1)
		self.THREE_PREF = round((float(self.player_stats_trad['FG3A'])/float(self.player_stats_trad['FGA']))*100, 1)
		
		self.stat_dict = {
		'RA_PCT' : self.RA_PCT,
		'PAINT_NON_RA_PCT' : self.PAINT_NON_RA_PCT,
		'MID_RANGE_PCT' : self.MID_RANGE_PCT,
		'THREE_PCT' : self.THREE_PCT,
		'RA_PREF' : self.RA_PREF,
		'PAINT_NON_RA_PREF' : self.PAINT_NON_RA_PREF,
		'MID_RANGE_PREF' : self.MID_RANGE_PREF,
		'THREE_PREF' : self.THREE_PREF
		}

		

"""

class Player:
    def __init__(self, name, age, height, weight, specialty, defense, ball_handling):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.specialty = specialty
        self.defense = defense
        self.ball_handling = ball_handling
        self.stats = Stats(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        if(specialty == 'sharpshooter'):
            self.layup_pref = 25.0
            self.layup_perc = 50.0
            self.mid_pref = 25.0
            self.mid_perc = 50.0
            self.three_pref = 50.0
            self.three_perc = 40.0
        elif(specialty == 'post'):
            self.layup_pref = 60.0
            self.layup_perc = 65.0
            self.mid_pref = 30.0
            self.mid_perc = 40.0
            self.three_pref = 10.0
            self.three_perc = 20.0
        elif(specialty == 'midrange'):
            self.layup_pref = 25.0
            self.layup_perc = 50.0
            self.mid_pref = 50.0
            self.mid_perc = 60.0
            self.three_pref = 25.0
            self.three_perc = 30.0
        elif(specialty == 'random'):
            self.layup_pref = randint(10, 75)
            self.layup_perc = randint(40, 75)
            if self.layup_pref >= 50:
            	self.mid_pref = randint(5, 20)
            else:
            	self.mid_pref = randint(20, 50)
            self.mid_perc = randint(30, 60)
            self.three_pref = 100 - self.mid_pref - self.layup_pref
            self.three_perc = randint(20, 50)

        self.player_abilities = {
            "% of shots layups": self.layup_pref,
            "% of shots midrange": self.mid_pref,
            "% of shots threes": self.three_pref,
            "layup %": self.layup_perc,
            "midrange %": self.mid_perc,
            "three %": self.three_perc
        }

        

        self.player_perc = [self.layup_perc, self.mid_perc, self.three_perc]
        self.player_pref = [self.layup_pref, self.mid_pref, self.three_pref]

    def abilities(self):
        print(self.player_abilities)


    def intro(self):
        print("Introducing " + self.name + " who is " + str(self.weight) + " pounds and stands " + self.height)
    def specialty_stats(self):
        print("Will go for layups " + str(self.layup_pref) + " percent of the time, mid range for " + str(self.mid_pref) +
              " percent of the time, and threes " + str(self.three_pref) + " percent of the time.")
"""
class Stats:
    def __init__(self, Points, Rebounds, Assists, Steals, Blocks, Turnovers, FGA, FGM, THREEPM, THREEPA):
        self.Stats = {
            "Points": Points,
            "Rebounds": Rebounds,
            "Assists": Assists,
            "Steals": Steals,
            "Blocks": Blocks,
            "Turnovers": Turnovers,
            "FGM": FGM,
            "FGA": FGA,
            "3PA": THREEPA,
            "3PM": THREEPM
        }
        self.Points = self.Stats["Points"]
        self.Rebounds = self.Stats["Rebounds"]
        self.Assists = self.Stats["Rebounds"]
        self.Steals = self.Stats["Steals"]
        self.Blocks = self.Stats["Blocks"]
        self.Turnovers = self.Stats["Turnovers"]
        self.FGA = self.Stats["FGA"]
        self.FGM = self.Stats["FGM"]
        self.THREEPM = self.Stats["3PM"]
        self.THREEPA = self.Stats["3PA"]

    def get_stats(self):
        stats_string = {
            "Points": str(self.Stats["Points"]),
            "Rebounds": str(self.Stats["Rebounds"]),
            "Assists": str(self.Stats["Assists"]),
            "Steals": str(self.Stats["Steals"]),
            "Blocks": str(self.Stats["Blocks"]),
            "Turnovers": str(self.Stats["Turnovers"]),
            "FGM/FGA": str(self.Stats["FGM"]) + "/" + str(self.Stats["FGA"]),
            "3PM/3PA": str(self.Stats["3PM"]) + "/" + str(self.Stats["3PA"])
        }
        print(stats_string)