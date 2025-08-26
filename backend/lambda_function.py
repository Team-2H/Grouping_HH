import json
from app import groupingLogic
from app.validationCheck import ValidationError, ClusteringValidator
from requests_toolbelt.multipart.decoder import MultipartDecoder
import base64
import io



def lambda_handler(event, context):
    # API Gateway에서 오는 이벤트 파싱
    # 이 방식은 AWS HTTP Api 방식
    # requestContext = event['requestContext']
    # http = requestContext['http']
    # http_method = http['method']
    # path = http['path']

    # 이 방식은 AWS Rest API 방식
    http_method = event['httpMethod']
    path = event['path']
    
    if path == '/grouping' and http_method == 'POST':
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
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }
        
        except ValidationError as e:
            print('ValidationError!')
            print(f'e.status_code : {e.status_code}')
            print(f'e.messages : {e.messages}')
            return {
                'statusCode': e.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'errors': e.messages})
            }
        except Exception as e:
            print('Exception!')
            print(f'e.messages : {str(e)}')
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': str(e)})
            }


    elif path == '/groupingByCSV' and http_method == 'POST':
        try:
            # Content-Type 확인
            headers = event.get('headers', {})
            content_type = headers.get('content-type', '')
            if 'multipart/form-data' not in content_type:
                raise ValidationError({'error': "multipart/form-data로 전송되어야 합니다"})
            
            body = event.get('body', '')
            if event.get('isBase64Encoded', False):
                body = base64.b64decode(body)
            else:
                body = body.encode("utf-8")

            # 파일 데이터 추출
            parser = MultipartDecoder(body, content_type)

            settingData = {}
            csvDataFile = None
            csvDataFileName = None

            for part in parser.parts:
                # 각 part의 헤더 확인
                partHeaders = part.headers
                disposition = partHeaders[b'Content-Disposition'].decode()  # type: ignore
                
                # Content-Disposition에서 name, filename 추출
                name = None
                filename = None
                if 'name=' in disposition:
                    # name="field_name" 추출
                    name = disposition.split('name="')[1].split('"')[0]
                if 'filename=' in disposition:
                    # filename="file_name" 추출
                    filename = disposition.split('filename="')[1].split('"')[0]
                
                if filename:  # 파일이면
                    csvDataFile = io.BytesIO(part.content)
                    csvDataFileName = filename
                else:  # 일반 필드이면
                    settingData[name] = part.content.decode() # 텍스트로 디코딩
            
            if csvDataFileName:
                if not str(csvDataFileName).lower().endswith(".csv"):
                    raise ValidationError({'error': 'CSV 파일이 아닙니다'})
            else:
                raise ValidationError({'error': '파일 이름이 없습니다'})

            groupCount = int(settingData['groupCount']  if 'groupCount' in settingData else 0)
            maxFactor  = int(settingData['maxFactor']   if 'maxFactor'  in settingData else 0)
            minFactor  = int(settingData['minFactor']   if 'minFactor'  in settingData else 0)

            # validation 체크
            validator = ClusteringValidator(None, groupCount, maxFactor, minFactor)
            validator.validateCSV(csvDataFile)

            userData = validator.raw_data
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
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }
        
        except ValidationError as e:
            print('ValidationError!')
            print(f'e.status_code : {e.status_code}')
            print(f'e.messages : {e.messages}')
            return {
                'statusCode': e.status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'errors': e.messages})
            }
        except Exception as e:
            print('Exception!')
            print(f'e.messages : {str(e)}')
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': str(e)})
            }
    
    return {
        'statusCode': 404,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Not found'})
    }
