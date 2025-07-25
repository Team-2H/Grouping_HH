
from flask import Blueprint, jsonify, request
from . import groupingLogic
import pandas as pd
import io
from app.validationCheck import ValidationError, ClusteringValidator


main = Blueprint('main', __name__)

# Was 동작 테스트
@main.route('/api/hello')
def hello():
    return jsonify(message='Hello from Flask!')







# 그룹핑 요청
@main.route('/grouping', methods=['POST'])
def grouping():
    try:
        data = request.get_json()
        groupCount = data.get('groupCount')
        maxFactor = data.get('maxFactor')
        minFactor = data.get('minFactor')
        userData = data.get('userData')

        # validation 체크
        validator = ClusteringValidator(userData, groupCount, maxFactor, minFactor)
        validator.validate()

        groupCount = int(groupCount or 0)
        maxFactor = int(maxFactor or 0)
        minFactor = int(minFactor or 0)

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
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), e.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500








# CSV 그룹핑 요청
@main.route('/groupingByCSV', methods=['POST'])
def groupingByCSV():
    try:
        groupCount = request.form.get('groupCount')
        maxFactor = request.form.get('maxFactor')
        minFactor = request.form.get('minFactor')

        # validation 체크
        validator = ClusteringValidator(None, groupCount, maxFactor, minFactor)
        validator.validateCSV(request)

        userData = validator.raw_data
        groupCount = int(groupCount or 0)
        maxFactor = int(maxFactor or 0)
        minFactor = int(minFactor or 0)

        # 클러스터링 로직 연결
        clustered_result, centroids = groupingLogic.constrained_kmeans_with_names(
            userData, groupCount, maxFactor, minFactor
        )

        result = {
            "labels": clustered_result
            # , "centroids": centroids.tolist()
        }

        return jsonify(result)
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), e.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500