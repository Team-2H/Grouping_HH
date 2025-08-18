import json
from app import groupingLogic
from app.validationCheck import ValidationError, ClusteringValidator
from multipart import MultipartParser
import base64
import tempfile


def lambda_handler(event, context):
    # API Gateway에서 오는 이벤트 파싱
    # 이 방식은 AWS HTTP Api 방식
    requestContext = event['requestContext']
    http = requestContext['http']
    http_method = http['method']
    path = http['path']

    # 이 방식은 AWS Rest API 방식
    # http_method = event['httpMethod']
    # path = event['path']
    
    if path == '/prod/grouping' and http_method == 'POST':
        try:
            body = event.get('body', '{}')

            data = json.loads(body) if body else {}

            if len(data) == 0:
                raise ValidationError({'error': "데이터가 들어오지 않았습니다"})

            userData = data.get('userData')
            groupCount = data.get('groupCount')
            maxFactor = data.get('maxFactor')
            minFactor = data.get('minFactor')
            factorWeight = data.get('factorWeight')

            # validation 체크
            validator = ClusteringValidator(userData, groupCount, maxFactor, minFactor, factorWeight)
            validator.validateJSON()

            groupCount = int(groupCount or 0)
            maxFactor = int(maxFactor or 0)
            minFactor = int(minFactor or 0)
            factorWeight = validator.factorWeight

            clustered_result, centroids = groupingLogic.constrained_kmeans_with_names(
                userData, groupCount, maxFactor, minFactor, factorWeight
            )

            # labels : 각 이름의 요소가 어떤 그룹에 속하는지 적혀있는 List
                # ex) {"cluster": 7,"name": "회원1"},{"cluster": 14,"name": "회원2"},,,
            # centroids : 각 그룹의 중심점. 6차원 데이터가 들어오면 그룹당 6개 데이터들의 중심값을 담고있는 List
                # ex) [29.0, 170.0, 69.5, 41.02, 6.55, 0.5], [62.66, 164.16, 91.66, 22.51, 0.46, 0.83],,,,
            result = {
                "labels": clustered_result
                # , "centroids": centroids.tolist()
            }

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(result)
            }
        
        except ValidationError as e:
            print('ValidationError!')
            print(f'e.status_code : {e.status_code}')
            print(f'e.messages : {e.messages}')
            return {
                'statusCode': e.status_code,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'errors': e.messages})
            }
        except Exception as e:
            print('Exception!')
            print(f'e.messages : {str(e)}')
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }


    elif path == '/prod/groupingByCSV' and http_method == 'POST':
        try:
            # Content-Type 확인
            headers = event.get('headers', {})
            content_type = headers.get('Content-Type', '')
            if 'multipart/form-data' not in content_type:
                raise ValidationError({'error': "multipart/form-data로 전송되어야 합니다"})
            
            body = event.get('body', '')
            if event.get('isBase64Encoded', False):
                body = base64.b64decode(body)
            
            # 파일 데이터 추출 (간단한 예시)
            boundary = content_type.split('boundary=')[1]
            parser = MultipartParser(body, boundary)
            parts = parser.parts  # type: ignore

            settingData = {}
            csvDataFile = None

            for part in parts:
                name = part.headers[b"Content-Disposition"].decode()
                name_val = name.split("name=")[-1].split(";")[0].strip('"')

                if name_val in ("groupCount", "maxFactor", "minFactor"):
                    # 설정값 받아옴
                    settingData[name_val] = part.content.decode()
                elif name_val == "csvData":
                    # 파일 받아옴
                    if part.filename:  # 파일
                        if part.filename == '':
                            raise ValidationError({'error': '파일 이름이 없습니다'})
                        if not str(part.filename).lower().endswith(".csv"):
                            raise ValidationError({'error': 'CSV 파일이 아닙니다'})

                        # --- 파일 처리: 가능한 스트림을 재사용, 없다면 스풀(메모리->디스크)로 만들기 ---
                        fileobj = None

                        # 1) part가 이미 file-like 객체 제공하는 경우 (일부 파서가 제공)
                        if hasattr(part, "file") and getattr(part, "file") is not None:
                            fileobj = part.file.stream
                            fileobj.seek(0)
                        elif hasattr(part, "stream") and getattr(part, "stream") is not None:
                            fileobj = part.stream
                            fileobj.seek(0)

                        # 2) 파서가 .content (bytes)만 제공하면 BytesIO 또는 SpooledTemporaryFile 사용
                        else:
                            # 메모리에 모두 올려도 괜찮은 작은 파일이면 BytesIO가 간편
                            # 대용량을 대비하려면 SpooledTemporaryFile을 사용 (threshold 지나면 디스크로 스풀됨)
                            spooled = tempfile.SpooledTemporaryFile(max_size=10 * 1024 * 1024)  # 10MB 임계값
                            # part.content 는 bytes 라고 가정
                            spooled.write(part.content)
                            spooled.seek(0)
                            fileobj = spooled

                        # 이제 fileobj는 읽을 수 있는 바이너리 파일 객체
                        csvDataFile = fileobj
                    else:
                        raise ValidationError({'error': "파일이 들어오지 않았습니다"})
                else:
                    raise ValidationError({'error': f"허용하지 않는 변수명 입니다. 변수명 : {name_val}"})


            groupCount = settingData['groupCount']
            maxFactor = settingData['maxFactor']
            minFactor = settingData['minFactor']

            # validation 체크
            validator = ClusteringValidator(None, groupCount, maxFactor, minFactor)
            validator.validateCSV(csvDataFile)

            userData = validator.raw_data
            groupCount = int(groupCount or 0)
            maxFactor = int(maxFactor or 0)
            minFactor = int(minFactor or 0)
            factorWeight = validator.factorWeight

            # 클러스터링 로직 연결
            clustered_result, centroids = groupingLogic.constrained_kmeans_with_names(
                userData, groupCount, maxFactor, minFactor, factorWeight
            )

            result = {
                "labels": clustered_result
                # , "centroids": centroids.tolist()
            }
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(result)
            }
        
        except ValidationError as e:
            print('ValidationError!')
            print(f'e.status_code : {e.status_code}')
            print(f'e.messages : {e.messages}')
            return {
                'statusCode': e.status_code,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'errors': e.messages})
            }
        except Exception as e:
            print('Exception!')
            print(f'e.messages : {str(e)}')
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
    
    return {
        'statusCode': 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Not found'})
    }
