import pandas as pd
import sys
from tabulate import tabulate
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

def get_goat_table():
    """    
    This function takes my personal list off NBA GOATs,
    and generates a pandas dataframe from the NBA API of their traditional counting stats (PTS/REB/AST).
    """
    
    ball_knower = input("Do you know ball? (y/n): ")

    #My GOATs
    retired_goat_list = [
        "Michael Jordan",
        "Kareem Abdul-Jabbar",
        "Wilt Chamberlain",
        "Bill Russell",
        "Tim Duncan",
        "Kobe Bryant",
        "Oscar Robertson",
        "Larry Bird",
        "Shaquille O'Neal",
        "Magic Johnson"
    ]

    goat_list = []
    career_stats = []
    goat_careerstats = []

    if ball_knower.lower() in ('y' or 'yes'):
        #Get their player IDs from the NBA API
        for goat in retired_goat_list:
            goat_dict = players.find_players_by_full_name(goat)
            goat_id = goat_dict[0]['id']
            goat_list.append({'name':goat, 'id':goat_id})
        
        #Get their stats based on the ID, convert them to a data frame
        for player in goat_list:
            # Fetch career stats
            career_line_obj = playercareerstats.PlayerCareerStats(player_id=player['id'])
            
            # Extract career totals data frame
            career_totals = career_line_obj.get_data_frames()[1] 
            career_totals['PLAYER_NAME'] = player['name']
            career_stats.append(career_totals[['PLAYER_NAME', 'PLAYER_ID', 'GP', 'PTS', 'REB', 'AST']])
        
        #Concatenate each player career totals into a single table
        goat_table = pd.concat(career_stats)
        return goat_table
    
    elif ball_knower.lower() in 'n' or 'no':
        sys.exit("Go watch some ball")
    else:
        sys.exit("Invalid input. Please input 'y' or 'n'")

def get_player():
    """
    This function is to ask the user for an NBA player and generate a dataframe
    for the traditional counting stats.  This dataframe will then be appended 
    to the dataframe with the GOATs for comparison
    """
    
    defendant = input("Who shall be judged?: ")
    defendant_id = players.find_players_by_full_name(defendant)

    if not defendant_id:
        sys.exit("No Player Found. Check spelling.")

    defendant_career_stats_obj = playercareerstats.PlayerCareerStats(player_id=defendant_id[0]['id'])
    defendant_career_table = defendant_career_stats_obj.get_data_frames()[1]
    defendant_career_table['PLAYER_NAME'] = defendant
    defendant_career_table = defendant_career_table[['PLAYER_NAME', 'PLAYER_ID', 'GP', 'PTS', 'REB', 'AST']]

    return defendant_career_table

def concat_tables(table_1, table_2):
    combined_df = pd.concat([table_1, table_2], ignore_index=True)
    return combined_df

def table_sorter(table):
    table['PTS/gm'] = (table['PTS']/table['GP'])
    table['REB/gm'] = (table['REB']/table['GP'])
    table['AST/gm'] = (table['AST']/table['GP'])

    table.drop('PLAYER_ID', axis=1, inplace=True)
    table_rounded = table.round(2)

    try:
        sort_by_stat = input(
            "How shall they be judged? Choose one of PTS, REB, AST, PTS/gm, REB/gm, AST/gm: "
            )
        table_rounded_sorted = table_rounded.sort_values(by=sort_by_stat, ascending=False)
        print(tabulate(table_rounded_sorted, headers='keys', tablefmt='grid', showindex=False))
        print('THEY HAVE BEEN FOUND....WANTING')
        return table_rounded_sorted
    except KeyError:
        sys.exit("Please choose a valid statistical category")


def main():
    #get stats from NBA API and convery to data frame
    df1 = get_goat_table()
    df2 = get_player()
    final_table = concat_tables(df1, df2)
    table_sorter(final_table)
    
    #Calculate per game counting stats
        
if __name__ == "__main__":
    main()
