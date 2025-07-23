
from flask import Blueprint, jsonify, request
from . import groupingLogic
import pandas as pd
import io


main = Blueprint('main', __name__)

# Was 동작 테스트
@main.route('/api/hello')
def hello():
    return jsonify(message='Hello from Flask!')







# 그룹핑 요청
@main.route('/grouping', methods=['POST'])
def grouping():
    data = request.get_json()
    groupCount = data.get('groupCount')
    maxFactor = data.get('maxFactor')
    minFactor = data.get('minFactor')
    userData = data.get('userData')

    clustered_result, centroids = groupingLogic.constrained_kmeans_with_names(userData, groupCount, maxFactor, minFactor)

    # labels : 각 이름의 요소가 어떤 그룹에 속하는지 적혀있는 List
        # ex) {"cluster": 7,"name": "회원1"},{"cluster": 14,"name": "회원2"},,,
    # centroids : 각 그룹의 중심점. 6차원 데이터가 들어오면 그룹당 6개 데이터들의 중심값을 담고있는 List
        # ex) [29.0, 170.0, 69.5, 41.02, 6.55, 0.5], [62.66, 164.16, 91.66, 22.51, 0.46, 0.83],,,,
    result = {
        "labels": clustered_result
        # , "centroids": centroids.tolist()
    }

    return jsonify(result)





# CSV 그룹핑 요청
@main.route('/groupingByCSV', methods=['POST'])
def groupingByCSV():
    file = request.files.get('csvData')
    if file == None:
        return jsonify({'error': '파일이 전송되지 않았습니다.'}), 400

    if file.filename == '':
        return jsonify({'error': '파일 이름이 없습니다.'}), 400

    try:
        # FileStorage는 바이너리 스트림이라 디코딩 필요
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        df = pd.read_csv(stream)

        # 필요한 후처리 수행 (예: dict 변환)
        data = df.to_dict(orient='records')

        groupCount = int(request.form.get('groupCount') or 0)
        maxFactor = int(request.form.get('maxFactor') or 0)
        minFactor = int(request.form.get('minFactor') or 0)

        # 클러스터링 로직 연결
        clustered_result, centroids = groupingLogic.constrained_kmeans_with_names(
            data, groupCount, maxFactor, minFactor
        )

        result = {
            "labels": clustered_result
            # , "centroids": centroids.tolist()
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'파일 처리 중 오류 발생: {str(e)}'}), 500