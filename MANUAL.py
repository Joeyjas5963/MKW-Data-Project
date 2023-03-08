import csv
import json
import pandas as pd


def reconstruct(file):

    place_to_point = {'1': 15,
                      '2': 12,
                      '3': 10,
                      '4': 8,
                      '5': 6,
                      '6': 4,
                      '7': 3,
                      '8': 2,
                      '9': 1,
                      '10': 0,
                      '-1': -1}

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

        print(names)

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

        print(teams[0])
        for i in range(len(names[:5])):

            print(names[i])
            sub_string = '"' + fcs[i] + '":{"mii_name":"' + mii[i] + '","lounge_name":"' + names[i] \
                        + '","tag":"' + tag[i] + '","total_score":"' + total[i] + '","subbed_out":"' \
                        + subbed_out[i] + '"'

            scores = []
            for num in places[i]:
                if num != '':
                    scores.append(place_to_point[num])
                else:
                    scores.append(-1)

            sub_string += f',"race_scores":{scores},"race_positions":{[int(x) for x in places[i]]},'
            sub_string += f'"gp_scores":{[scores[0:4], scores[4:8], scores[8:]]},"flag":"HELP"'
            sub_string += '},'
            string += sub_string

        string = string[:-1]
        string += '}},"' + teams[1] + '":{"table_penalty_str":"' + t2_pen + '","total_score":' + t2_points + ','
        string += '"players":{'

        print(teams[1])
        for i in range(len(names[5:])):

            i += 5

            print(names[i])

            sub_string = '"' + fcs[i] + '":{"mii_name":"' + mii[i] + '","lounge_name":"' + names[i] \
                         + '","tag":"' + tag[i] + '","total_score":"' + total[i] + '","subbed_out":"' \
                         + subbed_out[i] + '"'

            scores = []
            for num in places[i]:
                scores.append(place_to_point[num])

            sub_string += f',"race_scores":{scores},"race_positions":{[int(x) for x in places[i]]},'
            sub_string += f'"gp_scores":{[scores[0:4], scores[4:8], scores[8:]]},"flag":"HELP"'
            sub_string += '},'
            string += sub_string

        string = string[:-1]
        string += '}}}}'

        print(string)

        return string


j = reconstruct(os.path.join(os.get.cwd(), 'data', 'matches', 'D5', 'D5_2D.csv'))
