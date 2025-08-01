


# grouping Param
test_param_json = [
    # 1. 설정값 검증
    # 설정값이 문자로 들어오는 경우
    ("a","b","c","group_test_10_data.json",[],400),
    # 설정값이 0 혹은 음수로 들어오는 경우
    (0,-1,0,"group_test_10_data.json",[],400),
    # 지정 그룹 수가 1로 들어오는 경우
    (1,5,2,"group_test_10_data.json",[],400),
    # 그룹당 최대 인원수 값이 1로 들어오는 경우
    (10,1,1,"group_test_10_data.json",[],400),
    # 그룹당 최소 인원 수가 그룹당 최대 인원 수보다 큰 값일 경우
    (3,2,3,"group_test_10_data.json",[],400),
    # 지정 그룹 수가 데이터 행의 개수보다 큰 값일 경우
    (11,2,1,"group_test_10_data.json",[],400),
    # 지정 그룹 수와 그룹당 최소 인원 수의 곱이 데이터 행의 개수보다 클 경우
    (4,4,3,"group_test_10_data.json",[],400),
    # 지정 그룹 수와 그룹당 최대 인원 수의 곱이 데이터 행의 개수보다 작을 경우
    (3,3,2,"group_test_10_data.json",[],400),

    # 2. 데이터 - 마지막 빼고 전부 실패
    # 데이터 행의 개수가 1개 이하로 들어온 경우
    (3,3,1,"group_test_0_data.json",[],400),
    (3,3,1,"group_test_1_data.json",[],400),
    # 데이터에 빈 칸(값이 없는 칸)이 있는 경우
    (2,2,1,"group_test_empty_data.json",[],400),
    # name 컬럼이 없는 경우
    (3,2,1,"group_test_no_column.json",[],400),
    # name 컬럼 데이터가 겹치는 경우
    (3,3,2,"group_test_same_name.json",[],400),
    # 숫자가 아닌 값이 데이터로 들어있는 경우(name은 가능)
    (3,2,1,"group_test_text_in_data.json",[],400),
    # 컬럼 열의 개수와 데이터 열의 개수가 맞지 않는 경우 <- 이건 json에서 테스트가 안됨. 이럴 수가 없음
    # (3,2,1,"group_test_more_than_column.json",[],400),
    # 컬럼 이름이 일부 없는 경우
    (3,2,1,"group_test_empty_column.json",[],200),
    # 컬럼 이름이 겹치는 경우 - 성공
    (3,2,1,"group_test_same_column.json",[],200),

    # 4. JSON
    # 몇몇 데이터 row의 컬럼명이 다른 경우
    (3,2,1,"group_test_different_column_name.json",[],400),
    # 몇몇 데이터 row의 데이터 개수가 다른 경우
    (3,2,1,"group_test_different_column_num.json",[],400),
    # 몇몇 데이터 row의 데이터 순서가 다른 경우
    (3,2,1,"group_test_different_column_which.json",[],200),

    # 5. 가중치
    # 가중치 데이터 개수가 컬럼 개수와 다를 경우
    (3,2,1,"group_test_5_data.json",[1,1,1,1,1],400),
    # 가중치 데이터가 숫자가 아닐 경우
    (3,2,1,"group_test_5_data.json",["a","1","c","1","1","1"],400),
    # 가중치 데이터 값이 허용된 범위가 아닌 경우
    (3,2,1,"group_test_5_data.json",[7,0.4,0.1,-1,0,1],400),
    # 가중치 데이터가 정상적으로 들어온 경우
    (3,2,1,"group_test_5_data.json",[2.1,0.5,1.6,0.8,1,1.3],200),

    # 6. 정상 설정값
    # [지정 그룹 수] 값만 들어온 경우
    (4,'','',"group_test_10_data.json",[],200),
    # [그룹 내 최대 인자 수] 값만 들어온 경우
    ('',3,'',"group_test_10_data.json",[],200),
    # [그룹 내 최소 인자 수] 값만 들어온 경우
    ('','',2,"group_test_10_data.json",[],200),
    # [지정 그룹 수], [그룹당 최대 인원 수] 값만 들어온 경우
    (4,3,'',"group_test_10_data.json",[],200),
    # [지정 그룹 수], [그룹당 최소 인원 수] 값만 들어온 경우
    (4,'',2,"group_test_10_data.json",[],200),
    # [그룹당 최대 인원 수], [그룹당 최소 인원 수] 값만 들어온 경우
    ('',3,2,"group_test_10_data.json",[],200),
    # 세 설정값 전부 들어오는 경우
    (4,3,2,"group_test_10_data.json",[],200),
    # 세 설정값 전부 안 들어오는 경우
    ('','','',"group_test_10_data.json",[],200),

    # 6. 규모별 테스트
    # 데이터 5~10개
    (4,3,2,"group_test_10_data.json",[],200),
    # 데이터 10~50개
    (8,10,5,"group_test_50_data.json",[],200),
    # 데이터 100개
    (30,5,3,"group_test_100_data.json",[],200),
    # 데이터 250개
    (50,8,4,"group_test_250_data.json",[],200),
    # 데이터 500개
    (100,10,4,"group_test_500_data.json",[],200),
]







