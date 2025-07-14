# pip install numpy pandas PCA DBSCAN

import os
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# 1. 가상의 고차원 데이터 생성 (나중에는 사용자 정보로 집어넣어야 함)
# np.random.seed(3)
# n_samples = 500
# n_features = 5
# data = np.random.randn(n_samples, n_features)

# 1. testdata.py로 생성한 테스트 데이터 사용
base_path = os.path.dirname(__file__)  # 현재 py 파일 경로
file_path = os.path.join(base_path, "skewed_fitness_data.npy")
data = np.load(file_path)

# 2. 데이터 스케일링
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# 3. PCA를 사용하여 2차원으로 차원 축소
pca = PCA(n_components=2)
data_2d = pca.fit_transform(data_scaled)

# 4. 노이즈가 포함된 클러스터링을 수행 (DBSCAN 사용)
db = DBSCAN(eps=0.5, min_samples=10).fit(data_2d)
labels = db.labels_

# 5. 클러스터링 시각화 (노이즈 포함)
# plt.figure(figsize=(10, 7))
# unique_labels = set(labels)
# colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         col = 'k'  # 노이즈는 검정색으로 표시
# 
#     class_member_mask = (labels == k)
#     xy = data_2d[class_member_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

# plt.title('PCA-reduced Data clustered by DBSCAN (with Noise)')
# plt.show()

# 6. 클러스터 내 원소 수 제한하는 클러스터링 (예: KMeans + 제한)
def constrained_kmeans(data, max_elements_per_cluster, min_elements_per_cluster):
    # 클러스터 수 결정
    n_samples = data.shape[0]
    n_clusters = n_samples // max_elements_per_cluster
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    labels = kmeans.labels_
    unique_labels = set(labels)
    counts = np.bincount(labels)

    # 최대값 제한 처리
    for label in unique_labels:
        if counts[label] > max_elements_per_cluster:
            excess_indices = np.where(labels == label)[0]
            excess_indices = excess_indices[max_elements_per_cluster:]

            # 가장 가까운 클러스터를 찾아 이동
            for idx in excess_indices:
                distances = np.linalg.norm(data[idx] - kmeans.cluster_centers_, axis=1)
                sorted_indices = np.argsort(distances)
                for new_label in sorted_indices:
                    if counts[new_label] < max_elements_per_cluster:
                        labels[idx] = new_label
                        counts[label] -= 1
                        counts[new_label] += 1
                        break
    
    # 최소값 제한 처리
    for label in unique_labels:
        if counts[label] < min_elements_per_cluster:
            deficit_indices = np.where(labels == label)[0]
            
            # 가장 가까운 클러스터로부터 원소를 가져옴
            for idx in deficit_indices:
                distances = np.linalg.norm(data[idx] - kmeans.cluster_centers_, axis=1)
                sorted_indices = np.argsort(distances)
                for new_label in sorted_indices:
                    if counts[new_label] > min_elements_per_cluster:
                        labels[idx] = new_label
                        counts[label] += 1
                        counts[new_label] -= 1
                        if counts[label] >= min_elements_per_cluster:
                            break
                if counts[label] >= min_elements_per_cluster:
                    break
    
    return labels


max_elements_per_cluster = 6
min_elements_per_cluster = 2
constrained_labels = constrained_kmeans(data_2d, min_elements_per_cluster, max_elements_per_cluster)

# 7. 클러스터링 시각화 (제한된 클러스터)
plt.figure(figsize=(10, 7))
unique_labels = set(constrained_labels)
# colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
colors = plt.get_cmap("Spectral")(np.linspace(0, 1, len(unique_labels)))

for k, col in zip(unique_labels, colors):
    class_member_mask = (constrained_labels == k)
    xy = data_2d[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

plt.title('GroupPT Clustering')
plt.show()