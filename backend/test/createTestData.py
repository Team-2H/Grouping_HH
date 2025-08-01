## 테스트 데이터 생성 로직

import numpy as np
import pandas as pd

# 고정 시드 / 난수 생성 초기값을 42로 고정해서 난수 결과가 항상 같도록 설정
np.random.seed(316)

n_samples = 50
n_groups = 4
samples_per_group = n_samples // n_groups

group_data = []


# 그룹 1: 젊고 마른 초보자
for count in range(samples_per_group):
    age = np.random.randint(18, 25)
    height = round(np.random.uniform(170, 185),1)
    weight = round(np.random.normal(55, 5),1)
    muscle = round(np.random.normal(23, 3),1)
    experience = round(np.random.uniform(0, 1),1)
    group_data.append([age, height, weight, muscle, experience])

# 그룹 2: 고령이고 과체중이며 운동 경력 없음
for count in range(samples_per_group):
    age = np.random.randint(50, 61)
    height = round(np.random.uniform(165, 175),1)
    weight = round(np.random.normal(95, 7),1)
    muscle = round(np.random.normal(28, 3),1)
    experience = round(np.random.uniform(0, 1),1)
    group_data.append([age, height, weight, muscle, experience])

# 그룹 3: 중년이면서 체중은 보통, 근육량 높고 운동 구력 많음
for count in range(samples_per_group):
    age = np.random.randint(45, 55)
    height = round(np.random.uniform(165, 180),1)
    weight = round(np.random.normal(65, 5),1)
    muscle = round(np.random.normal(37, 3),1)
    experience = round(np.random.uniform(10, 20),1)
    group_data.append([age, height, weight, muscle, experience])

# 그룹 4: 젊고 헬스 매니아 (저체지방, 고근육, 운동 구력 높음)
for count in range(samples_per_group):
    age = np.random.randint(20, 30)
    height = round(np.random.uniform(175, 185),1)
    weight = round(np.random.normal(80, 4),1)
    muscle = round(np.random.normal(50, 3),1)
    experience = round(np.random.uniform(5, 15),1)
    group_data.append([age, height, weight, muscle, experience])


np.random.shuffle(group_data)

# DataFrame
df_skewed = pd.DataFrame(group_data, columns=["age","height","weight","muscle_mass","experience"])
df_skewed.index.name = "name"
df_skewed.reset_index(inplace=True)

# 전체 회원 정보를 CSV로 저장
# df_skewed.to_csv(f"group_test_{n_samples}_data.csv", index=False)

# JSON 저장
json_list_filename = f"group_test_{n_samples}_data.json"
df_skewed.to_json(json_list_filename, orient="records", force_ascii=False, indent=2)