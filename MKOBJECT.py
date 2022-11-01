# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import defaultdict

COURSES = ['LC', 'MMM', 'MG', 'TF',
           'MC', 'CM', 'DKS', 'WGM',
           'DC', 'KC', 'MT', 'GV',
           'DDR', 'MH', 'BCWii', 'RR',
           'rPB', 'rYF', 'GV2', 'rMR',
           'rSL', 'SGB', 'rDS', 'rWS',
           'rDH', 'BC3', 'rJP', 'GCN MC',
           'MC3', 'rPG', 'DKM', 'rBC']

POINTS = [15, 12, 10, 8, 6, 4, 3, 2, 1, 0]


class Player():

    def __init__(self, name, gp1, gp2, gp3, points, placement, team='', num=0, sum=False):

        check = [gp1, gp2, gp3, points, placement]

        self.name = name
        self.gp1 = gp1
        self.gp2 = gp2
        self.gp3 = gp3
        self.points = points
        self.placement = placement
        self.team = team
        self.num = num

        if sum == False:
            self.att_clean(check)

    def __str__(self):

        return self.name

    def att_clean(self, check):

        for i in range(len(check)):
            try:
                check[i] = int(check[i])
            except ValueError:
                check[i] = -1

        self.gp1 = check[0]
        self.gp2 = check[1]
        self.gp3 = check[2]
        self.points = check[3]
        self.placement = check[4]

    def spread(self):

        return [self.team, self.name, self.gp1, self.gp2, self.gp3,
                self.points, self.placement]

    def sub_parse(self):

        if '/' in self.name:
            name1, name2 = self.name.split('/')




class PlayerAll(Player):

    def __init__(self, name, team, gp1, gp2, gp3, points, placement, num, id, sum=True):
        Player.__init__(self=self, name=name, team=[team], gp1=[gp1],
                        gp2=[gp2], gp3=[gp3], points=[points],
                        placement=[placement], num=[num], sum=sum)

        self.id = id
    def update(self, player):
        if player.team not in self.team:
            self.team.append(player.team)

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


class Team():

    def __init__(self, name, gp1, gp2, gp3, pen, score, players=[], num=0):
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
            string += player.name + ", "

        string = string[:-2]

        return self.name + " Players: " + string


class TeamAll(Team):

    def __init__(self, name, gp1, gp2, gp3, pen, score, players, num, id, roster=[]):

        Team.__init__(self, name=name, gp1=[gp1], gp2=[gp2],
                      gp3=[gp3], pen=[pen], score=[score],
                      players=[players], num=[num])
        self.id = id

    def update(self, team):

        self.num.append(team.num)
        self.gp1.append(team.gp1)
        self.gp2.append(team.gp2)
        self.gp3.append(team.gp3)
        self.score.append(team.score)
        self.players.append(team.players)


    def roster_calc(self):

        roster = defaultdict(lambda: 0)

        for group in self.players:
            for player in group:
                roster[player.name] += 1

        df = pd.Series(dict(roster)).sort_values(ascending=False)


class Race():

    def __init__(self, number, course, first, second, third, fourth, fifth,
                 sixth, seventh, eighth, ninth, tenth):
        self.number = number
        self.course = course
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.fifth = fifth
        self.sixth = sixth
        self.seventh = seventh
        self.eighth = eighth
        self.ninth = ninth
        self.tenth = tenth


class Match():

    def __init__(self, name, date, num, t1, t2, t1p, t2p, dif, id, df=[]):

        self.name = name
        self.date = date
        self.num = num
        self.t1 = t1
        self.t2 = t2
        self.t1p = t1p
        self.t2p = t2p
        self.dif = dif
        self.id = id
        self.df = self.match_df()

    def __repr__(self):

        print(self.name)
        print(self.match_df())

        return 'Date Played: ' + self.date

    def match_df(self):

        columns = ['Team', 'Player', 'GP1', 'GP2', 'GP3', 'Total', 'Placement']
        full = []
        for player in self.t1.players:
            full.append(player.spread())
        for player in self.t2.players:
            full.append(player.spread())

        df = pd.DataFrame(full, columns=columns)

        return df
