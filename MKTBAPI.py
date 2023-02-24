import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from MKOBJECT import Player, Team, Match
from MKOBJECT import PlayerAll, TeamAll
from MKOBJECT import PlayerAPI, MatchAPI, PlayerAPIALL
import csv
import plotly.express as px
import plotly.graph_objs as go
import json

TRACKS = {"Wii Luigi Circuit": 'LC',
          "Wii Moo Moo Meadows": 'MMM',
          "Wii Mushroom Gorge": 'MG',
          "Wii Toad's Factory": 'TF',
          "Wii Mario Circuit": 'MC',
          "Wii Coconut Mall": 'CM',
          "Wii DK Summit": 'DKS',
          "Wii Wario's Gold Mine": 'WGM',
          "Wii Daisy Circuit": 'DC',
          "Wii Koopa Cape": 'KC',
          "Wii Maple Treeway": 'MT',
          "Wii Grumble Volcano": 'GV',
          "Wii Dry Dry Ruins": 'DDR',
          "Wii Moonview Highway": 'MH',
          "Wii Bowser's Castle": "BCWii",
          "Wii Rainbow Road": 'RR',
          "GCN Peach Beach": 'rPB',
          "DS Yoshi Falls": 'rYF',
          "SNES Ghost Valley 2": 'rGV2',
          "N64 Mario Raceway": 'rMR',
          "N64 Sherbet Land": 'rSL',
          "GBA Shy Guy Beach": 'rSGB',
          "DS Delfino Square": 'rDS',
          "GCN Waluigi Stadium": 'rWS',
          "DS Desert Hills": 'rDH',
          "GBA Bowser Castle 3": 'rBC3',
          "N64 DK's Jungle Parkway": 'rDKJP',
          "GCN Mario Circuit": 'rMC',
          "SNES Mario Circuit 3": 'MC3',
          "DS Peach Gardens": 'rPG',
          "GCN DK Mountain": 'rDKM',
          "N64 Bowser's Castle": 'rBC'}


def load_pdb(file):

    with open (file, 'r', encoding='utf-8') as infile:

        df = pd.read_csv(infile)

        df_fcs = df.iloc[:, 4:]

        fcs_list = []

        for i in range(len(df_fcs)):
            fcs = ''
            for j in range(len(list(df_fcs.columns))):
                if str(df_fcs.iloc[i, j]) != 'nan':
                    fcs += (str(df_fcs.iloc[i, j]))
                    fcs += '|'

            fcs_list.append(fcs)

        df.loc[:, 'FCs'] = fcs_list
        df = df.iloc[:, :5]

        return df


def load_tdb(file):

    with open(file, 'r') as infile:

        df = pd.read_csv(infile, encoding='utf-8')
        df = df.iloc[:, :-1]

        df.iloc[0, 3] = '£★'
        df.iloc[8, 3] = 'Λν'
        df.iloc[12, 3] = 'Purξ'
        df.iloc[14, 3] = 'ßÿ'
        df.iloc[17, 3] = '«♪»'
        df.iloc[20, 3] = 'Berserk'
        df.iloc[21, 3] = 'Cγ1'
        df.iloc[22, 3] = 'Σz'
        df.iloc[27, 3] = 'Mι'
        df.iloc[28, 3] = 'beγønd'
        df.iloc[29, 3] = 'βτ'
        df.iloc[30, 3] = 'Lε'
        df.iloc[33, 3] = 'Ω'
        df.iloc[36, 3] = 'λυ'
        df.iloc[45, 3] = 'Cγ2'
        df.iloc[53, 3] = 'PΨ'

        return df


def db_crucial(p_data, t_data):

    df_player = load_pdb(p_data)
    df_team = load_tdb(t_data)

    return df_player, df_team


