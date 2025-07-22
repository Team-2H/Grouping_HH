
from flask import Blueprint, jsonify, request
import groupingLogic

main = Blueprint('main', __name__)

# Was 동작 테스트
@main.route('/api/hello')
def hello():
    return jsonify(message='Hello from Flask!')

# 메인 화면
@main.route('/')
def mainPage():
    return jsonify(message='Hello from Flask!')

# 그룹핑 요청
@main.route('/grouping', methods=['POST'])
def grouping():
    data = request.get_json()
    groupCount = data.get('groupCount')
    maxFactor = data.get('maxFactor')
    minFactor = data.get('minFactor')
    userData = data.get('userData')

    resultData = groupingLogic.constrained_kmeans(userData, groupCount, maxFactor, minFactor)
    return jsonify(resultData)

