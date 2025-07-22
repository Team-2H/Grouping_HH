
import math
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import math
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler


def constrained_kmeans(data, n_clusters=0, max_elements_per_cluster=0, min_elements_per_cluster=0, max_iter=100, tol=1e-4):
    # 1. 데이터 스케일링
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # 2. PCA를 사용하여 2차원으로 차원 축소
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data_scaled)

    # 3. 노이즈가 포함된 클러스터링을 수행 (DBSCAN 사용)
    db = DBSCAN(eps=0.5, min_samples=10).fit(data_2d)
    labels = db.labels_

    n_samples = data.shape[0]
    dim = data.shape[1]

    if n_clusters == 0:
        n_clusters = estimate_n_clusters(n_samples, max_elements_per_cluster, min_elements_per_cluster)

    # 초기 클러스터 중심: 무작위로 선택
    rng = np.random.default_rng()
    centroids = data[rng.choice(n_samples, n_clusters, replace=False)]

    labels = -np.ones(n_samples, dtype=int)
    counts = np.zeros(n_clusters, dtype=int)

    for iteration in range(max_iter):
        old_centroids = centroids.copy()

        # 각 샘플을 가능한 클러스터 중 가장 가까운 곳에 할당
        counts[:] = 0
        labels[:] = -1

        for i in range(n_samples):
            distances = np.linalg.norm(data[i] - centroids, axis=1)
            # 클러스터 크기 제한을 만족하는 클러스터만 선택
            possible_clusters = [k for k in range(n_clusters) if counts[k] < max_elements_per_cluster]

            if not possible_clusters:
                # 모든 클러스터가 꽉 찼으면 가장 가까운 클러스터로 강제 할당
                labels[i] = np.argmin(distances)
                counts[labels[i]] += 1
            else:
                # 가능한 클러스터 중 가장 가까운 곳 선택
                filtered_distances = distances[possible_clusters]
                chosen = possible_clusters[np.argmin(filtered_distances)]
                labels[i] = chosen
                counts[chosen] += 1

        # 클러스터 중심 업데이트
        for k in range(n_clusters):
            members = data[labels == k]
            if len(members) > 0:
                centroids[k] = members.mean(axis=0)

        # 중심점 이동량 계산
        centroid_shift = np.linalg.norm(centroids - old_centroids, axis=1).max()
        if centroid_shift < tol:
            break

    # 최소 크기 클러스터 처리 (예: 너무 작은 클러스터는 가장 가까운 큰 클러스터에 합병)
    small_clusters = [k for k in range(n_clusters) if counts[k] < min_elements_per_cluster]
    for k in small_clusters:
        members = np.where(labels == k)[0]
        for idx in members:
            distances = np.linalg.norm(data[idx] - centroids, axis=1)
            # 최소 크기 이상인 클러스터 중 가장 가까운 클러스터 찾기
            candidates = [c for c in range(n_clusters) if counts[c] >= min_elements_per_cluster and c != k]
            if not candidates:
                # 모든 클러스터가 작거나 자기 자신만 크면 그냥 유지
                continue
            filtered_distances = distances[candidates]
            new_cluster = candidates[np.argmin(filtered_distances)]

            labels[idx] = new_cluster
            counts[new_cluster] += 1
            counts[k] -= 1

        # 중심 업데이트
        if counts[k] == 0:
            centroids[k] = np.zeros(dim)

    return labels, centroids

# 그룹 개수가 들어오지 않은 경우, 최솟값, 최댓값으로 그룹 개수를 정하는 함수
def estimate_n_clusters(n_samples, max_per_group, min_per_group):
    if min_per_group != 0 and max_per_group != 0:
        min_possible = math.ceil(n_samples / max_per_group)
        max_possible = math.floor(n_samples / min_per_group)
        if min_possible > max_possible:
            raise ValueError("min/max 그룹 수 조건이 충돌합니다.")
        return (min_possible + max_possible) // 2

    elif max_per_group != 0:
        return math.ceil(n_samples / max_per_group)

    elif min_per_group != 0:
        return math.floor(n_samples / min_per_group)

    else:
        # 아무 값도 없을 경우엔 sqrt(n) 규칙 사용
        return round(math.sqrt(n_samples))



# 최초 로직
# def constrained_kmeans(data, max_elements_per_cluster, min_elements_per_cluster):
#     # 클러스터 수 결정
#     n_samples = data.shape[0]
#     n_clusters = n_samples // max_elements_per_cluster
#     kmeans = KMeans(n_clusters=n_clusters)
#     kmeans.fit(data)
#     labels = kmeans.labels_
#     unique_labels = set(labels)
#     counts = np.bincount(labels)

#     # 최대값 제한 처리
#     for label in unique_labels:
#         if counts[label] > max_elements_per_cluster:
#             excess_indices = np.where(labels == label)[0]
#             excess_indices = excess_indices[max_elements_per_cluster:]

#             # 가장 가까운 클러스터를 찾아 이동
#             for idx in excess_indices:
#                 distances = np.linalg.norm(data[idx] - kmeans.cluster_centers_, axis=1)
#                 sorted_indices = np.argsort(distances)
#                 for new_label in sorted_indices:
#                     if counts[new_label] < max_elements_per_cluster:
#                         labels[idx] = new_label
#                         counts[label] -= 1
#                         counts[new_label] += 1
#                         break
    
#     # 최소값 제한 처리
#     for label in unique_labels:
#         if counts[label] < min_elements_per_cluster:
#             deficit_indices = np.where(labels == label)[0]
            
#             # 가장 가까운 클러스터로부터 원소를 가져옴
#             for idx in deficit_indices:
#                 distances = np.linalg.norm(data[idx] - kmeans.cluster_centers_, axis=1)
#                 sorted_indices = np.argsort(distances)
#                 for new_label in sorted_indices:
#                     if counts[new_label] > min_elements_per_cluster:
#                         labels[idx] = new_label
#                         counts[label] += 1
#                         counts[new_label] -= 1
#                         if counts[label] >= min_elements_per_cluster:
#                             break
#                 if counts[label] >= min_elements_per_cluster:
#                     break
    
#     return labels