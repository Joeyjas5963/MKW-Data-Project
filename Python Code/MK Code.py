from MKOBJECT import Player, Team, Match
from MKOBJECT import PlayerAll, TeamAll
import csv

def collect_table_list(file1):
    with open(file1, 'r') as infile:
        csv_file = csv.reader(infile, delimiter=',')

        data = []
        for row in csv_file:
            data.append(row)

        matches = []
        count = -1
        for i in range(len(data)):
            if 'DONE' in data[i]:
                match = data[i+1:i+17]

                team1_players = []
                team2_players = []

                for j in range(len(match)):
                    match[j] = match[j][0:6]

                    if 1 < j < 8 or 9 < j:

                        name = match[j][0]
                        gp1 = match[j][1]
                        gp2 = match[j][2]
                        gp3 = match[j][3]
                        if j == 7 or j == 10:
                            pen = match[j][4]
                            points = match[j][5]
                            if j == 7:
                                team1 = Team(name, gp1, gp2, gp3, pen, points)

                            else:
                                team2 = Team(name, gp1, gp2, gp3, pen, points)


                        else:
                            points = match[j][4]
                            placement = match[j][5]
                            p = Player(name, gp1, gp2, gp3, points, placement)

                        if 1 < j < 7:
                            team1_players.append(p)
                        elif j > 10:
                            team2_players.append(p)

                count += 1

                for p in team1_players:
                    p.team = team1.name
                    p.num = count
                for p in team2_players:
                    p.team = team2.name
                    p.num = count

                team1.num = count
                team2.num = count


                team1.players = team1_players
                team2.players = team2_players


                name = file1[:-4].replace('_', ' ') + " Match #" + \
                       str(count) + ': ' + match[1][0]

                match = Match(name, match[0][0], count, team1, team2, team1.score,
                        team2.score, match[2][5], count)

                matches.append(match)

    return matches

def summarize(matches):

    player_alls = []
    player_names = []
    p_ids = {}
    p_id = -1

    team_alls = []
    team_names = []
    t_ids = {}
    t_id = -1

    for match in matches:

        both = match.t1.players + match.t2.players

        for player in both:
            if player.name not in player_names:
                p_id += 1
                p = PlayerAll(player.name, player.team,
                              player.gp1, player.gp2,
                              player.gp3, player.points,
                              player.placement, player.num,
                              p_id)

                p_ids[p.name] = p_id
                player_alls.append(p)
                player_names.append(player.name)
            else:
                idx = player_names.index(player.name)
                player_alls[idx].update(player)

        both = [match.t1, match.t2]

        for team in both:
            if team.name not in team_names:
                t_id += 1
                t = TeamAll(team.name, team.gp1, team.gp2,
                            team.gp3, team.pen, team.score,
                            team.players, team.num, t_id)

                t_ids[t.name] = t_id
                team_alls.append(t)
                team_names.append(team.name)
            else:
                idx = team_names.index(team.name)
                team_alls[idx].update(team)

            for team_all in team_alls:
                team_all.roster_calc()

    p_ids.pop('')
    t_ids.pop('')

    return player_alls, team_alls, p_ids, t_ids

def main():
    file1 = 'GSC_S1_D1.csv'
    matches = collect_table_list(file1)
    player_alls, team_alls, p_ids, t_ids = summarize(matches)
    print(matches[0])
    print(p_ids)
    #print(player_alls[42])


    p1, p2 = player_alls[72]

main()

