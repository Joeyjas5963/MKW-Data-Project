from MKTBAPI import *
from MKOBJECT import *


def track_picks(matches):

    track_dict = defaultdict(lambda: 0)

    for match in matches:
        for track in match.races:
            track_dict[track] += 1

    track_dict = dict(track_dict)

    ds_track = pd.Series(track_dict).sort_values(ascending=False)

    print(ds_track)


def match_graph(match, df_team):

    points_t1 = 0
    points_t2 = 0
    gp_t1 = 0
    gp_t2 = 0
    difs = [0]
    gps = [0]

    ds_teams = list(df_team.loc[:, 'Mii Tag'])

    color1 = df_team.iloc[ds_teams.index(match.t1.name), -1]
    color2 = df_team.iloc[ds_teams.index(match.t2.name), -1]

    for i in range(len(match.races)):

        if i == 4 or i == 8:
            gp_t1 = 0
            gp_t2 = 0

        for player in match.t1.players:
            points_t1 += player.race_scores[i]
            gp_t1 += player.race_scores[i]
        for player in match.t2.players:
            points_t2 += player.race_scores[i]
            gp_t2 += player.race_scores[i]

        dif = points_t1 - points_t2
        gp = gp_t1 - gp_t2
        difs.append(dif)
        gps.append(gp)

    pens = [match.t1.pen, match.t2.pen]

    for i in range(len(pens)):
        if pens[i] != '':
            pens[i] = int(pens[i].split(' ')[1])
        else:
            pens[i] = 0

    final = difs[-1] + pens[0] - pens[1]

    sns.set(rc={'figure.facecolor': '#0d2d35', 'text.color': 'white',
                'xtick.color': 'white', 'ytick.color': 'white',
                'axes.labelcolor': 'white'})
    #sns.set()

    # line
    plt.plot(list(range(len(difs))) + [12.5], difs + [final], 'o-', color=color1, linewidth=4)

    # gp1
    plt.plot([0, 1, 2, 3, 4], [0] + gps[1:5], color='black')
    plt.text(2.5, 108, str(122+gps[4]), color='black', ha='center')
    plt.text(2.5, -78, str(122-gps[4]), color='black', ha='center')

    # gp2
    plt.plot([4.5, 5, 6, 7, 8], [0] + gps[5:9], color='black')
    plt.text(6.5, 108, str(122+gps[8]), color='black', ha='center')
    plt.text(6.5, -78, str(122-gps[8]), color='black', ha='center')

    # gp3
    plt.plot([8.5, 9, 10, 11, 12], [0] + gps[9:], color='black')
    plt.text(10.5, 108, str(122+gps[-1]), color='black', ha='center')
    plt.text(10.5, -78, str(122-gps[-1]), color='black', ha='center')

    # pen
    if pens[0] != 0:
        plt.text(12, 10, str(pens[0]), color='black', ha='center')
    if pens[1] != 0:
        plt.text(12, -20, str(pens[1]), color='black', ha='center')

    plt.scatter(12.5, (difs[-1] + pens[0] - pens[1]), color=color1)

    # bound lines
    plt.axhline(color='black')
    plt.axvline(0.5, color='blue')
    plt.axvline(4.5, color='blue')
    plt.axvline(8.5, color='blue')
    plt.axvline(12.5, color='blue')

    # labels
    plt.xlabel('Races')
    plt.ylabel("Points in Winner's Favor")

    # team 1 name
    plt.text(2.5, 62, match.t1.name, size=40, color='black', ha='center')
    plt.axhspan(0, 150, color=color1, alpha=0.3)

    # team 2 name
    plt.text(2.5, -62, match.t2.name, size=40, color='black', ha='center')
    plt.axhspan(0, -100, color=color2, alpha=0.3)

    # x axis
    plt.xticks((list(range(len(match.races) + 1)))[1:])
    plt.xlim((0.3, 12.7))

    # y axis
    plt.yticks([-93, -62, -31, 0, 31, 62, 93, 124])
    plt.ylim((-100, 125))

    # title
    title = '(' + str(points_t1 + pens[0]) + ') ' + match.t1.name + ' vs. ' + match.t2.name + \
            ' (' + str(points_t2 + pens[1]) + ')'
    plt.title(title)
    plt.show()


def main():
    matches, player_alls, team_alls, p_ids, t_ids, df_player, df_team = api_crucial()

    for match in matches:
        match.small_print()

    #track_picks(matches)
    print(matches[2])

    while True:
        index = int(input('index?'))
        match_graph(matches[index], df_team)


main()
