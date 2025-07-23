
1. 파일 설명
    groupingVisualization.py    : 시각화 테스트 로직
    consistencyCheck.py         : 정합성 테스트 로직. 점수를 반환하는 함수가 있음
    
    testData/
    group_pt_members.json       : json 형태의 테스트 데이터
    group_pt_members.csv        : csv 형태의 테스트 데이터


2. 시각화 테스트
    (1) 터미널
        cd backend
        python test/groupingVisualization.py
    
    (2) debug
        groupingVisualization.py 파일 켜두고
        실행 및 디버그에서 디버스 실행


3. 정합성 테스트
    (1) 터미널
        cd backend
        python test/consistencyCheck.py
    
    (2) debug
        consistencyCheck.py 파일 켜두고
        실행 및 디버그에서 디버스 실행