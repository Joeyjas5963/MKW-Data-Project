import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from MKOBJECT import Player, Team, Match
from MKOBJECT import PlayerAll, TeamAll
import csv
import plotly.express as px
import plotly.graph_objs as go
import random
import os

# DATA COLLECTION AND OBJECT CREATION

COLORS = [{'Netherlands': '#FFA500', 'Daisy Squad': '#FF0000',
           'Lazarus': '#6495ED', 'Infinite Fusion': '#39FF14',
           'perma jc': '#FF10F0', 'Superbia': '#8B8000'},
          {'Apocalypse': '#228B22', 'Berserk': '#FF0000',
           'Curse': '#D2B48C', 'Explorers of Time': '#00FFFF',
           'Lethal Vengeance': '#FFA500', 'Lightspeed Kitty Cats': '#39FF14',
           'Long Shaft University': '#A020F0', 'Megavolt': '#6495ED'},
          {'Pure': '#FF10F0', 'Butterfly Effect': '#FFA500',
           'Team Gun': '#D2B48C', 'Avail': '#808080',
           'Mount Olympus': '#FF0000', 'Unxseen': '#6495ED',
           'MY13': '#00FFFF', 'Melody': '#39FF14'},
          {'Brutality': '#D2B48C', 'Ici Ca Bz': '#39FF14',
           'George Arvo Mark Toad': '#FF0000', 'The Nice Guys': '#FFA500',
           'Shadow Team': '#E0B0FF', 'Contingency White': '#93CCEA',
           'Geek for Life': '#00FFFF', 'Quintessence': '#FF10F0'},
          {'Berserk II': '#8B0000', 'Band Together': '#228b22',
           'Faithless': '#8B8000', 'Contingency Black': '#E0B0FF',
           'Rise': '#FFA500', 'Ez': '#39FF14', 'Versatile': '#00FFFF',
           'Tunes Horizon': '#FF0000'},
          {"Brophy's Theory": '#FF0000', 'beyond the universe': '#228b22',
           'Contingency Orange': '#FFA500', "Hell's Kitchen": '#800000',
           'Luminescence': '#39FF14', 'Auspicion': '#6495ED',
           'The Twelve': '#93CCEA', "Euler's Identity": '#FFD700'},
          {'Gardie Lumb Wacker': '#39FF14', 'Helicity': '#00FFFF',
           'Jugar o Perder': '#FFA500', 'L Fourteen': '#FF10F0',
           'Northwest': '#6495ED', 'Southwest': '#FF0000'}]



def collect_table_list(file1):
    ''' function which reads list of tables in GSC Master

    Arguments:
        file1 (str): name of csv

    Returns:
        matches (list): list of match objects
    '''

    # opens and reads data from csv
    with open(file1, 'r') as infile:
        print(file1)
        csv_file = csv.reader(infile, delimiter=',')

        data = []
        for row in csv_file:
            data.append(row)

        matches = []
        count = 0

        # data collection loop
        for i in range(len(data)):

            # check if table has DONE verification
            if 'DONE' in data[i]:

                # sets individual table to variable
                match = data[i+1:i+17]

                team1_players = []
                team2_players = []

                # table reading loop
                for j in range(len(match)):

                    # chops excess columns off of match
                    match[j] = match[j][0:6]

                    # checks if currently reading a row with scores
                    if 1 < j < 8 or 9 < j:

                        # getting player data
                        name = match[j][0]
                        gp1 = match[j][1]
                        gp2 = match[j][2]
                        gp3 = match[j][3]

                        # checks if currently reading team row
                        if j == 7 or j == 10:

                            pen = match[j][4]
                            points = match[j][5]

                            if pen == '':
                                pen = 0

                            # create team object if it's a team row
                            if j == 7:
                                team1 = Team(name, gp1, gp2, gp3, pen, points)
                                #print(team1, name, gp1, gp2, gp3, pen, points)
                                

                            else:
                                team2 = Team(name, gp1, gp2, gp3, pen, points)
                                #print(team2, name, gp1, gp2, gp3, pen, points)


                        else:

                            # gets points and placement for player
                            points = match[j][4]
                            placement = match[j][5]

                            # creates player object from player
                            p = Player(name, gp1, gp2, gp3, points, placement)
                            #print(p, name, gp1, gp2, gp3, points, placement)

                        # adds player objects to team rosters
                        if 1 < j < 7:
                            team1_players.append(p)
                        elif j > 10:
                            team2_players.append(p)
                        #print(team1_players)
                        #print(team2_players)

                count += 1

                # gives player objects team association
                # adds match this player played in as p.num
                for p in team1_players:
                    p.team = team1.name
                    p.num = count
                for p in team2_players:
                    p.team = team2.name
                    p.num = count

                # adds match these teams played in as team.num
                team1.num = count
                team2.num = count


                # adds player rosters to team objects
                team1.players = team1_players
                team2.players = team2_players
                both = team1.players + team2.players


                # creates name for match
                name = file1[:-4].replace('_', ' ') + " Match #" + \
                       str(count) + ': ' + match[1][0]

                date = match[0][0]
                dif = match[2][5]

                # creates match with all of the above information
                match = Match(name, date, count, team1, team2, int(match[8][-1]),
                              int(match[9][-1]), team1.score, team2.score, both,
                              dif, count)

                # adds match to list of matches
                matches.append(match)

    return matches


