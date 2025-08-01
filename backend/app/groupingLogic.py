
import math
import numpy as np
from sklearn.preprocessing import StandardScaler
import math
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd


def constrained_kmeans_with_names(
    raw_data,
    n_clusters=0,
    max_elements_per_cluster=0,
    min_elements_per_cluster=0,
    weightFactor=[],
    max_iter=100,
    tol=1e-4
):
    
    names, labels, n_samples, centroids = clustering(
        raw_data, n_clusters, max_elements_per_cluster,
        min_elements_per_cluster, weightFactor, max_iter, tol
    )

    # 최종 결과: 이름과 클러스터 번호 매핑
    clustered_result = [{"name": names[i], "cluster": int(labels[i])} for i in range(n_samples)]

    return clustered_result, centroids








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










# 테스트에서 클러스터링 기능만 사용하기 위해 함수 따로 빼둠
def clustering(
    raw_data,
    n_clusters=0,
    max_elements_per_cluster=0,
    min_elements_per_cluster=0,
    weightFactor=[],
    max_iter=100,
    tol=1e-4
):
    # 1. 데이터에서 이름 분리
    names = [item["name"] for item in raw_data]

    # 2. 데이터 추출 (name,weightFactor 제외)
    reference_keys = set(raw_data[0].keys()) - {"name"}
    numeric_data = [
        [item[key] for key in reference_keys]
        for item in raw_data
    ]

    data = np.array(numeric_data)
    n_samples, dim = data.shape

    # 3. 데이터 스케일링
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # 가중치 데이터가 리스트로 들어오는 경우
    # 가중치 데이터 적용
    if len(weightFactor) > 0:
        weightFactor = np.array(weightFactor, dtype=np.float64)
        data_scaled = data_scaled * weightFactor
    
    # 가중치 데이터가 key,value로 들어오는 경우
    # 아직 미구현

    # 4. PCA를 사용하여 20차원으로 차원 축소
    pca = PCA( n_components=min( 20, data_scaled.shape[0], data_scaled.shape[1]))
    data_2d = pca.fit_transform(data_scaled)

    # 5. 노이즈 제거용 DBSCAN (필수는 아님)
    db = DBSCAN(eps=0.5, min_samples=10).fit(data_2d)
    labels_db = db.labels_

    # 6. 지정 그룹 수 없을 시, 최대최소값으로 추정
    if n_clusters == 0:
        n_clusters = estimate_n_clusters(n_samples, max_elements_per_cluster, min_elements_per_cluster)

    # 7. 클러스터링 진행
    # 7.1. 초기 중심 무작위 선택
    rng = np.random.default_rng()
    centroids = data[rng.choice(n_samples, n_clusters, replace=False)]

    labels = -np.ones(n_samples, dtype=int)
    counts = np.zeros(n_clusters, dtype=int)

    for iteration in range(max_iter):
        old_centroids = centroids.copy()
        labels[:] = -1
        counts[:] = 0

        for i in range(n_samples):
            distances = np.linalg.norm(data[i] - centroids, axis=1)
            possible_clusters = [k for k in range(n_clusters) if counts[k] < max_elements_per_cluster]

            if not possible_clusters:
                labels[i] = np.argmin(distances)
                counts[labels[i]] += 1
            else:
                filtered_distances = distances[possible_clusters]
                chosen = possible_clusters[np.argmin(filtered_distances)]
                labels[i] = chosen
                counts[chosen] += 1

        for k in range(n_clusters):
            members = data[labels == k]
            if len(members) > 0:
                centroids[k] = members.mean(axis=0)

        centroid_shift = np.linalg.norm(centroids - old_centroids, axis=1).max()
        if centroid_shift < tol:
            break

    # 최소 인원 미만 클러스터 병합
    small_clusters = [k for k in range(n_clusters) if counts[k] < min_elements_per_cluster]
    for k in small_clusters:
        members = np.where(labels == k)[0]
        for idx in members:
            distances = np.linalg.norm(data[idx] - centroids, axis=1)
            candidates = [c for c in range(n_clusters) if counts[c] >= min_elements_per_cluster and c != k]
            if not candidates:
                continue
            filtered_distances = distances[candidates]
            new_cluster = candidates[np.argmin(filtered_distances)]
            labels[idx] = new_cluster
            counts[new_cluster] += 1
            counts[k] -= 1

        if counts[k] == 0:
            centroids[k] = np.zeros(dim)
    
    return names, labels, n_samples, centroids