def read(file, num=0, manual=False):

    if manual:
        print('MANUAL')

    matches = []

    with open(file, 'r', encoding='utf-8') as infile:

        while True:

            string = infile.readline()

            if string == '':
                break

            else:

                num += 1

                dct = json.loads(string)

                print(dct)

                tracks = dct['tracks']

                for i in range(len(tracks)):
                    tracks[i] = TRACKS[tracks[i]]

                teams = dct['teams']

                both = []

                for key in teams:

                    df = pd.DataFrame.from_dict(teams[key])
                    players = []
                    key_num = -1

                    for fc, entry in df['players'].items():
                        key_num += 1

                        if manual:
                            k = -1
                            for i in range(len(entry['gp_scores'])):
                                for j in range(len(entry['gp_scores'][i])):
                                    k += 1
                                    entry['gp_scores'][i][j] = int(entry['gp_scores'][i][j])
                                    entry['race_scores'][k] = int(entry['race_scores'][k])

                            entry['total_score'] = int(entry['total_score'])

                        player = PlayerAPI(entry['lounge_name'],
                                           sum(entry['gp_scores'][0]),
                                           sum(entry['gp_scores'][1]),
                                           sum(entry['gp_scores'][2]),
                                           entry['total_score'],
                                           fc,
                                           entry['mii_name'],
                                           entry['race_scores'],
                                           entry['race_positions'],
                                           entry['flag'],
                                           team=key, num=num, sum=True)

                        if entry['subbed_out'] and type(entry['subbed_out']) != str:
                            player.sub_out = True
                        elif entry['subbed_out'] == 'TRUE':
                            player.sub_out = True

                        players.append(player)

                    gp1 = 0
                    gp2 = 0
                    gp3 = 0

                    for p in players:
                        gp1 += int(p.gp1)
                        gp2 += int(p.gp2)
                        gp3 += int(p.gp3)

                    if key == '[L]':
                        if 'D1' in dct['title_str']:
                            name = '[L]1'
                        else:
                            name = '[L]2'

                    elif key == 'HK':
                        if 'D4' in dct['title_str']:
                            name = 'HK1'
                        else:
                            name = 'HK2'

                    elif key == '@NN':
                        if 'D4' in dct['title_str']:
                            name = '@NN1'
                        else:
                            name = '@NN2'

                    elif key == 'Cγ':
                        if 'D4' in dct['title_str']:
                            name = 'Cγ1'
                        else:
                            name = 'Cγ2'

                    elif key == 'Mt':
                        name = 'Mt.'
                    else:
                        name = key

                    team = Team(name, gp1, gp2, gp3,
                                teams[key]['table_penalty_str'],
                                int(teams[key]['total_score']),
                                players, num)

                    both.append(team)

                t1t = 'later'
                t2t = 'bruh'

                match = MatchAPI('Index ' + str(num) + ' ' + dct['title_str'],
                                 both[0],
                                 both[1],
                                 t1t,
                                 t2t,
                                 both[0].score,
                                 both[1].score,
                                 both[0].players + both[1].players,
                                 both[0].score - both[1].score,
                                 num,
                                 tracks)

                matches.append(match)

        return matches, num


def summarize(matches, df_player, df_team):

    player_alls = []
    player_names = []
    p_ids = {}
    dict_id = -1

    team_alls = []
    team_names = []
    t_ids = {}
    t_id = -1

    # loops through each match in match list
    for match in matches:
        '''
        if type(match) == list:
            match = match[0]
            print(match)
        '''
        # creates joint list for all players in match
        both = match.t1.players + match.t2.players

        # loops through each player in combined list
        for player in both:

            for i in range(len(df_player.loc[:, 'FCs'])):
                mod_code = df_player.iloc[i, -1].strip('|')
                if '|' in mod_code:
                    mod_code = mod_code.split('|')
                if player.fc in mod_code:
                    player.name = df_player.iloc[i, 2]

                    if player.name not in player_names:

                        # create player_all object for this player
                        p = PlayerAPIALL(player.name, df_player.iloc[i, 3], player.team,
                                         player.gp1, player.gp2, player.gp3, player.points,
                                         player.fc, player.mii, player.race_scores, player.race_positions,
                                         player.flag, dict_id, df_player.iloc[i, 0], player.placement, player.num)

                        dict_id += 1
                        p_ids[p.tag_name] = dict_id
                        player_alls.append(p)
                        player_names.append(player.name)

                    else:

                        # if player already exists in player_alls
                        # find player all object and update it with new match data
                        idx = player_names.index(player.name)
                        player_alls[idx].update(player)

        # redefines both for new loop, looking at team data now
        both = [match.t1, match.t2]

        # loops for each team
        for team in both:

            # check is team is not already in list
            if team.name not in team_names:

                # creates team_all object
                t_id += 1
                t = TeamAll(team.name, team.gp1, team.gp2,
                            team.gp3, team.pen, team.score,
                            team.players, team.num, t_id)

                tags = list(df_team.iloc[:, 3])
                base_row = tags.index(team.name)
                t.base_id = df_team.iloc[base_row, 0]

                # adds id to dict, adds team_all to list
                # saves name for future updates
                t_ids[t.name] = t_id
                team_alls.append(t)
                team_names.append(team.name)
            else:

                # updates team object if already in list
                idx = team_names.index(team.name)
                team_alls[idx].update(team)

            for team_all in team_alls:
                team_all.roster_calc()

    # gets rid of blank ids in id list (it happens idk)
    # p_ids.pop('')
    # t_ids.pop('')

    return player_alls, team_alls, p_ids, t_ids


def api_crucial():

    df_player, df_team = db_crucial('P_Data.csv', 'T_Data.csv')

    matches = []
    m_num = -1
    for num in range(1, 9):
        m, m_num = read('GSCD' + str(num) + '.txt', m_num)
        matches += m

    addon = read('blank.txt', m_num, manual=True)
    addon = addon[0]
    matches += addon

    player_alls, team_alls, p_ids, t_ids = summarize(matches, df_player, df_team)

    return matches, player_alls, team_alls, p_ids, t_ids, df_player, df_team


def debug():

    matches, player_alls, team_alls, p_ids, t_ids, df_player, df_team = api_crucial()

    for player in matches[69].players:
        print(player.tag_name)
        print(player.race_scores)

debug()