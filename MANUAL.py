import csv
import json
import pandas as pd
from MKOBJECT import *

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
          "SNES Ghost Valley 2": 'GV2',
          "N64 Mario Raceway": 'rMR',
          "N64 Sherbet Land": 'rSL',
          "GBA Shy Guy Beach": 'SGB',
          "DS Delfino Square": 'DSDS',
          "GCN Waluigi Stadium": 'rWS',
          "DS Desert Hills": 'rDH',
          "GBA Bowser Castle 3": 'BC3',
          "N64 DK's Jungle Parkway": 'DKJP',
          "GCN Mario Circuit": 'rMC',
          "SNES Mario Circuit 3": 'MC3',
          "DS Peach Gardens": 'rPG',
          "GCN DK Mountain": 'DKM',
          "N64 Bowser's Castle": 'rBC'}


def read(string, num=0):

    matches = []

    num += 1

    dct = json.loads(string)

    tracks = dct['tracks']

    for i in range(len(tracks)):
        tracks[i] = TRACKS[tracks[i]]

    teams = dct['teams']
    both = []

    print(len(teams))

    for key in teams:

        df = pd.DataFrame.from_dict(teams[key])
        players = []
        key_num = -1

        for fc, entry in df['players'].items():
            key_num += 1
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

            if entry['subbed_out']:
                player.sub_out = True

            players.append(player)

        gp1 = 0
        gp2 = 0
        gp3 = 0

        for p in players:
            gp1 += int(p.gp1)
            gp2 += int(p.gp2)
            gp3 += int(p.gp3)

        team = Team(key, gp1, gp2, gp3,
                    teams[key]['table_penalty_str'],
                    int(teams[key]['total_score']),
                    players, num)

        both.append(team)
        print(both)

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


def reconstruct(file):

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
                      None: 0}

    with open(file, 'r') as infile:

        data = csv.reader(infile)

        row_num = 0

        names = []
        fcs = []
        mii = []
        tag = []
        total = []
        subbed_out = []
        places = []

        for row in data:

            row_num += 1

            if row_num == 1:
                title_str = row[0]
            elif row_num == 2:
                teams = [row[0]]
                t1_pen = row[1]
                t1_points = row[2]
            elif row_num == 3:
                teams.append(row[0])
                t2_pen = row[1]
                t2_points = row[2]
            elif row_num == 5:
                tracks = row[6:]
            elif 5 < row_num < 16:
                names.append(row[0])
                fcs.append(row[1])
                mii.append(row[2])
                tag.append(row[3])
                total.append(row[4])
                subbed_out.append(row[5])
                places.append(row[6:])

        string = '{"title_str":"' + title_str
        string += '","format":"5v5","races_played":12,'
        string += f'"tracks":['

        for track in tracks:
            string += f'"{track}",'

        string = string[:-1]
        string += ']'

        string += ',"teams":'
        string += '{"' + teams[0] + '":{"table_penalty_str":"' + t1_pen + '","total_score":' + t1_points + ','
        string += '"players":{'

        for i in range(len(names[:5])):
            sub_string = '"' + fcs[i] + '":{"mii_name":"' + mii[i] + '","lounge_name":"' + names[i] \
                        + '","tag":"' + tag[i] + '","total_score":"' + total[i] + '","subbed_out":"' \
                        + subbed_out[i] + '"'

            scores = []
            for num in places[i]:
                scores.append(place_to_point[int(num)])

            sub_string += f',"race_scores":{scores},"race_positions":{[int(x) for x in places[i]]},'
            sub_string += f'"gp_scores":{[scores[0:4], scores[4:8], scores[8:]]},"flag":"HELP"'
            sub_string += '},'
            string += sub_string

        string = string[:-1]
        string += '}},"' + teams[1] + '":{"table_penalty_str":"' + t2_pen + '","total_score":' + t2_points + ','
        string += '"players":{'

        for i in range(len(names[5:])):

            i += 5

            sub_string = '"' + fcs[i] + '":{"mii_name":"' + mii[i] + '","lounge_name":"' + names[i] \
                         + '","tag":"' + tag[i] + '","total_score":"' + total[i] + '","subbed_out":"' \
                         + subbed_out[i] + '"'

            scores = []
            for num in places[i]:
                scores.append(place_to_point[int(num)])

            sub_string += f',"race_scores":{scores},"race_positions":{[int(x) for x in places[i]]},'
            sub_string += f'"gp_scores":{[scores[0:4], scores[4:8], scores[8:]]},"flag":"HELP"'
            sub_string += '},'
            string += sub_string

        string = string[:-1]
        string += '}}}}'

        print(string)

        return string


def main():

    string = reconstruct('D1_2B.csv')
    j = json.loads(string)

    funny = j['teams'][list(j['teams'].keys())[0]]['players']
    funk = list(funny.keys())

    for key in funk:

        num = j['teams'][list(j['teams'].keys())[0]]['players'][key]['total_score']
        j['teams'][list(j['teams'].keys())[0]]['players'][key]['total_score'] = int(num)

        scores = j['teams'][list(j['teams'].keys())[0]]['players'][key]['race_scores']

        scores = [int(x) for x in scores]

        j['teams'][list(j['teams'].keys())[0]]['players'][key]['races_scores'] = scores

    print('final')
    print(j)


main()
