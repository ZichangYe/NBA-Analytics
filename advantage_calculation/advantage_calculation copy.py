# calculate advantages using past games lineup data
# in specific, OFFRTG, and DEFRTG

import pandas as pd
import numpy as np
import os
import random
path = os.getcwd()
name = pd.read_csv(path + '/name_abb.csv')
name_dict = dict(zip(name['Franchise'],name['Abbreviation/Acronym']))

# import the lineup csv
temp = pd.read_csv(path + '/all_combined.csv')

# there is no away team, so I am going to find one.
sche = pd.read_csv(path+'/total_schedule.csv')

sche_home_away_date = sche[['Visitor/Neutral','Home/Neutral',
                            'Home_abb',
                            'Date_fmt',
                            'Season','PTS','PTS.1']]

sche_home_away_date.columns = ['Visitor/Neutral','Home/Neutral',
                               'TEAM','GAMEDAY',
                               'SEASON','AWAYSCORE','HOMESCORE']
# format the date into datetime stamp
sche_home_away_date['GAMEDAY_FMT'] = pd.to_datetime(sche_home_away_date.GAMEDAY)

# find the abbrevation for away team
sche_home_away_date['AWAY'] = [name_dict[n] for n in sche_home_away_date['Visitor/Neutral']]

# add the season in temp
temp['SEASON'] = [gameday[0:4] for gameday in temp['GAMEDAY']]

sche_home_away_date['SEASON_FMT'] = sche_home_away_date['SEASON'].str.replace( "\-\d\d", "")

# find all previous games of two team
# including their last season
def findpreviousgames(home, away, pred_day, season, include_last = True):
    prev_season = str(int(season) -1)
    all_last_season_home_games = sche_home_away_date.loc[(sche_home_away_date['SEASON_FMT'] == prev_season) &
                                                 (sche_home_away_date['GAMEDAY_FMT'] < pred_day) &
                                                 ((sche_home_away_date['TEAM'] == home) &
                                                 (sche_home_away_date['AWAY'] == away))]
    all_last_season_away_games = sche_home_away_date.loc[(sche_home_away_date['SEASON_FMT'] == prev_season) &
                                                 (sche_home_away_date['GAMEDAY_FMT'] < pred_day) &
                                                 ((sche_home_away_date['TEAM'] == away) &
                                                 (sche_home_away_date['AWAY'] == home))]
    all_this_season_home_games = sche_home_away_date.loc[(sche_home_away_date['SEASON_FMT'] == season) &
                                                 (sche_home_away_date['GAMEDAY_FMT'] < pred_day) &
                                                 ((sche_home_away_date['TEAM'] == home) &
                                                 (sche_home_away_date['AWAY'] == away))]
    all_this_season_away_games = sche_home_away_date.loc[(sche_home_away_date['SEASON_FMT'] == season) &
                                                 (sche_home_away_date['GAMEDAY_FMT'] < pred_day) &
                                                 ((sche_home_away_date['TEAM'] == away) &
                                                 (sche_home_away_date['AWAY'] == home))]
    if include_last:
        return pd.DataFrame(pd.concat([all_last_season_home_games,
                                    all_last_season_away_games,
                                    all_this_season_home_games,
                                    all_this_season_home_games]))
    else:
        return pd.DataFrame(pd.concat([all_this_season_home_games,
                                    all_this_away_games]))

# find lineups data
def find_lineups_stats(team,gameday):
    stats = temp.loc[(temp['TEAM'] == team) & (temp['GAMEDAY'] == gameday)]
    return stats

# calculate the relevant features: weighted average of their feature
# weighted by time played in the game
def calculate_weighted_feature(season,lineup_stats,
                               feature,
                               max_lineup_considered = 10,
                               time_disc = 0.90):
    # try:
    total_time = np.sum(lineup_stats['MIN'])
    weighted_feature = 0

    for index, lineup in lineup_stats.iterrows():
        # previous data is discounted
        if int(lineup['SEASON']) < int(season):
            # print(type(time_disc))
            # print(type(lineup['MIN']/total_time))
            # print(type(lineup[feature]))
            weighted_feature += \
            time_disc * (((lineup['MIN']/total_time) * float(lineup[feature])))
        else:
            weighted_feature += \
            (((lineup['MIN']/total_time) * float(lineup[feature])))
        if index > 10:
            break

    return weighted_feature

