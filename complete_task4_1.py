from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def open_site():
    arr=[]
    for i in range(1,15):
        general_site = 'https://www.footballtransfers.com/us/leagues-cups/national/uk/premier-league/transfers/2024-2025/'

        site = webdriver.Chrome()
        site.get(f'{general_site}{i}')
        try:
            WebDriverWait(site,15).until(
                EC.presence_of_element_located((By.ID, "template"))
            )
        
        except TimeoutException:
            print("The site is not accessible!")
            site.quit()
        price_df = pd.DataFrame(columns = ['Name','Price'])
        get_rows_info(site,arr)
        site.quit()
    
    price_df = pd.concat([price_df, pd.DataFrame(arr)], ignore_index=True)
    price_df.to_csv('price.csv',index = False)
    create_new_df(price_df)
    

def get_rows_info(site,l):
    
    try:
        
        rows = site.find_elements(By.CSS_SELECTOR, 'table[class="table table-striped table-hover leaguetable mvp-table transfer-table mb-0"] tbody tr')
        print('taking info')
        for row in rows:
            a = row.find_element(By.CSS_SELECTOR, 'td[class="td-player"] div[class = "text"] a').text.strip()
            b = row.find_element(By.CSS_SELECTOR, f'td[class="text-right td-price td-price--no-tag"] span').text.strip()
            d = {'Name': a, 'Price': b}
            l.append(d)
        
        
        
    
    except NoSuchElementException:
        return
    
        
            
def create_new_df(df2):
    df1 = pd.read_csv('result.csv',na_values='N/a')
    df1 = df1[df1['Minutes'] > 900]
    df_merged = pd.merge(df1, df2, on='Name', how='inner')
    df_merged.to_csv('new_stat_table.csv',index = False)

def main():
    open_site()
if __name__ == '__main__':
    
    main()


