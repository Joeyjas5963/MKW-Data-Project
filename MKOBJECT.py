# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import defaultdict

# constants to be used when S5 table bot data is implemented
COURSES = ['LC', 'MMM', 'MG', 'TF',
           'MC', 'CM', 'DKS', 'WGM',
           'DC', 'KC', 'MT', 'GV',
           'DDR', 'MH', 'BCWii', 'RR',
           'rPB', 'rYF', 'GV2', 'rMR',
           'rSL', 'SGB', 'rDS', 'rWS',
           'rDH', 'BC3', 'rJP', 'GCN MC',
           'MC3', 'rPG', 'DKM', 'rBC']

place_to_point = {1: 15,
                  2: 12,
                  3: 10,
                  4: 8,
                  5: 6,
                  6: 4,
                  7: 3,
                  8: 2,
                  9: 1,
                  10: 0,
                  None: 0,
                  -1: 0}


# ONE INSTANCE of a player (i.e. EmilP in match #7 against XI)
class Player():
    ''' object defining a single instance of a player in a given match

    Attributes:
        name (str): player name
        gp1/gp2/gp3 (int): score in each gp
        points (int): total points scored
        placement (int): placement in war
        team (str): team affiliation
        num (int): match this instance of player played in
        sum (bool): determines if att_clean should be run


    '''

    def __init__(self, name, gp1, gp2, gp3, points,
                 placement=0, team='', num=0, sum=False,
                 sub_in=False, sub_out=False):

        # creates list for att_clean
        check = [gp1, gp2, gp3, points, placement]

        # setting attributes
        self.name = name
        self.gp1 = gp1
        self.gp2 = gp2
        self.gp3 = gp3
        self.points = points
        self.placement = placement
        self.team = team
        self.num = num
        self.sub_in = sub_in
        self.sub_out = sub_out
        self.tag_name = self.team + ' ' + self.name

        # runs att_clean if told to
        if sum == False:
            self.att_clean(check)

    def __str__(self):

        return self.name

    def att_clean(self, check):
        ''' cleans data if there are empty spaces

        Arguments:
            check (list): list of inputs from __init__
        '''

        # checks if value can be converted to int
        for i in range(len(check)):
            try:
                check[i] = int(check[i])

            # if value error, change variable to -1
            except ValueError:
                check[i] = -1

        # resets attributes after cleaning
        self.gp1 = check[0]
        self.gp2 = check[1]
        self.gp3 = check[2]
        self.points = check[3]
        self.placement = check[4]

    def spread(self):
        ''' a more in-depth print of player object

        Arguments:
            None
        '''

        return [self.team, self.name, self.gp1, self.gp2, self.gp3,
                self.points, self.placement, self.sub_in]


# PLAYER THROUGHOUT SEASON (i.e. all of EmilP's score, places, etc.)
class PlayerAll(Player):
    ''' object that contains all stats a player has in a given season

    Attributes:
        name (str): player name
        team (str): team affiliation
        gp1/gp2/gp3 (list): list of all scores from respective gps
        points (list): list of scores from all matches
        placement (list): list of placements from all matches
        num (list): list of matches player played in
        sum (bool): checks to see if att_clean needs to be run
    '''

    def __init__(self, name, team, gp1, gp2, gp3, points, placement, num,
                 dict_id, sum=True,
                 avg=0):

        # creates player object
        Player.__init__(self=self, name=name, team=team, gp1=[gp1],
                        gp2=[gp2], gp3=[gp3], points=[points],
                        placement=[placement], num=[num], sum=sum)

        # sets player id
        self.dict_id = dict_id

    def update(self, player):
        ''' updates player_all object with new match info

        Arguments:
            player (player obj): player object from new match
        '''

        # adds new stats to player_all object
        self.num.append(player.num)
        self.gp1.append(player.gp1)
        self.gp2.append(player.gp2)
        self.gp3.append(player.gp3)
        self.points.append(player.points)
        self.placement.append(player.placement)

    def __str__(self):

        t = ''
        for team in self.team:
            t += team + ' '

        return self.name + '\n' + t


