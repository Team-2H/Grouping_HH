
import json
import os
import pytest
import requests
from pytest_param import test_param_json, test_param_csv, test_param_csv_header

BASE_URL = "http://127.0.0.1:5000"  # 또는 실제 서버 주소
TEST_CSV_DIR = "testData"






# 데이터가 JSON으로 넘어오는 경우 테스트
@pytest.mark.parametrize("groupCount,maxFactor,minFactor,testFile,factorWeight,expected_code",
                         test_param_json)
def test_grouping(groupCount,maxFactor,minFactor,testFile,factorWeight,expected_code):
    filepath = os.path.join(TEST_CSV_DIR+"/json", testFile)
    with open(filepath, "r", encoding="utf-8") as f:
        userData = json.load(f)
    
    data = {
        "groupCount": groupCount,
        "maxFactor": maxFactor,
        "minFactor": minFactor,
        "userData": userData,
        "factorWeight": factorWeight
    }

    # 요청 헤더 설정
    headers = {
                "Content-Type": "application/json"
    }

    # API로 POST 요청 보내기
    response = requests.post(BASE_URL + "/grouping", json=data, headers=headers)
    assert response.status_code == expected_code

    if expected_code >= 400:
        resultJson = response.json()
        assert "errors" in resultJson
        # print("resultJson['errors'] : " + str(resultJson["errors"]))
        # 각 테스트 케이스마다 나오는 에러 메세지도 검사를 해야하지 않을까 싶어서 일단 넣어둠
        # assert resultJson["error"] == ""





# 데이터가 CSV로 넘어오는 경우 테스트
@pytest.mark.parametrize("groupCount,maxFactor,minFactor,testFile,expected_code",
                         test_param_csv)
def test_groupingByCSV(groupCount,maxFactor,minFactor,testFile,expected_code):
    filepath = os.path.join(TEST_CSV_DIR+"/csv", testFile)
    with open(filepath, "rb") as f:
        # 파일
        files = {"csvData": (testFile, f, "text/csv")}

        # 매개변수
        data = {
            "groupCount": groupCount,
            "maxFactor": maxFactor,
            "minFactor": minFactor
        }
                
        # 전송
        response = requests.post(BASE_URL + "/groupingByCSV", files=files, data=data)
        assert response.status_code == expected_code

    if expected_code >= 400:
        resultJson = response.json()
        assert "errors" in resultJson
        # 각 테스트 케이스마다 나오는 에러 메세지도 검사를 해야하지 않을까 싶어서 일단 넣어둠
        # assert resultJson["error"] == ""





@pytest.mark.parametrize("groupCount,maxFactor,minFactor,testFile,expected_code", test_param_csv_header)
def test_groupingByCSV_check_header(groupCount,maxFactor,minFactor,testFile,expected_code):
    filepath = os.path.join(TEST_CSV_DIR+"/json", testFile)
    with open(filepath, "r", encoding="utf-8") as f:
        userData = json.load(f)
            
    data = {
        "groupCount": groupCount,
        "maxFactor": maxFactor,
        "minFactor": minFactor,
        "userData": userData
    }

    # 요청 헤더 설정
    headers = {
                "Content-Type": "application/json"
    }

    # API로 POST 요청 보내기
    response = requests.post(BASE_URL + "/groupingByCSV", json=data, headers=headers)
    assert response.status_code == expected_code