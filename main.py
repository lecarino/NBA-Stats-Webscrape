import requests
from bs4 import BeautifulSoup
import re
import csv

response = requests.get(url='https://www.nba.com/stats')
nba_webpage = response.text
soup = BeautifulSoup(nba_webpage,'html.parser')

title_spans = soup.find_all(class_="LeaderBoardCard_lbcWrapper__e4bCZ LeaderBoardWithButtons_lbwbCardGrid__Iqg6m LeaderBoardCard_leaderBoardCategory__vWRuZ")
all_categories = [title.getText() for title in title_spans]

date_of_data = soup.find(name= "span", class_="LeaderBoardWithButtons_lbwbDate__gsMEu")
date = date_of_data.getText()

# Dictionary to store cleaned data
cleaned_data = {}

# Process each data entry
for entry in title_spans:
    # Split category and player information
    category, *players_info = entry.getText().split('1. ')
    category, *team_info= category.split('1.')

    # NBA team abbreviations
    team_abbreviations = {'ATL','BOS','BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'}

    # Extract and clean player names using regex
    cleaned_players = [re.sub(r'[^A-Za-z\s]', '', name.strip('.').strip('0123456789')) for info in players_info for name in info.split('.') if len(name) > 3]

    # Remove team abbreviations from player names
    for team in team_abbreviations:
        cleaned_players = [player.replace(team, '').strip() for player in cleaned_players]

    # Filter out empty strings
    cleaned_players = list(filter(None, cleaned_players))

    teams = [name.strip('.').strip('0123456789') for info in team_info for name in info.split('.')]
    cleaned_teams = list(filter(None, teams))
   
    if players_info:
        cleaned_data[f"Player_{category}"] = cleaned_players
    else:
        cleaned_data[f"Team_{category}"] = cleaned_teams

#Write to CSV
csv_file_path = 'nba_stats.csv'
with open(csv_file_path, 'w', newline='') as csvfile:

    csv_writer =  csv.writer(csvfile)

    #Date Of Data
    csv_writer.writerow([f'Stat Leaders for {date}'])

    #Empty Line Separator
    csv_writer.writerow([])

    #Header
    csv_writer.writerow(['Category', 'Values'])

    #Write the Data
    for category, values, in cleaned_data.items():
        csv_writer.writerow([category, values])