class PlayerAPI(Player):

    def __init__(self, name, gp1, gp2, gp3, points, fc,
                 mii, race_scores, race_positions, flag,
                 placement=None, team='', num=0, sum=False,):

        Player.__init__(self=self, name=name, team=team, gp1=gp1,
                        gp2=gp2, gp3=gp3, points=points,
                        placement=placement, num=num, sum=sum)

        self.fc = fc
        self.mii = mii
        self.race_scores = race_scores
        self.race_positions = race_positions
        self.flag = flag


class PlayerAPIALL(PlayerAPI):

    def __init__(self, name, tag_name, team, gp1, gp2, gp3, points, fc,
                 mii, race_scores, race_positions, flag, dict_id, base_id,
                 placement=0, fantasy='NA', fantasy_spread={}, num=0, sum=True):

        PlayerAPI.__init__(self, name=name, team=team, gp1=[gp1], gp2=[gp2], gp3=[gp3],
                   points=[points], fc=[fc], mii=[mii], race_scores=[race_scores],
                   race_positions=[race_positions], flag=flag,
                   placement=[placement], num=[num], sum=sum)

        self.tag_name = tag_name
        self.dict_id = dict_id
        self.base_id = base_id
        self.fantasy = fantasy
        self.fantasy_spread = fantasy_spread

    def update(self, player):
        ''' updates player_all object with new match info

        Arguments:
            player (player obj): player object from new match
        '''

        # adds new stats to player_all object
        self.num.append(player.num)
        self.gp1.append(player.gp1)
        self.gp2.append(player.gp2)
        self.gp3.append(player.gp3)
        self.points.append(player.points)
        self.fc.append(player.fc)
        self.placement.append(player.placement)
        self.race_scores.append(player.race_scores)
        self.race_positions.append(player.race_scores)

    def show_fantasy(self):

        print(self.name)
        for key, value in self.fantasy_spread.items():
            print(f'{key}: {value}')
        print(f'\nTotal: {self.fantasy}')


# ONE INSTANCE of a team (i.e. Daisy playing match #7 against XI)
class Team():
    ''' object that defines one instance of a team playing

    Attributes:
        name (str): team name
        gp1/gp2/gp3 (int): team gp scores
        pen (int): pens on team
        score (int): ending score
        players (list): list of player objects on team
        num (int): match team played
    '''

    def __init__(self, name, gp1, gp2, gp3, pen, score, players=[], num=0):

        # sets attributes
        self.name = name
        self.gp1 = gp1
        self.gp2 = gp2
        self.gp3 = gp3
        self.pen = pen
        self.score = score
        self.players = players
        self.num = num

    def __str__(self):
        string = ""

        for player in self.players:
            print(player)
            string += player.name + ", "

        string = string[:-2]

        return self.name + " Players: " + string


# TEAM THROUGHOUT SEASON (i.e. Daisy overall scores, t-points, etc.)
class TeamAll(Team):
    ''' object that contains total season data for team

    Attributes:
        name (str): team name
        gp1/gp2/gp3 (int): team gp scores
        pen (int): pens on team
        score (int): ending score
        players (list): list of player objects on team
        num (int): match team played
        roster (dict): number of appearances per player
    '''

    def __init__(self, name, gp1, gp2, gp3, pen, score, players, num, dict_id, base_id=0, roster={},
                 fantasy=0):

        # creates team object using inputs
        Team.__init__(self, name=name, gp1=[gp1], gp2=[gp2],
                      gp3=[gp3], pen=[pen], score=[score],
                      players=[players], num=[num])

        # sets team id
        self.dict_id = dict_id
        self.base_id = base_id
        self.roster = roster
        self.fantasy = fantasy
        self.roster_calc()

    def __str__(self):

        print(list(self.roster.keys()))

        return self.name

    def update(self, team):
        ''' updates team_all object with new team data

        Arguments:
            team (team object): team data to be added to team_all
        '''

        # add new inputs to team_all lists
        self.num.append(team.num)
        self.gp1.append(team.gp1)
        self.gp2.append(team.gp2)
        self.gp3.append(team.gp3)
        self.score.append(team.score)
        self.players.append(team.players)

    def roster_calc(self):
        ''' Creates roster dictionary

        Arguments:
            None
        '''

        # assigns defaultdict to roster
        roster = defaultdict(lambda: 0)

        # counts player appearances in matches
        for group in self.players:
            for player in group:
                roster[player.name] += 1

        self.roster = roster

        # creates dataframe of player appearances
        df = pd.Series(dict(roster)).sort_values(ascending=False)

        return df


