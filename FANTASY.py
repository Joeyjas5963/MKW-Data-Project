from MKTBAPI import *
from MKOBJECT import *
from collections import defaultdict


def load_qdf(file):

    with open(file, 'r', encoding='utf-8') as infile:

        df = pd.read_csv(infile)

    return df


def player_calc(df_player, player_all, week):

    m = week * 2

    for x in range(len(df_player)):
        player_all.fantasy_spread = defaultdict(lambda: [])

        player_all.fantasy = sum(player_all.points)
        player_all.fantasy_spread['Earned'] += player_all.points

        if len(player_all.points) != m:
            player_all.fantasy += 45 * (m - len(player_all.points))
            for i in range(m - len(player_all.points)):
                player_all.fantasy_spread['Benched'].append(45)

        for scores in player_all.race_scores:
            for score in scores:
                if score < 2:
                    player_all.fantasy += 4
                    player_all.fantasy_spread['Bagged'].append(4)

        player_all.fantasy_spread = dict(player_all.fantasy_spread)


def team_calc(team_all):

    score = 0

    for player_list in team_all.players:
        for player in player_list:
            score += player.points

    team_all.fantasy = score // 4


def leaderboard(player_alls):

    score = {}

    for player_all in player_alls:
        score[player_all.tag_name] = player_all.fantasy

    ds_leaderboard = pd.Series(score).sort_values(ascending=False)

    return ds_leaderboard


def quick_calc(player_alls, p_ids, df_quick, week):

    df_calc = df_quick.iloc[:, 1:]
    print(df_calc.head(10).to_string())
    dct = defaultdict(lambda: [])

    for i in range(len(df_calc)):
        for j in range(len(df_calc.columns)):
            selection = df_calc.iloc[i, j]
            if selection in p_ids.keys():
                player_all = player_alls[p_ids[selection]]
                dct[df_quick.iloc[i, 0]].append(player_all.fantasy)

            else:
                dct[df_quick.iloc[i, 0]].append('NA')

    df_quick_num = pd.DataFrame(dct).transpose()

    for i in range(len(df_quick_num)):
        for j in range(len(df_quick_num.columns)):
            if df_quick_num.iloc[i, j] == 'NA':
                df_quick_num.iloc[i, j] = 45*week*2

    total = []

    for i in range(len(df_quick_num)):
        t = sum(df_quick_num.iloc[i, :])
        total.append(t)

    df_quick_num['Total'] = total

    columns = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'Total']
    df_quick_num.columns = columns

    df_quick_num = df_quick_num.sort_values('Total', ascending=False)

    return df_quick_num


def regular_calc(player_alls, team_alls,  p_ids, t_ids, draft, week):

    print(draft.to_string())

    df_calc = draft.iloc[:, 1:]
    dct = defaultdict(lambda: [])

    for i in range(len(df_calc.columns)):
        for j in range(len(df_calc)):

            selection = df_calc.iloc[j, i]

            if selection in p_ids.keys():

                player_all = player_alls[p_ids[selection]]
                dct[draft.columns[i + 1]].append(player_all.fantasy)

            elif selection in t_ids.keys():
                team_all = team_alls[t_ids[selection]]
                dct[draft.columns[i + 1]].append(team_all.fantasy)

            else:
                print('BRUH')
                print(selection)
                dct[draft.columns[i + 1]].append('NA')

    df_regular_num = pd.DataFrame(dct)

    for i in range(len(df_regular_num)):
        for j in range(len(df_regular_num.columns)):
            if df_regular_num.iloc[i, j] == 'NA':
                df_regular_num.iloc[i, j] = 45 * week * 2

    df_regular_num['Choice'] = draft.iloc[:, 0]
    df_regular_num = df_regular_num.set_index('Choice')

    df_regular_num.loc['Total'] = df_regular_num[:].sum()

    print(df_regular_num.to_string())

    df_totals = df_regular_num.iloc[-1, :].transpose().sort_values(ascending=False)
    print(df_totals)


def quick_check(df_quick, df_quick_num, draft):

    nums = df_quick_num.loc[draft]

    for i in range(len(df_quick.iloc[:, 0])):
        if df_quick.iloc[i, 0] == draft:
            picks = df_quick.iloc[i, :]

    df_draft = pd.DataFrame()
    df_draft['Picks'] = picks
    df_draft['Points'] = nums
    df_draft = df_draft.iloc[1:, :]
    df_draft.loc['Total', :] = [draft, sum(df_draft.loc[:, 'Points'])]
    print(df_draft)


def fantasy_crucial():

    week = 2
    df_quick = load_qdf('Quick Drafts.csv')
    draft = load_qdf('Bt Draft.csv')
    matches, player_alls, team_alls, p_ids, t_ids, df_player, df_team = api_crucial()

    for player_all in player_alls:
        player_calc(df_player, player_all, week)

    for team_all in team_alls:
        team_calc(team_all)

    return df_quick, draft, player_alls, team_alls, p_ids, t_ids, week


def fantasy_main():

    df_quick, draft, player_alls, team_alls, p_ids, t_ids, week = fantasy_crucial()

    ds_leaderboard = leaderboard(player_alls)
    print(ds_leaderboard.to_string())
    #player_alls[p_ids['Sk GamerLife']].show_fantasy()

    df_quick_num = quick_calc(player_alls, p_ids, df_quick, week)
    print(df_quick_num.to_string())

    #regular_calc(player_alls, team_alls,  p_ids, t_ids, draft, week)

    """
    while True:
        p = str(input('Which Person?'))
        if p == 'n':
            break
        else:
            quick_check(df_quick, df_quick_num, p)
    """


fantasy_main()
