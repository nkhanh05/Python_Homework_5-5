import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA



def scaled_data():
    df = pd.read_csv('result.csv',na_values = 'N/a')
    n_df = df.fillna(0)
    n_df = df.iloc[:, [5]]
    scaler = StandardScaler()
    scaler.fit_transform(n_df)
    a = pd.DataFrame(scaler,columns = n_df.columns)
    return scaler
def save_wcss_graph():
    wcss=[]
    for k in range(2,21):

        kmeans = KMeans(n_clusters=k)
        kmeans.fit(scaled_data())
        wcss.append(kmeans.inertia_)
    
    plt.plot(range(2,21),wcss)

    plt.xlabel('Number of cluster')
    plt.ylabel('Inertia')
    plt.title('The Elbow graph')
    plt.savefig('Elbow_graph.png',dpi = 300)

    
    

    

# def save_player_groups():
    
# def save_2d_cluster():

save_wcss_graph()