# except:
    # print('Error')
#         print(lineup_stats.head())

def find_lineup_records_for_two_teams(games, home, away):
    team1_stats = pd.DataFrame()
    team2_stats = pd.DataFrame()
    for index, game in games.iterrows():
        # we don't know who is home
        team1 = game['TEAM']
        team2 = game['AWAY']

        if index == 1:
            team1_stats = find_lineups_stats(home,game['GAMEDAY'])
            team2_stats = find_lineups_stats(away,game['GAMEDAY'])
        else:
            team1_stats = pd.concat([team1_stats,find_lineups_stats(home,game['GAMEDAY'])])
            team2_stats = pd.concat([team2_stats,find_lineups_stats(away,game['GAMEDAY'])])

    return (team1_stats,team2_stats)

if __name__ == "__main__":

    # target data is what we what
    targ_data = sche_home_away_date[['TEAM','AWAY',
                                    'GAMEDAY_FMT','SEASON_FMT',
                                    'AWAYSCORE','HOMESCORE']]
    # construct a target variable
    targ_data['HOMEWIN'] = [int(int(game['AWAYSCORE']) < int(game['HOMESCORE'])) \
                            for index, game in targ_data.iterrows()]
    # testing on five games
    feature_name = ['HOME_AST%','AWAY_AST%','HOME_AST/TO', 'AWAY_AST/TO',
 'HOME_AST RATIO',
 'AWAY_AST RATIO',
 'HOME_OREB%',
 'AWAY_OREB%',
 'HOME_DREB%',
 'AWAY_DREB%',
 'HOME_REB%',
 'AWAY_REB%',
 'HOME_TO RATIO',
 'AWAY_TO RATIO',
 'HOME_EFG%',
 'AWAY_EFG%',
 'HOME_TS%',
 'AWAY_TS%',
 'HOME_PACE',
 'AWAY_PACE',
 'HOME_PIE',
 'AWAY_PIE']

    storage = [[] for _ in range(len(feature_name))]
    calculated_features_storage = dict(zip(feature_name,storage))
    num_runs = 0
    start = 0
    end = len(targ_data) - 1
    print('Running the script from Game ' + str(start) + ' to Game ' + str(end))

    for index, game in targ_data.iloc[start:].iterrows():
        # print(game)
        num_runs += 1
        # first finds all previous games
        home = game['TEAM']
        away = game['AWAY']
        gameday = game['GAMEDAY_FMT']
        season = game['SEASON_FMT']
        feature = ['AST%','AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%',
       'TS%', 'PACE', 'PIE']
        home_feature = 0
        away_feature = 0
        try:
            previous_games_now = findpreviousgames(home = home, away = away,
                                              pred_day = gameday,
                                              season = season)
            # print(previous_games_now.head())

            # then finds the relevant lineup stats
            homestats, awaystats = find_lineup_records_for_two_teams(previous_games_now,
                                                                    home = home,
                                                                    away = away)
            # print(homestats.columns)
            # print(awaystats.head())

            # then calculate the weighted features
            for feat in feature:
                # print(feat)
                home_feature = calculate_weighted_feature(season = season,
                                                           lineup_stats= homestats,
                                                           feature = feat)
                # print('Home_' + str(feat) + str(home_feature))
                away_feature = calculate_weighted_feature(season = season,
                                                           lineup_stats= awaystats,
                                                           feature = feat)
                # print('away_' + str(feat) + str(away_feature))

                # store it somewhere
                for key in calculated_features_storage.keys():
                    if key.endswith("_"+str(feat)) & key.startswith('H'):
                        if home_feature == None:
                            calculated_features_storage[key].append('NaN')
                        else:
                            calculated_features_storage[key].append(home_feature)

                    elif key.endswith("_"+str(feat)) & key.startswith('A'):
                        if away_feature == None:
                            calculated_features_storage[key].append('NaN')
                        else:
                            calculated_features_storage[key].append(away_feature)

        # print([len(l) for l in calculated_features_storage.values()])
        # print(calculated_features_storage.values())

        except:
            print('Error')

        print('Number of Runs: ', num_runs)

    result = pd.DataFrame(calculated_features_storage)
    startend = [str(start),str(end)]
    result.to_csv('result_{0}_{1}.csv'.format(startend[0],startend[1]))
