import os
import copy
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

os.environ['PATH'] += "C:/SeleniumDrivers"
tmp = {
    "Personal Information":
    {
        "f_name": "N/a",
        "l_name": "N/a",
        "nationality": "N/a",
        "team": "N/a",
        "position": "N/a",
        "age": "N/a",
    },
    "Standard Status":
    {
        "Playing time": {
            "games": "N/a",
            "games_starts": "N/a",
            "minutes": "N/a",
        },
        "Performance": {
            "goals": "N/a",
            "assists": "N/a",
            "cards_yellow": "N/a",
            "cards_red": "N/a"
        },
        "Expected": {
            "xg": "N/a",
            "xg_assist": "N/a"
        },
        "Progression": {
            "progressive_carries": "N/a",
            "progressive_passes": "N/a",
            "progressive_passes_received": "N/a"
        },
        "Per 90 minutes": {
            "goals_per90": "N/a",
            "assists_per90": "N/a",
            "xg_per90": "N/a",
            "xg_assist_per90": "N/a"
    }
    },
    "Goalkeeping": {
        "Performance": {
            "gk_goals_against_per90": "N/a",
            "gk_save_pct": "N/a",
            "gk_clean_sheet_pct": "N/a"
        },
        "Penalty Kicks": {
            "gk_pens_save_pct": "N/a"
        }
    },
    "Shooting": {
        "Standard": {
            "shots_on_target_pct": "N/a",
            "shots_per90": "N/a",
            "goals_per_shot": "N/a",
            "average_shot_distance": "N/a"
        }
    },
    "Passing": {
        "Total": {
            "passes_completed": "N/a",
            "passes_pct": "N/a",
            "passes_total_distance": "N/a"
        },
        "Short": {
            "passes_pct_short": "N/a"
        },
        "Medium": {
            "passes_pct_medium": "N/a"
        },
        "Long": {
            "passes_pct_long": "N/a"
        },
        "Expected": {
            "assisted_shots": "N/a",
            "passes_into_final_third": "N/a",
            "passes_into_penalty_area": "N/a",
            "crosses_into_penalty_area": "N/a",
            "progressive_passes": "N/a"
        }
    },
    "Goal and Shot Creation": {
        "SCA": {
            "sca": "N/a",
            "sca_per90": "N/a"
        },
        "GCA90": {
            "gca": "N/a",
            "gca_per90": "N/a"
        }
    },
    "Defensive Actions": {
        "Tackles": {
            "tackles": "N/a",
            "tackles_won": "N/a"
        },
        "Challenges": {
            "challenge_tackles": "N/a",
            "challenges_lost": "N/a"
        },
        "Blocks": {
            "blocks": "N/a",
            "blocked_shots": "N/a",
            "blocked_passes": "N/a",
            "interceptions": "N/a"
        }
    },
    "Possession": {
        "Touches": {
            "touches": "N/a",
            "touches_def_pen_area": "N/a",
            "touches_def_3rd": "N/a",
            "touches_mid_3rd": "N/a",
            "touches_att_3rd": "N/a",
            "touches_att_pen_area": "N/a"
        },
        "Take-Ons": {
            "take_ons": "N/a",
            "take_ons_won_pct": "N/a",
            "take_ons_tackled_pct": "N/a"
        },
        "Carries": {
            "carries": "N/a",
            "carries_progressive_distance": "N/a",
            "progressive_carries": "N/a",
            "carries_into_final_third": "N/a",
            "carries_into_penalty_area": "N/a",
            "miscontrols": "N/a",
            "dispossessed": "N/a"
        },
        "Receiving": {
            "passes_received": "N/a",
            "progressive_passes_received": "N/a"
        }
    },
    "Miscellaneous Stats": {
        "Performance": {
            "fouls": "N/a",
            "fouled": "N/a",
            "offsides": "N/a",
            "crosses": "N/a",
            "ball_recoveries": "N/a"
        },
        "Aerial Duels": {
            "aerials_won": "N/a",
            "aerials_lost": "N/a",
            "aerials_won_pct": "N/a"
        }
    }
}
std_source = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
goalkeeping_source="https://fbref.com/en/comps/9/keepers/Premier-League-Stats"
shooting_source = "https://fbref.com/en/comps/9/shooting/Premier-League-Stats"
passing_source = "https://fbref.com/en/comps/9/passing/Premier-League-Stats"
goal_and_shot_creation_source = "https://fbref.com/en/comps/9/gca/Premier-League-Stats"
defensive_source = "https://fbref.com/en/comps/9/defense/Premier-League-Stats"
possession_source = "https://fbref.com/en/comps/9/possession/Premier-League-Stats"
miscellaneous_source = "https://fbref.com/en/comps/9/misc/Premier-League-Stats"

