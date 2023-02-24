import re

player_csv = open("P_Data.csv")
name_and_tags = []
names = []
for line in player_csv.readlines()[1:]:
    line_arr = line.split(",")
    names.append(line_arr[2])
    name_and_tags.append(line_arr[3])

team_csv = open("T_Data.csv")
team_names = []
team_tags = []
invalid_team_tags=[]
for line in team_csv.readlines()[1:]:
    line_arr = line.split(",")
    team_names.append(line_arr[2])
    team_tags.append(line_arr[3])
    invalid_team_tags.append(line_arr[5])


def check_player(player):
    if player not in name_and_tags:
        if '(' in player:
            tag = re.search(r"\((.*?)\)", player).group(1)
            name = re.sub(r"\(.*?\)", "", player)
            player = f"{tag} {name}"
            new_player = check_player(player)
            return new_player

        tag, name = player.rsplit(" ", 1)[0], player.rsplit(" ", 1)[-1]

        if name.lower() in [x.lower() for x in names] and name not in names:
            new_player = check_player(f"{player.rsplit(' ', 1)[0]} {names[[x.lower() for x in names].index(name.lower())]}")
            return new_player

        if name in names:
            suggested_name_and_tag=name_and_tags[names.index(name)]
            confirmation = input(f"Found {name} in registry, but as a member of {suggested_name_and_tag.rsplit(' ', 1)[0]} instead of {player}, correct it? (y/n) ")

            if confirmation.lower() in ["y", "yes"]:
                return suggested_name_and_tag

            else:
                new_player=input("Please enter the tag and name that it should be corrected to (try and use the correct symbols for the tag): ")
                new_player=check_player(new_player)
                return new_player


        else:
            pass

    elif len(player.split(" ")) == 0 and player in names: #if theres no tag
        suggested_player = name_and_tags[names.index[player]]
        confirmation = input(f"Player found but tag not specified, did you mean {suggested_player}? (y/n)")

        if confirmation.lower() in ["y", "yes"]:
            return suggested_player

        else:
            inputted_correction = input("Enter the tag for the team the player: ")
            new_player = check_player(inputted_correction)
            return new_player
    elif player in name_and_tags:
        return player
    else:
        inputted_correction = input(f"{player} didnt match any instances, Enter the tag for the team the player: ")
        new_player = check_player(inputted_correction)
        return new_player


def check_team(team):
    if team not in team_tags:
        if team not in invalid_team_tags:
            new_team_input=input(f"Could not find {team} in registry, please change it here: ")
            new_team=check_team(new_team_input)

        elif team in invalid_team_tags:

            suggested_correct_team = team_tags[invalid_team_tags.index(team)]
            if "2" in team:
                suggested_correct_team+="2"
            while True:
                confirmation=input(f"Could not find {team} in registry, did you mean {suggested_correct_team}? Y/N ")

                if confirmation.lower() in ["y", "yes"]:
                    return suggested_correct_team

                elif confirmation.lower() in ["n", "no"]:
                    new_team_input=input("Please enter the tag that it should be corrected to (try and use the correct symbols for the tag): ")
                    new_team=check_team(new_team_input)
                    return new_team

                else:
                    return "ERROR"
    else:
        return team

with open("V$ Draft.csv") as csv_file:
    csv_copy = csv_file.read()
    lines = csv_copy.split("\n")
    for x in range(1, len(lines)):
        line = lines[x]
        if line.split(",")[0].lower() == "team":
            corrected_teams=[line.split(",")[0]]
            for team in line.split(",")[1:-1]:
                corrected_team = check_team(team)
                corrected_teams.append(corrected_team)
            lines[x] = ",".join(corrected_teams)
        else:
            corrected_players = [line.split(",")[0]]
            for player in line.split(",")[1:-1]:
                corrected_player=check_player(player)
                corrected_players.append(corrected_player)
            lines[x]=",".join(corrected_players)
    new_csv = open("new_csv.csv", "w")
    new_csv.write("\n".join(lines))
    new_csv.close()
    print("File saved as new_csv.csv")