def summarize(matches):
    ''' composes all objects into ALL versions (total season data)

    Arguments:
        matches (list): list of match objects created by above function

    Returns:
        player_alls (list): list of player_all objects, overall season data
        team_alls (list): list of team_all objects, overall season data
        p_ids (dict): dictionary with ids for each player,
                      corresponding to index in player_alls list
        t_ids (dict): dictionary with ids for each team,
                      corresponding to index in team_alls list
    '''

    # initializing variables
    player_alls = []
    player_names = []
    p_ids = {}
    p_id = -1

    team_alls = []
    team_names = []
    t_ids = {}
    t_id = -1

    # loops through each match in match list
    for match in matches:

        # creates joint list for all players in match
        both = match.t1.players + match.t2.players

        # loops through each player in combined list
        for player in both:

            # checks if it's the first instance of this player
            if player.name not in player_names:

                # create player_all object for this player
                p_id += 1
                p = PlayerAll(player.name, player.team,
                              player.gp1, player.gp2,
                              player.gp3, player.points,
                              player.placement, player.num,
                              p_id)

                # add id to dictionary, and player to total list
                # saves player name for future updates
                p_ids[p.name] = p_id
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
    #p_ids.pop('')
    #t_ids.pop('')

    return player_alls, team_alls, p_ids, t_ids

# ANALYTIC FUNCTIONS


def average(player_alls_D):
    ''' Finds the average score for each player (idk what to do with subs)

    Arguments:
        player_alls_D (list): list of player_alls

    '''

    avg_dict = {}

    # iterates through each player_alls lists
    for player_alls in player_alls_D[1:]:
        # iterates through each player
        for player in player_alls:

            # find the average score of each player and print
            print(player.name)
            if '/' not in player.name:
                avg = sum(player.points) / len(player.points) / 3
                player.avg = float(format(avg, '.1f'))
                print(player.avg)
                if player.avg < 50:
                    avg_dict[player.name] = player.avg

    ds = pd.Series(avg_dict)

    print(ds.sort_values(ascending=False).to_string())


def perfect(matches_D):
    ''' Searches all matches for "perfect" wars

    Arguments:
        matches_D: list of each divs matches
    '''

    # set perfect standing list, and list to store perfects
    perfect_list = [1, 2, 3, 4, 9]
    perfect_matches = []

    # iterate through each div
    for matches in matches_D[1:]:
        # iterate through each match
        for match in matches:

            # grab just the placements column of bottom team
            df = match.df
            place = list(df.iloc[5:, -1])
            count = 0

            # iterate through each place
            for num in place:
                # if match is not perfect, or empty, break
                if num in perfect_list or -1 in place:
                    break
                else:
                    count += 1
                    # if each player looked at, and winners got 10 points, store
                    if count == 5 and match.t1t == 10:
                        perfect_matches.append(match)
                        match.perfect = True

    # print names of all winning matches
    for i in range(len(perfect_matches)):
        print(perfect_matches[i].name)

    return perfect_matches


def top_scores(matches_D):
    ''' Creates dataframe of top scores for season

    Arguments:
        matches_D: list of each divs matches
    '''

    # create list to store player objects, and framework for df
    top = []
    df_dict = {'Score': [], 'Player': [],
               'Team': [], 'Div': [], 'Match Num': []}

    # iterate through each div
    for matches in matches_D[1:]:
        # iterate through each match
        for match in matches:
            # iterate through each player in match
            for player in match.players:
                # if they scored more than 130, add to df
                if player.points >= 130:

                    # adding to top player list, and df
                    top.append(player)
                    df_dict['Score'].append(player.points)
                    df_dict['Player'].append(player.name)
                    df_dict['Team'].append(player.team)
                    df_dict['Div'].append(matches_D.index(matches))
                    df_dict['Match Num'].append(player.num)

    # creating and printing df
    df_top = pd.DataFrame(df_dict).sort_values('Score', ascending=False)
    print(df_top.to_string())


