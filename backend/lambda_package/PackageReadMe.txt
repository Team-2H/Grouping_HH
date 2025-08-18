## 사전에 AWS 계정정보를 설정값으로 등록해야 함
export AWS_ACCESS_KEY_ID={AWS 계정 엑세스 키}
export AWS_SECRET_ACCESS_KEY={AWS 계정 엑세스 키의 시크릿 키}
export AWS_DEFAULT_REGION=ap-northeast-2

# AWS ECR 로그인
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 475698774641.dkr.ecr.ap-northeast-2.amazonaws.com


## 패키징
# 소스 취합해서 docker 이미지 생성까지 진행
python build_lambda.py

# 로컬 docker에 이미지 갱신
docker tag groupingproject:latest 475698774641.dkr.ecr.ap-northeast-2.amazonaws.com/project/grouping:latest

# AWS ECR에 해당 이미지 업로드
docker push 475698774641.dkr.ecr.ap-northeast-2.amazonaws.com/project/grouping:latest