# A match with team and player objects, same as spreadsheet
class Match():

    def __init__(self, name, date, num, t1, t2, t1t, t2t, t1p, t2p, players, dif, id, df=[],
                 perfect=False):

        self.name = name
        self.date = date
        self.num = num
        self.t1 = t1
        self.t2 = t2
        self.t1t = t1t
        self.t2t = t2t
        self.t1p = t1p
        self.t2p = t2p
        self.players = players
        self.dif = dif
        self.id = id
        self.df = self.match_df()

    def __repr__(self):

        print(self.name + ' ' + self.date)
        print(self.match_df())

        return '\n'

    def small_print(self):

        print(self.name, self.t1.name, self.t2.name)

    def match_df(self):

        columns = ['Team', 'Player', 'GP1', 'GP2', 'GP3', 'Total', 'Placement', 'Sub']
        full = []
        for player in self.t1.players:
            full.append(player.spread())
        for player in self.t2.players:
            full.append(player.spread())

        df = pd.DataFrame(full, columns=columns)

        df = df.sort_values(by='Total', ascending=False)
        medal = 0
        for i in range(len(df)):
            if not df.iloc[i, -1]:
                medal += 1
                df.iloc[i, -2] = medal
            else:
                df.iloc[i, -2] = 'Sub'

        if [self.t1.name, self.t2.name] == sorted([self.t1.name, self.t2.name]):
            asc = True
        else:
            asc = False

        df = df.sort_values(by=['Team', 'Total'], ascending=asc)
        df = df.iloc[:, :-1]

        return df


class MatchAPI(Match):

    def __init__(self, name, t1, t2, t1t, t2t, t1p, t2p, players, dif, id,
                 races, df=[]):

        Match.__init__(self=self, name=name, date='', num=0, t1=t1, t2=t2,
              t1t=t1t, t2t=t2t, t1p=t1p, t2p=t2p, players=players,
              dif=dif, id=id)

        self.races = races
        self.sub_check()

    def sub_check(self):

        for player in self.players:
            if player.sub_out:

                drop = player
                team_name = player.team

                if self.t1.name == team_name:
                    team = self.t1
                else:
                    team = self.t2

                for mate in team.players:
                    if drop.race_positions.count(None) + \
                            mate.race_positions.count(None) == 12 or \
                            drop.race_positions.count(-1) + \
                            mate.race_positions.count(-1) == 12:
                        if drop.race_positions != mate.race_positions:


                            print(drop)
                            print('Subbed Out')
                            print(drop.race_scores)
                            print(mate)
                            print('Subbed In')
                            print(mate.race_scores)

                            for i in range(len(drop.race_scores)):
                                drop.race_scores[i] = place_to_point[drop.race_positions[i]]

                            if drop.race_positions.count(-1) + mate.race_positions.count(-1) == 12:
                                after = len([i for i in drop.race_positions if i != -1])
                                drop.race_scores = drop.race_scores[:after] + list(np.zeros((12 - after), dtype=int))

                                drop.gp1 = sum(drop.race_scores[0:4])
                                drop.gp2 = sum(drop.race_scores[4:8])
                                drop.gp3 = sum(drop.race_scores[8:])

                            else:
                                after = len([i for i in drop.race_positions if i])

                            mate.race_scores = list(np.zeros(after, dtype=int)) + mate.race_scores[after:]

                            mate.gp1 = sum(mate.race_scores[0:4])
                            mate.gp2 = sum(mate.race_scores[4:8])
                            mate.gp3 = sum(mate.race_scores[8:])
                            mate.points = sum(mate.race_scores)
                            mate.sub_in = True
                            break