import csv


def print_each(a,f,n_list):
    f.write("Name")
    for key1 in tmp.keys():
        for key2 in tmp[key1]:
                if key2 == "f_name" or key2 == "l_name":
                    continue
                if not isinstance(tmp[key1][key2],dict):
                    f.write(','+key2.capitalize())
                else:
                    for key3 in tmp[key1][key2]:
                        f.write(','+key3.capitalize())

    f.write('\n')
    
    for key1 in n_list:
        f.write(f"{key1}")
        for key2 in a[key1]:
            for key3 in a[key1][key2]:
                if key3 == "f_name" or key3 == "l_name":
                    continue
                if not isinstance(a[key1][key2][key3],dict):
                    f.write(f",{a[key1][key2][key3]}")
                else:
                    for key4 in a[key1][key2][key3]:
                        f.write(f",{a[key1][key2][key3][key4]}")
        f.write('\n')
        



    
    
        

def print_to_file(a,n_list):
    print("Save information to result file!")

    with open("result.csv", "w", encoding="utf-8") as f:
        print_each(a,f,n_list)
    
    print("Save successfully!")
            
def first_name(name):
    a = name.split()
    return a[-1].strip()  # Lấy tên đầu tiên

def last_name(name):
    a = name.split()
    return name.replace(first_name(name),"").strip() # Lấy họ từ tên đầy đủ

def auto_convert(value: str):
    value = value.replace(",", "")
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def get_value(needed_val, row):
    try:
        a = row.find_element(By.CSS_SELECTOR, f'td[data-stat="{needed_val}"]').text.strip()
    except NoSuchElementException:
        return "N/a"
    if a == "":
        return "N/a"
    else:
        return auto_convert(a)
    

def main():
    Fb_players=dict()
    take_players(Fb_players,goalkeeping_source,shooting_source ,passing_source ,goal_and_shot_creation_source,defensive_source ,possession_source, miscellaneous_source,std_source)
    sorted_names = sorted(
    Fb_players,
    key=lambda k: (Fb_players[k]['Personal Information']['f_name'],Fb_players[k]['Personal Information']['l_name'])
)
    print_to_file(Fb_players,sorted_names)
    
        

def take_players(p_l,goalkeeping_source,shooting_source ,passing_source ,goal_and_shot_creation_source,defensive_source ,possession_source, miscellaneous_source,std_source):
    get_std_info(p_l,std_source)
    get_goalkeeping_info(p_l,goalkeeping_source)
    get_passing_info(p_l,passing_source)
    get_shooting_info(p_l,shooting_source)
    get_goal_and_shot_creation_info(p_l,goal_and_shot_creation_source)
    get_defensive_actions_info(p_l,defensive_source)
    get_possession_info(p_l,possession_source)
    get_miscellaneous_stats_info(p_l,miscellaneous_source)
    