def score_dist(matches_D, all):
    ''' creates distribution of runner scores

    Arguments:
        matches_D: list of each divs matches
    '''

    sns.set()

    # crate bins for histogram
    bins = [13] + list(range(20, 180, 5))

    if all == True:
        # list to store scores
        scores = []

        # iterate through each div
        for matches in matches_D[1:]:
            # iterate through each match
            for match in matches:
                # iterate through each player
                for player in match.players:
                    # if player is not a bagger, add to list
                    if player.points > 12:
                        scores.append(player.points)

        # plot and show histogram
        plt.hist(scores, bins=bins)
        plt.title('Runner Score Distribution Across GSC')
        plt.xlabel('Scores')
        plt.ylabel('Frequency')
        plt.show()

    else:

        for matches in matches_D[1:]:
            scores = []
            div = matches_D.index(matches)
            for match in matches:
                # iterate through each player
                for player in match.players:
                    # if player is not a bagger, add to list
                    if player.points > 12:
                        scores.append(player.points)

            plt.hist(scores, bins=bins)
            title = 'Runner Score Distribution Across D' + str(div)
            plt.title(title)
            plt.xlabel('Scores')
            plt.ylabel('Frequency')
            plt.show()


def wins_five(matches_d, t_ids_d):

    teams = {}

    div = 0
    t_ids_d = t_ids_d[1:]
    for t_ids in t_ids_d:
        div += 1
        for team in t_ids.keys():
            r = {'w': 0, 'l': 0, 'rate': 0}
            record = [0]
            print(team)
            for match in matches_d[div]:
                if match.t1.name == team:
                    r['w'] += 1
                if match.t2.name == team:
                    r['l'] += 1

                if match.t1.name == team or match.t2.name == team:
                    r['rate'] = r['w'] - (r['l'])
                    print(r)
                    record.append(r['rate'])

            teams[team] = record

    div = 0
    for t_ids in t_ids_d:

        df = pd.DataFrame()
        fig = go.Figure()
        div += 1

        for team in t_ids.keys():

            color = COLORS[div-1][team]

            df.loc[:, team] = teams[team]
            fig.add_trace(go.Scatter(x=df.index.values,
                                     y=(df[team] + .08 * (len(t_ids.keys()) / 2 - list(t_ids.keys()).index(team) - 1)),
                                     name=team, line=dict(width=3, color=color)))

        fig.add_hline(y=0)
        fig.update_traces(hoverinfo='name+y')
        fig.update_layout(hovermode='x unified', xaxis=dict(
                            tickmode='linear',
                            tick0=0,
                            dtick=1),
                          yaxis=dict(tickmode='linear', tick0=-10, dtick=1))
        fig.update_xaxes(title_text='Match')
        fig.update_yaxes(title_text='Wins - Losses')
        fig.update_layout(title={'text': f'Wins Above .500 (D{div})'}, legend_title_text='Teams')

        fig.show()

    print(teams)


def tunes(matches_d, t_ids_d):

    teams = {}

    div = 0
    t_ids_d = t_ids_d[1:]
    for t_ids in t_ids_d:
        div += 1
        for team in t_ids.keys():
            t = 0
            points = [0]
            for match in matches_d[div]:
                if match.t1.name == team:
                    t += match.t1t
                elif match.t2.name == team:
                    t += match.t2t

                if match.t1.name == team or match.t2.name == team:
                    points.append(t)

            teams[team] = points

    div = 0
    for t_ids in t_ids_d:

        df = pd.DataFrame()
        fig = go.Figure()
        div += 1

        for team in t_ids.keys():
            color = COLORS[div - 1][team]

            df.loc[:, team] = teams[team]
            fig.add_trace(go.Scatter(x=df.index.values,
                                     y=df[team],
                                     name=team, line=dict(width=3, color=color)))

        fig.add_hline(y=0)
        fig.update_traces(hoverinfo='name+y')
        fig.update_layout(hovermode='x unified', xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=1),
                          yaxis=dict(tickmode='linear', tick0=0, dtick=10))
        fig.update_xaxes(title_text='Match')
        fig.update_yaxes(title_text='Wins - Losses')
        fig.update_layout(title={'text': f'Tunes Points for (D{div})'}, legend_title_text='Teams')

        fig.show()


def neccsary():

    divs = list(range(1, 8))
    matches_D = [0]
    player_alls_D = [0]
    team_alls_D = [0]
    p_ids_D = [0]
    t_ids_D = [0]

    for div in divs:
        #print(str(div))
        #TODO: Make a global variable for the season so that its not hardcoded
        print(os.getcwd())
        file = os.path.join(os.getcwd(), 'data', 'S4', 'divs', 'GSC_S4_D' + str(div) + '.csv')
        #file = os.getcwd() + 'data\\' + 'S4\\' + 
        print(file)
        matches = collect_table_list(file)
        player_alls, team_alls, p_ids, t_ids = summarize(matches)
        matches_D.append(matches)
        player_alls_D.append(player_alls)
        team_alls_D.append(team_alls)
        p_ids_D.append(p_ids)
        t_ids_D.append(t_ids)
        print(f'Collected D{div}')

    return matches_D, player_alls_D, team_alls_D, p_ids_D, t_ids_D



