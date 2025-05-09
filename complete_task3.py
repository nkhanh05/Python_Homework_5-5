import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def load_and_preprocess_data():
    """Đọc và tiền xử lý dữ liệu"""
    try:
        df = pd.read_csv('result.csv', na_values=['N/a', 'NA', 'NaN'])
        return df.iloc[:, 5:].fillna(0)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return None

def scale_data(data):
    """Chuẩn hóa dữ liệu"""
    scaler = StandardScaler()
    return scaler.fit_transform(data), scaler

def perform_clustering(data, n_clusters=3):
    """Thực hiện phân cụm K-Means"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    return kmeans.fit_predict(data)

def visualize_clusters(data, clusters, n_clusters, filename):
    """Trực quan hóa kết quả cụm bằng PCA 2D"""
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)
    
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(reduced_data[:, 0], reduced_data[:, 1], 
                         c=clusters, cmap='viridis', alpha=0.6)
    plt.title(f'Phân cụm {n_clusters} nhóm cầu thủ', fontsize=14)
    plt.xlabel('Thành phần chính 1', fontsize=12)
    plt.ylabel('Thành phần chính 2', fontsize=12)
    plt.colorbar(scatter, label='Nhóm')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def save_cluster_results(df, clusters, filename):
    """Lưu kết quả phân cụm vào file"""
    df['Cluster'] = clusters
    with open(filename, 'w', encoding='utf-8') as f:
        for group in sorted(df['Cluster'].unique()):
            f.write(f"\n{' NHÓM ' + str(group) + ' ':-^50}\n")
            for name in df[df['Cluster'] == group]['Name']:
                f.write(f"- {name}\n")

def main():
    # Thực hiện toàn bộ quy trình
    data = load_and_preprocess_data()
    if data is None:
        return
    
    # Chuẩn hóa dữ liệu
    scaled_data, _ = scale_data(data)
    
    # Phân cụm với 3 nhóm
    clusters = perform_clustering(scaled_data, n_clusters=3)
    
    # Lưu kết quả và hình ảnh
    df = pd.read_csv('result.csv', na_values=['N/a', 'NA', 'NaN'])
    save_cluster_results(df, clusters, 'ket_qua_phan_cum.txt')
    visualize_clusters(scaled_data, clusters, 3, 'phan_cum_2d.png')

if __name__ == "__main__":
    main()