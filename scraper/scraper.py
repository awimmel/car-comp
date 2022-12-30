import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# These imports are not used yet, but will be if the code segment at the bottom of the file is ever fully implemented
# If that ever happens to be the case, the README will be updated accordingly
# from bs4 import Comment
# import re

# Generating CSVs to store collected data
def genCSV():
    # Map storing team abbreviations from PFR as well as each team's first year as an official NFL franchise
    # Establishment years are important to ensure that we only access valid pages on PFR
    teams_and_years = {"crd": 1920, "atl": 1966, "rav": 1996, "buf": 1960, "car": 1995, "chi": 1920, "cin": 1968, "cle": 1950,
            "dal": 1960, "den": 1960, "det": 1930, "gnb": 1921, "htx": 2002, "clt": 1953, "jax": 1995, "kan": 1960,
            "rai": 1960, "sdg": 1960, "ram": 1937, "mia": 1966, "min": 1961, "nwe": 1960, "nor": 1967, "nyg": 1925,
            "nyj": 1960, "phi": 1933, "pit": 1933, "sfo": 1950, "sea": 1976, "tam": 1976, "oti": 1960, "was": 1932}
    
    # Building array of years to examine
    years = []
    curr_year = 1990
    while curr_year <= 2021:
        years.append(curr_year)
        curr_year += 1

    # Creating dataframes in which to store accumulated statistics and rankings
    offense_stats = pd.DataFrame()
    defense_stats = pd.DataFrame()
    offense_ranks = pd.DataFrame()
    defense_ranks = pd.DataFrame()

    # Iterating through each year and team combination, ensuring that each combination is valid before
    # attempting to access any PFR page
    for year in years:
        for team in teams_and_years:
            if year >= teams_and_years[team]:
                # Retrieving current team and year's page, finding the team's record
                init_url = f"https://www.pro-football-reference.com/teams/{team}/{year}.htm"
                page = requests.get(init_url)
                soup = BeautifulSoup(page.content, "html.parser")
                record_info = soup.find("div", id="meta")
                
                # Printing to track the status of the data collection
                print(team)
                print(year)
                print()
                print()

                # Ensuring that there is actually record information to pull from before continuing
                if record_info is not None:
                    record_info = record_info.find_all("p")[2].text.split(" ")[1]
                    record = record_info[:len(record_info) - 1]

                    # Retrieving team statistics, reading statistics into table and renaming columns
                    stats_table = soup.find("table", id="team_stats").find_all("tr")
                    stats_table =  [str(row) for row in stats_table]
                    stats_table = "".join(stats_table[1:6])
                    stats_table = "<table>" + stats_table + "</table>"
                    team_stats = pd.read_html(stats_table)[0]
                    
                    team_stats.rename(columns={"Player": "Team", "Yds.1": "Pass Yds", "1stD.1": "Pass 1stD",
                        "Att.1": "Rushes", "Yds.2": "Rush Yds", "TD.1": "Rush TD", "1stD.2": "Rush 1stD",
                        "Yds.3": "Penalty Yds", "Yds.4": "Yds/Drive"}, inplace=True)
                    
                    # Recording team, year, and record, setting index to team
                    team_stats["Team"] = team + '-' + str(year)
                    team_stats["Record"] = record
                    team_stats = team_stats.set_index("Team")
                    
                    # Concatenating offensive and defensive stats for storage
                    offense_stats = pd.concat([offense_stats, team_stats[0:1]])
                    defense_stats = pd.concat([defense_stats, team_stats[1:2]])

                    # Extracting information about team rankings within the NFL for statistics
                    ranks = team_stats[2:4]

                    # Popping statistics that are not ranked league-wide
                    ranks.pop("Ply")
                    ranks.pop("Y/P")
                    ranks.pop("Cmp")
                    ranks.pop("Pass 1stD")
                    ranks.pop("Rush 1stD")
                    ranks.pop("Pen")
                    ranks.pop("Penalty Yds")
                    ranks.pop("1stPy")

                    # Only popping this statistic if it is available. Not available for many of the earlier stat pages
                    if ('Penalties', "#Dr") in ranks.columns:
                        ranks.pop(("Penalties", "#Dr")) 

                    # Storing offensive and defensive team ranks
                    offense_ranks = pd.concat([offense_ranks, ranks[0:1]])
                    defense_ranks = pd.concat([defense_ranks, ranks[1:2]])
                    
                # Sleeping to abide by the PFR bot rules
                time.sleep(3.16)


    # After data collection has completed, writing information to CSV for retrieval later 
    offense_stats.to_csv('../data/offense_stats.csv')
    defense_stats.to_csv('../data/defense_stats.csv')
    offense_ranks.to_csv('../data/offense_ranks.csv')
    defense_ranks.to_csv('../data/defense_ranks.csv')


if __name__ == "__main__":
    genCSV()





# Logic for gaining information about different matchups
# Will work with adding a sleep statement to avoid timeout from Pro Football Reference, could be implemented
# for future analysis
# all_games = pd.DataFrame()
#     for year in years:
#         max_weeks = 21 
#         if year == 2021:
#             max_weeks = 22

#         for week in range(max_weeks):
#             init_url = f"https://www.pro-football-reference.com/years/{year}/week_{week}.htm"
#             page = requests.get(init_url)
#             soup = BeautifulSoup(page.content, "html.parser")
#             weekly_games = soup.find_all("td", class_="right gamelink")
#             for game in weekly_games:
#                 game_specific_info = game.find("a")["href"]
#                 game_url = "https://www.pro-football-reference.com" + game_specific_info + "#team_stats"
#                 game_page = requests.get(game_url)
#                 game_soup = BeautifulSoup(game_page.content, "html.parser")
#                 # This StackOverflow answer helped me in successfully extracting the comments from the HTML
#                 for comment in game_soup.find_all(string=lambda text: isinstance(text, Comment)):
#                     stats_table = BeautifulSoup(comment, "html.parser").find_all("table", id="team_stats")
#                     if len(stats_table) != 0:
#                         game_stats = pd.read_html(str(stats_table[0]))[0]
#                         game_stats.rename(columns={"Unnamed: 0": "Team"}, inplace=True)
#                         game_stats = game_stats.append({"Team": "Opponent", game_stats.columns[1]: game_stats.columns[2], game_stats.columns[2]: game_stats.columns[1]}, ignore_index=True)
#                         date_to_extract = game_specific_info.split("/")[2]
#                         regex = re.match(r'[0-9]*', date_to_extract)[0]
#                         unformatted = regex[:len(regex)-1]
#                         format_date = unformatted[4:6] + "/" + unformatted[6:8] + "/" + unformatted[0:4]
#                         game_stats = game_stats.append({"Team": "Date of Game", game_stats.columns[1]: format_date, game_stats.columns[2]: format_date}, ignore_index=True)
#                         game_stats = game_stats.transpose()
#                         all_games.append(game_stats)
#         break
#     all_games.to_csv('../data/test.csv', header=False)

