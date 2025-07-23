
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from app.groupingLogic import constrained_kmeans_with_names


def groupingVisualization(raw_data, clustered_result, centroids):
    # 1. raw_data에서 numeric 값만 추출 (name 제외)
    numeric_data = [
        [v for k, v in item.items() if k != "name"]
        for item in raw_data
    ]
    data = np.array(numeric_data)

    # 2. 클러스터 라벨 추출
    labels = np.array([item["cluster"] for item in clustered_result])

    # 3. 데이터 스케일링 + PCA (2차원으로 축소)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data_scaled)

    # 4. centroids 도 동일하게 변환
    centroids_scaled = scaler.transform(np.array(centroids))
    centroids_2d = pca.transform(centroids_scaled)

    # 5. 시각화
    plt.figure(figsize=(10, 7))
    unique_labels = sorted(set(labels))
    colors = plt.get_cmap("tab10")(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        mask = labels == k
        plt.scatter(
            data_2d[mask, 0], data_2d[mask, 1],
            color=col, edgecolor='k', s=50, label=f'Cluster {k}'
        )

    # 중심점 그리기
    plt.scatter(
        centroids_2d[:, 0], centroids_2d[:, 1],
        marker='*', color='black', s=200, label='Centroids'
    )

    # 중심점에 라벨 번호 붙이기
    for i, (x, y) in enumerate(centroids_2d):
        plt.text(x, y, str(i), fontsize=12, color='white', ha='center', va='center',
                bbox=dict(facecolor='black', boxstyle='circle'))

    plt.title('GroupPT 클러스터링 결과')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



# 1. JSON 파일로 테스트
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'testData/group_pt_members.json')

# 2. 파일 읽고 list로 변환
with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 3. 설정값 수정
groupCount = 20
max_elements_per_cluster = 6
min_elements_per_cluster = 2

# 4. 클러스터링 진행
clustered_result, centroids = constrained_kmeans_with_names(raw_data, groupCount, max_elements_per_cluster, min_elements_per_cluster)

# 5. 시각화
groupingVisualization(raw_data, clustered_result, centroids)