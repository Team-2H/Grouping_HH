# pip install numpy pandas PCA DBSCAN

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import groupingLogic


# 1. 가상의 고차원 데이터 생성 (나중에는 사용자 정보로 집어넣어야 함)
# np.random.seed(3)
# n_samples = 500
# n_features = 5
# data = np.random.randn(n_samples, n_features)

# 1. testdata.py로 생성한 테스트 데이터 사용
base_path = os.path.dirname(__file__)  # 현재 py 파일 경로
file_path = os.path.join(base_path, "skewed_fitness_data.npy")
data = np.load(file_path)

groupCount = 20
max_elements_per_cluster = 0
min_elements_per_cluster = 0
constrained_data = groupingLogic.constrained_kmeans(data, groupCount, max_elements_per_cluster, min_elements_per_cluster)

constrained_labels = constrained_data[0]
constrained_centroids = constrained_data[1]

## 테스트용 코드
# 2. 클러스터링 시각화 (제한된 클러스터)
# 2-1. 2차원 데이터 필요
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)
pca = PCA(n_components=2)
data_2d = pca.fit_transform(data_scaled)

plt.figure(figsize=(10, 7))
unique_labels = set(constrained_labels)
colors = plt.get_cmap("Spectral")(np.linspace(0, 1, len(unique_labels)))

for k, col in zip(unique_labels, colors):
    class_member_mask = (constrained_labels == k)
    xy = data_2d[class_member_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

plt.title('GroupPT Clustering')
plt.show()