def cmpTunesToRealScore(divs):

    tunes = []
    real_score = []
    for div in divs:
        if div == 0:
            tunes.append([0])
            real_score.append([0])
            continue
        else:
            tempTunes = []
            tempScore = []
            tempT1TunesScore = 0
            tempT2TunesScore = 0
            for match in div:
                if 'free win' in match.name:
                    #print('Free win detected. Will continue')
                    continue
                
                if match.t1.gp1 > match.t2.gp1:
                    tempT1TunesScore += 2
                elif match.t1.gp1 < match.t2.gp1:
                    tempT2TunesScore += 2
                else:
                    tempT1TunesScore += 1
                    tempT2TunesScore += 1

                if match.t1.gp2 > match.t2.gp2:
                    tempT1TunesScore += 2
                elif match.t1.gp2 < match.t2.gp2:
                    tempT2TunesScore += 2
                else:
                    tempT1TunesScore += 1
                    tempT2TunesScore += 1

                if match.t1.gp3 > match.t2.gp3:
                    tempT1TunesScore += 2
                elif match.t1.gp3 < match.t2.gp3:
                    tempT2TunesScore += 2
                else:
                    tempT1TunesScore += 1
                    tempT2TunesScore += 1

                if match.t1.score > match.t2.score:
                    tempT1TunesScore += 4
                elif match.t1.score < match.t2.score:
                    tempT2TunesScore += 4
                else:
                    tempT1TunesScore += 2
                    tempT2TunesScore += 2
                
                if int(match.t1.score) > int(match.t2.score):
                    tempScore.append(int(match.t1.score) - int(match.t2.score))
                    tempTunes.append(tempT1TunesScore)
                elif int(match.t1.score) < int(match.t2.score):
                    tempScore.append(int(match.t2.score) - int(match.t1.score))
                    tempTunes.append(tempT2TunesScore)
                
                #tempTunes.append(tempT1TunesScore)
                #tempTunes.append(tempT2TunesScore)
                #tempScore.append(int(match.t1.score) - int(match.t2.score))
                #tempScore.append(int(match.t2.score) - int(match.t1.score))
                tempT1TunesScore = 0
                tempT2TunesScore = 0
            
            tunes.append(tempTunes)
            real_score.append(tempScore)
            tempTunes = []
            tempScore = []
    if len(tunes) != len(real_score):
        print('Something is wrong because the scores are not equal') 
    currDiv = 0
    numDivs = 8

    for div in range(0, numDivs):
        if div == 0:
            #print('Continue')
            continue
        print('D' + str(div))
        divTunes = tunes[div]
        divScore = real_score[div]
        if len(divTunes) != len(divScore):
            print('Something went wrong. len(divTunes) != len(divScore)')
            break
        numMatches = len(divScore)
        t6 = []
        t8 = []
        t10 = []
        for i in range(0, numMatches):
            if divTunes[i] == 6:
                t6.append(divScore[i])
            if divTunes[i] == 8:
                t8.append(divScore[i])
            if divTunes[i] == 10:
                t10.append(divScore[i])
        m6 = sum(t6) / len(t6)
        m8 = sum(t8) / len(t8)
        m10 = sum(t10) / len(t10)
        print('6 Points avg for D' + str(div) + ' (numMatches: ' + str(len(t6)) + '):', str(m6))
        print('8 Points avg for D' + str(div) + ' (numMatches: ' + str(len(t8)) + '):', str(m8))
        print('10 Points avg for D' + str(div) + ' (numMatches: ' + str(len(t10)) + '):', str(m10) + '\n')   
        plt.scatter(x = divScore, y = divTunes)
        plt.title('Runner Score Distribution Across GSC\n' + 'D' + str(div))
        plt.xlabel('Scores')
        plt.ylabel('Tunes Points')
        plt.ylim([5,11])
        plt.show()
        currDiv += 1

def main():

    matches_D, player_alls_D, team_alls_D, p_ids_D, t_ids_D = neccsary()
    # Commentable functions
    #average(player_alls_D)
    #perfect(matches_D)
    #top_scores(matches_D)
    #score_dist(matches_D, False)
    #wins_five(matches_D, t_ids_D)
    #tunes(matches_D, t_ids_D)
    cmpTunesToRealScore(matches_D)


    #print(len(matches_D[6][30].players))
    #print(t_ids_D[5])

main()

