# 고정 시드
import numpy as np
import pandas as pd

np.random.seed(42)

n_samples = 100
n_groups = 4
samples_per_group = n_samples // n_groups

group_data = []
group_labels = []

# 그룹 1: 젊고 마른 초보자
for _ in range(samples_per_group):
    age = np.random.randint(18, 25)
    weight = np.random.normal(55, 5)
    muscle = np.random.normal(23, 3)
    experience = np.random.uniform(0, 1)
    group_data.append([age, weight, muscle, experience])
    group_labels.append("초보 마름")

# 그룹 2: 고령이고 과체중이며 운동 경력 없음
for _ in range(samples_per_group):
    age = np.random.randint(50, 61)
    weight = np.random.normal(95, 7)
    muscle = np.random.normal(28, 3)
    experience = np.random.uniform(0, 1)
    group_data.append([age, weight, muscle, experience])
    group_labels.append("비운동 고령")

# 그룹 3: 중년이면서 체중은 보통, 근육량 높고 운동 구력 많음
for _ in range(samples_per_group):
    age = np.random.randint(45, 55)
    weight = np.random.normal(65, 5)
    muscle = np.random.normal(37, 3)
    experience = np.random.uniform(10, 20)
    group_data.append([age, weight, muscle, experience])
    group_labels.append("운동 중년")

# 그룹 4: 젊고 헬스 매니아 (저체지방, 고근육, 운동 구력 높음)
for _ in range(samples_per_group):
    age = np.random.randint(20, 30)
    weight = np.random.normal(80, 4)
    muscle = np.random.normal(50, 3)
    experience = np.random.uniform(5, 15)
    group_data.append([age, weight, muscle, experience])
    group_labels.append("헬스 매니아")

# 셔플
combined = list(zip(group_data, group_labels))
np.random.shuffle(combined)
group_data, group_labels = zip(*combined)

# DataFrame
df_skewed = pd.DataFrame(group_data, columns=["나이", "몸무게(kg)", "근육량(kg)", "운동구력(년)"])
df_skewed["그룹"] = group_labels
df_skewed.index.name = "회원ID"
df_skewed.reset_index(inplace=True)

# numpy 배열 (클러스터링 용)
skewed_numeric_data = df_skewed[["나이", "몸무게(kg)", "근육량(kg)", "운동구력(년)"]].to_numpy()

# 데이터를 numpy 배열로 저장
np.save("skewed_fitness_data.npy", skewed_numeric_data)

# 전체 회원 정보를 CSV로 저장
# df_skewed.to_csv("skewed_fitness_members.csv", index=False)