def get_goalkeeping_info(a,site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_keeper"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:
        
        print("No goalkeeping information is found")
        i.quit()
        return
    
    
    print("Get goalkeeping information")

    for row in rows:
        name = get_value("player",row)
        
        if name in a:
            for key1 in a[name]["Goalkeeping"]:
                for key2 in a[name]["Goalkeeping"][key1]:
                    a[name]["Goalkeeping"][key1][key2] = get_value(key2,row)
    i.quit()



def get_passing_info(a,site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_passing"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:
        
        print("No passing information is found")
        i.quit()
        return
    
    print("Get passing information")

    for row in rows:
        name = get_value("player",row)
        if name in a:
            for key1 in a[name]["Passing"]:
                for key2 in a[name]["Passing"][key1]:
                    a[name]["Passing"][key1][key2] = get_value(key2,row)
    i.quit()
            

   
def get_shooting_info(a,site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_shooting"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:
        print("No shooting information is found")
        i.quit()
        return

    print("Get Shooting Information")

    for row in rows:
        name = get_value("player",row)
        if name in a:
            for key1 in a[name]["Shooting"]:
                for key2 in a[name]["Shooting"][key1]:
                    a[name]["Shooting"][key1][key2] = get_value(key2,row)
    i.quit()



def get_goal_and_shot_creation_info(a,site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_gca"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:
        print("No goal and shot creation information is found")
        i.quit()
        return
    print("Get Goal and Shot Creation Information")

    for row in rows:
        name = get_value("player",row)
        if name in a:
            for key1 in a[name]["Goal and Shot Creation"]:
                for key2 in a[name]["Goal and Shot Creation"][key1]:
                    a[name]["Goal and Shot Creation"][key1][key2] = get_value(key2,row)
    i.quit()

def get_defensive_actions_info(a, site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_defense"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:
        print("No defensive information is found")
        i.quit()
        return
    print("Get defensive Information")

    for row in rows:
        name = get_value("player",row)
        if name in a:
            for key1 in a[name]["Defensive Actions"]:
                for key2 in a[name]["Defensive Actions"][key1]:
                    a[name]["Defensive Actions"][key1][key2] = get_value(key2, row)
    i.quit()

def get_possession_info(a, site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_possession"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:
        print("No possession information is found")
        i.quit()
        return
    print("Get possession Information") 
    for row in rows:
        name = get_value("player",row)
        if name in a:
            for key1 in a[name]["Possession"]:
                for key2 in a[name]["Possession"][key1]:
                    a[name]["Possession"][key1][key2] = get_value(key2, row)
    i.quit()

def get_miscellaneous_stats_info(a, site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_misc"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:

        print("No miscellaneous information is found")
        i.quit()
        return
    print("Get Miscellaneous Information")
    for row in rows:
        name = get_value("player",row)
        if name in a:
            for key1 in a[name]["Miscellaneous Stats"]:
                for key2 in a[name]["Miscellaneous Stats"][key1]:
                    a[name]["Miscellaneous Stats"][key1][key2] = get_value(key2, row)
    i.quit()



def get_std_info(a,site):
    i = webdriver.Chrome()
    i.get(site)
    try:
        WebDriverWait(i,15).until(
            EC.presence_of_element_located((By.ID, "info"))
        )
        try:

            rows = i.find_elements(By.CSS_SELECTOR, 'table[id="stats_standard"] tbody tr')

        except NoSuchElementException:
            return    
    except TimeoutException:
        print("No standard information is found")
        i.quit()
        return
    print("Get Standard Information")
    for row in rows:
        if isinstance(get_value("minutes",row),int) and get_value("minutes",row) >90:
            name = get_value("player",row)
            a[name]= copy.deepcopy(tmp)
            get_personal_information(a,row)
            for key1 in a[name]["Standard Status"]:
                for key2 in a[name]["Standard Status"][key1]:
                    a[name]["Standard Status"][key1][key2] = get_value(key2, row)
    i.quit()

def get_personal_information(a,row):
    name = get_value("player",row)
    for key in a[name]["Personal Information"]:
        a[name]["Personal Information"][key] = get_value(key, row)
    a[name]["Personal Information"]["f_name"] = first_name(name)
    a[name]["Personal Information"]["l_name"] = last_name(name)
    try:
        a[name]["Personal Information"]["nationality"] = row.find_element(By.CSS_SELECTOR,' table tr td[data-stat="nationality"] a span span').text.strip().upper()
    except NoSuchElementException:
        a[name]["Personal Information"]["nationality"]="N/a"

    




    
    
    

if __name__ == "__main__":
    main()




    
    

        

