import requests
import pandas as pd

from bs4 import BeautifulSoup

url = "https://fbref.com/en/comps/9/Premier-League-Stats"
data = requests.get(url)
soup = BeautifulSoup(data.text)

def get_links(retrieved_data):
    standings_table = soup.select('table.stats_table')[0]
    links = [l.get("href") for l in standings_table.find_all('a')]
    links = [l for l in links if retrieved_data in l ]
    links = [f"https://fbref.com{link}" for link in links]
    return links

def team_name():
    link_squads = get_links("/squads/")
    link_squads = [f"https://fbref.com{link}" for link in link_squads]
    teams=[]
    # print(links)
    for team_url in link_squads:
        team_name = team_url.split("/")[-1].replace('-Stats','').replace('-',' ')
        teams.append(team_name)
    return teams

if __name__ == "__main__":
    link_squads = get_links("/squads")
    for link in link_squads[:1]:
        # print(link)
        data_teams = requests.get(link)
        soup_raw_data = BeautifulSoup(data_teams.text)

        data_result = pd.read_html(data_teams.text, match="Scores & Fixtures")[0]

        link_data = [l.get("href") for l in soup_raw_data.find_all('a')]
        link_shooting = [l for l in link_data if l and '/all_comps/shooting' in l]
        link_passing = [l for l in link_data if l and '/all_comps/passing' in l]
        link_possession = [l for l in link_data if l and '/all_comps/possession' in l]
        link_shooting = f"https://fbref.com{link_shooting[0]}"
        link_passing = f"https://fbref.com{link_passing[0]}"
        link_possession = f"https://fbref.com{link_possession[0]}"
        # print(link_shooting)

        data_shooting = requests.get(link_shooting)
        data_passing = requests.get(link_passing)
        data_possession = requests.get(link_possession)
        shooting = pd.read_html(data_shooting.text, match="Shooting")[0]
        passing = pd.read_html(data_passing.text, match="Passing")[0]
        possession = pd.read_html(data_possession.text, match="Possession")[0]
        shooting_agn = pd.read_html(data_shooting.text, match="Shooting")[1]
        passing_agn = pd.read_html(data_passing.text, match="Passing")[1]
        possession_agn = pd.read_html(data_possession.text, match="Possession")[1]
        shooting.columns = shooting.columns.droplevel() 
        passing.columns = passing.columns.droplevel() 
        possession.columns = possession.columns.droplevel() 
        shooting_agn.columns = shooting_agn.droplevel()
        passing_agn.columns = passing_agn.droplevel()
        possession_agn.columns = possession_agn.droplevel()


        #insert data shooting 'Date','GF', 'GA', 'Gls', 'Sh', 'SoT','Dist','FK','PK','xG',npxG', on 'Date
        #ambil data passing 'Date','Cmp'(complete),'Att'(attemp), 'TotDist'(total distance), 'PrgDist'(progresive passing distance),'Ast', 'xAG', 'xA','KP', '1/3', 'PPA', 'CrsPA', 'PrgP'
        #ambil data posession 

        # print(data_shooting.text)
        # print(passing.columns)
        # print(possession.columns)













    # print(links)
    # for team_url in links[:1]:
    #     data = requests.get(team_url)
    #     print(f"team_url : {team_url}")
    #     # matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
    #     shooting = pd.read_html(data.text, match="Shooting")[0]
    #     print(type(shooting))
    #     links = [l for l in links if l and '/all_comps/shooting' in l]
    #     links = f"https://fbref.com{links[0]}"
    #     data1 = requests.get(links)
    #     shooting = pd.read_html(data1.text, match="Shooting")[0]
    #     shooting.columns = shooting.columns.droplevel()