# groupingByCSV Param
test_param_csv = [
    # 1. 설정값 검증
    # 설정값이 문자로 들어오는 경우
    ("a","b","c","group_test_10_data.csv",400),
    # 설정값이 0 혹은 음수로 들어오는 경우
    (0,-1,0,"group_test_10_data.csv",400),
    # 지정 그룹 수가 1로 들어오는 경우
    (1,5,2,"group_test_10_data.csv",400),
    # 그룹당 최대 인원수 값이 1로 들어오는 경우
    (10,1,1,"group_test_10_data.csv",400),
    # 그룹당 최소 인원 수가 그룹당 최대 인원 수보다 큰 값일 경우
    (3,2,3,"group_test_10_data.csv",400),
    # 지정 그룹 수가 데이터 행의 개수보다 큰 값일 경우
    (11,2,1,"group_test_10_data.csv",400),
    # 지정 그룹 수와 그룹당 최소 인원 수의 곱이 데이터 행의 개수보다 클 경우
    (4,4,3,"group_test_10_data.csv",400),
    # 지정 그룹 수와 그룹당 최대 인원 수의 곱이 데이터 행의 개수보다 작을 경우
    (3,3,2,"group_test_10_data.csv",400),

    # 2. 데이터 - 마지막 빼고 전부 실패
    # 데이터 행의 개수가 1개 이하로 들어온 경우
    (3,3,1,"group_test_0_data.csv",400),
    (3,3,1,"group_test_1_data.csv",400),
    # 데이터에 빈 칸(값이 없는 칸)이 있는 경우
    (2,2,1,"group_test_empty_data.csv",400),
    # name 컬럼이 없는 경우
    (3,2,1,"group_test_no_column.csv",400),
    # name 컬럼 데이터가 겹치는 경우
    (3,3,2,"group_test_same_name.csv",400),
    # 숫자가 아닌 값이 데이터로 들어있는 경우(name은 가능)
    (3,2,1,"group_test_text_in_data.csv",400),
    # 컬럼 열의 개수와 데이터 열의 개수가 맞지 않는 경우
    (3,2,1,"group_test_more_than_column.csv",400),
    # 컬럼 이름이 일부 없는 경우
    (3,2,1,"group_test_empty_column.csv",200),
    # 컬럼 이름이 겹치는 경우 - 성공
    (3,2,1,"group_test_same_column.csv",200),

    # 3. CSV
    # 파일 형식이 csv가 아닌 경우
    (25,6,2,"group_test_no_csv.text",400),
    # 파일 크기가 0인 경우
    (3,2,1,"group_test_no_data.csv",400),

    # 5. 가중치
    # 가중치 데이터 개수가 컬럼 개수와 다를 경우
    (4,3,2,"group_test_different_weight_num.csv",400),
    # 가중치 데이터가 숫자가 아닐 경우
    (4,3,2,"group_test_text_in_weight.csv",400),
    # 가중치 데이터 값이 허용된 범위가 아닌 경우
    (4,3,2,"group_test_weight_under_over_flow.csv",400),
    # 가중치 데이터가 정상적으로 들어온 경우
    (4,3,2,"group_test_10_data_with_weight.csv",200),

    # 6. 정상 설정값
    # [지정 그룹 수] 값만 들어온 경우
    (4,'','',"group_test_10_data.csv",200),
    # [그룹 내 최대 인자 수] 값만 들어온 경우
    ('',3,'',"group_test_10_data.csv",200),
    # [그룹 내 최소 인자 수] 값만 들어온 경우
    ('','',2,"group_test_10_data.csv",200),
    # [지정 그룹 수], [그룹당 최대 인원 수] 값만 들어온 경우
    (4,3,'',"group_test_10_data.csv",200),
    # [지정 그룹 수], [그룹당 최소 인원 수] 값만 들어온 경우
    (4,'',2,"group_test_10_data.csv",200),
    # [그룹당 최대 인원 수], [그룹당 최소 인원 수] 값만 들어온 경우
    ('',3,2,"group_test_10_data.csv",200),
    # 세 설정값 전부 들어오는 경우
    (4,3,2,"group_test_10_data.csv",200),
    # 세 설정값 전부 안 들어오는 경우
    ('','','',"group_test_10_data.csv",200),

    # 7. 규모별 테스트
    # 데이터 5~10개
    (4,3,2,"group_test_10_data.csv",200),
    # 데이터 10~50개
    (8,10,5,"group_test_50_data.csv",200),
    # 데이터 100개
    (30,5,3,"group_test_100_data.csv",200),
    # 데이터 250개
    (50,8,4,"group_test_250_data.csv",200),
    # 데이터 500개
    (100,10,4,"group_test_500_data.csv",200),
]

# CSV Header Check
test_param_csv_header = [
    # HTTP 요청이 multipart/form-data가 아닌 경우
    (4,3,2,"group_test_10_data.json",400),
]