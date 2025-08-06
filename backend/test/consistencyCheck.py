
import json
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.groupingLogic import clustering


def consisCheckWithModule(data, labels):
    sScore = silhouette_score(data, labels)
    dScore = davies_bouldin_score(data, labels)
    cScore = calinski_harabasz_score(data, labels)

    return sScore, dScore, cScore





# 1. JSON 파일로 테스트
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'testData/json/group_test_100_data.json')

# 2. 파일 읽고 list로 변환
with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 3. 설정값 수정
groupCount = 20
max_elements_per_cluster = 6
min_elements_per_cluster = 2

# 4. 클러스터링 진행
names, labels, n_samples, centroids = clustering(raw_data, groupCount, max_elements_per_cluster, min_elements_per_cluster)


numeric_data = [
    [v for k, v in item.items() if k != "name"]
    for item in raw_data
]
num_data = np.array(numeric_data)

scaler = StandardScaler()
data_scaled = scaler.fit_transform(num_data)

# 5. 정합성
sScore, dScore, cScore = consisCheckWithModule(num_data, labels)
print("sScore : ", sScore)
print("dScore : ", dScore)
print("cScore : ", cScore)