
import pandas as pd
import io
from collections import defaultdict
from io import StringIO
from typing import cast

class ValidationError(Exception):
    def __init__(self, messages, status_code=400):
        self.messages = messages  # List of strings
        self.status_code = status_code
        super().__init__("Validation failed")



class ClusteringValidator:
    def __init__(self, raw_data, n_clusters, max_per, min_per, factorWeight=[]):
        self.raw_data = raw_data
        self.n_clusters = n_clusters
        self.max_per = max_per
        self.min_per = min_per
        self.factorWeight = factorWeight
        self.errors = []


    # 기본 validation 체크
    def validate(self, moduleType):
        self._check_configuration()
        self._check_data()
        self._check_constraints()
        self._check_factorWeight(moduleType)

        
    

    # CSV validation 체크
    def validateCSV(self, request):
        self._check_CSV(request)
        self.validate("CSV")
        if self.errors:
            raise ValidationError(self.errors)
    

    # JSON validation 체크
    def validateJSON(self):
        self.validate("JSON")
        self._check_JSON()
        if self.errors:
            raise ValidationError(self.errors)

        


    # 설정값 체크
    def _check_configuration(self):
        numExceptCount = 0

        for attr, name in [
            ("n_clusters", "지정 그룹 수"),
            ("max_per", "그룹당 최대 인원수"),
            ("min_per", "그룹당 최소 인원수")
        ]:
            val = getattr(self, attr)

            # 값이 없으면 넘어감 (선택 입력 처리)
            if val in (None, ""):
                continue

            try:
                val = int(val)
                if val <= 0:
                    self.errors.append(f"{name}은 1 이상이어야 합니다")
                setattr(self, attr, val)  # 변환된 int 값을 다시 설정
            except ValueError:
                self.errors.append(f"{name}은 숫자로 들어와야 합니다")
                numExceptCount += 1

        # 숫자 변환 실패했다면 이후 처리 중단
        if numExceptCount > 0:
            raise ValidationError(self.errors)

        # 유효한 값이 있을 때만 세부 비교
        if self.max_per not in (None, ""):
            if self.max_per == 1:
                self.errors.append("그룹당 최대 인원수는 2 이상이어야 합니다")
            
            if self.min_per not in (None, ""):
                if self.min_per > self.max_per:
                    self.errors.append("그룹당 최소 인원수가 최대 인원수보다 큽니다")


    def _check_data(self):
        if not isinstance(self.raw_data, list) or len(self.raw_data) <= 1:
            self.errors.append("데이터는 2개 이상 입력해야 합니다")

        name_indices = defaultdict(list)

        for idx, entry in enumerate(self.raw_data, start=1):  # 1부터 시작하는 행 번호
            if "name" not in entry:
                self.errors.append("데이터에 name 열이 없습니다. 열을 확인해주세요.")
                break
            
            # 중복 확인을 위해 name 정보 따로 빼두기
            name = entry["name"]
            name_indices[name].append(idx)

            for key, value in entry.items():
                if value in ("", None) or pd.isna(value):
                    self.errors.append(f"{name or '알 수 없음'} 의 {key} 값이 없습니다")
                elif key != "name":
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        self.errors.append("name 이 아닌 열에는 숫자만 기입 가능합니다")

        # 중복 name + 행 정보 포함
        duplicates = {name: rows for name, rows in name_indices.items() if len(rows) > 1}
        if duplicates:
            dup_msg = " ".join([
                f"'{name}'- [{', '.join([f'{i}행' for i in indices])}]"
                for name, indices in duplicates.items()
            ])
            self.errors.append(f"다음 name 값이 중복되어 있습니다:{dup_msg}")


    # 세부조건 체크
    def _check_constraints(self):

        if self.n_clusters not in (None, ""):
            if self.n_clusters == 1:
                self.errors.append("지정 그룹 수는 2 이상이어야 합니다")

            row_count = len(self.raw_data)

            if self.n_clusters > row_count:
                self.errors.append("지정 그룹 수는 데이터 행의 개수보다 작아야 합니다")

            if self.min_per not in (None, ""):
                if self.n_clusters * self.min_per > row_count:
                    self.errors.append(
                        f"현재 데이터 {row_count}명으로는 최소 {self.min_per}명씩 {self.n_clusters}개의 그룹을 만들 수 없습니다. 설정을 변경해주세요"
                    )
            if self.max_per not in (None, ""):
                if self.n_clusters * self.max_per < row_count:
                    self.errors.append("데이터가 많아 그룹 수, 최대 인원수 제한을 맞출 수 없습니다. 설정값을 변경해주세요")


    # 가중치 데이터 체크
    def _check_factorWeight(self, moduleType):
        if self.factorWeight != None and len(self.factorWeight) > 0:
            factorWeight = self.factorWeight

            if moduleType == "JSON":
                # factorWeight가 dist 객체
                factorWeight = cast(dict, factorWeight[0])

                if len(self.raw_data[0]) != len(factorWeight)+1: # raw_data 안에는 name컬럼도 들어있어서 1을 추가함
                    self.errors.append(f"가중치 데이터의 수({len(factorWeight)})는 컬럼 수({len(self.raw_data[0])-1})와 같아야 합니다")
                for weight in factorWeight.values():
                    try:
                        float(weight)
                    except(ValueError, TypeError):
                        self.errors.append(f"가중치 데이터는 숫자만 기입 가능합니다. 제한된 값 : {weight}")
                        continue
                    if float(weight) > 3 or float(weight) < 0.5:
                        self.errors.append(f"가중치 데이터는 0.5 이상, 3 이하여야 합니다. 제한된 값 : {weight}")
                
                self.factorWeight = factorWeight


            elif moduleType == "CSV":
                # factorWeight가 list 객체
                if len(self.raw_data[0]) != len(factorWeight)+1: # raw_data 안에는 name컬럼도 들어있어서 1을 추가함
                    self.errors.append(f"가중치 데이터의 수({len(factorWeight)})는 컬럼 수({len(self.raw_data[0])-1})와 같아야 합니다")
                for weight in factorWeight:
                    try:
                        float(weight)
                    except(ValueError, TypeError):
                        self.errors.append(f"가중치 데이터는 숫자만 기입 가능합니다. 제한된 값 : {weight}")
                        continue
                    if float(weight) > 3 or float(weight) < 0.5:
                        self.errors.append(f"가중치 데이터는 0.5 이상, 3 이하여야 합니다. 제한된 값 : {weight}")


    # CSV 파일 체크
    def _check_CSV(self, request):
        # CSV 추가 validation 체크
        if not request.content_type.startswith("multipart/form-data"):
            raise ValidationError('multipart/form-data로 전송되어야 합니다')

        file = request.files.get('csvData')
        if file == None:
            raise ValidationError({'error': '파일이 전송되지 않았습니다'})
        if len(file.read()) == 0:
            raise ValidationError({'error': '파일이 비어있습니다'})
        if file.filename == '':
            raise ValidationError({'error': '파일 이름이 없습니다'})
        if not str(file.filename).lower().endswith(".csv"):
            raise ValidationError({'error': 'CSV 파일이 아닙니다'})

        # validation 체크하느라 한번 read 했어서 포인터 앞으로 돌림
        file.seek(0)

        # FileStorage는 바이너리 스트림이라 디코딩 필요
        stream = io.StringIO(file.stream.read().decode("utf-8"))
        lines = stream.getvalue().splitlines()

        # 가중치 데이터 검사 | 첫 컬럼이 factorWeight인 행 찾음
        factorWeight = None
        dataWithoutWeight = lines
        for line in lines:
            if line.split(",")[0] == 'factorWeight':
                # 가중치 데이터 존재함. 가져옴
                factorWeight = line.split(",")
                break
        if factorWeight != None:
            # 가중치 데이터 있음
            dataWithoutWeight = [line for line in lines if line.split(",")[0] != "factorWeight"]
            self.factorWeight = factorWeight[1:]
        
        # 가중치 데이터 제외하고 첫번째 줄 기준 열 개수
        expected_num_cols = len(dataWithoutWeight[0].split(","))
        for i, line in enumerate(dataWithoutWeight[1:], start=2):  # 2번째 줄부터 검사
            num_cols = len(line.split(","))
            if num_cols != expected_num_cols:
                self.errors.append(f"{i}번째 줄의 열 개수({num_cols})가 헤더({expected_num_cols})와 다릅니다.")

        if self.errors:
            raise ValidationError(self.errors)

        # 가중치를 제거한 데이터
        csv_text = "\n".join(dataWithoutWeight)
        csv_buffer = StringIO(csv_text)
        df = pd.read_csv(csv_buffer)
        self.raw_data = df.to_dict(orient='records')

        # 문제 없으면 데이터프레임으로 읽기
        # stream.seek(0)  # 다시 처음으로 이동해서 read_csv
        # df = pd.read_csv(stream)
        # self.raw_data = df.to_dict(orient='records')
    

    def _check_JSON(self):
        raw_data = self.raw_data

        # 몇몇 데이터 row의 컬럼명이 다른 경우
        # 첫번째 행의 key값을 전부 가져옴
        reference_keys = set(raw_data[0].keys())

        # 각 행의 key값을 하나씩 가져와서 첫 행의 key값들과 비교
        for idx, item in enumerate(raw_data):
            current_keys = set(item.keys())
            if current_keys != reference_keys:
                self.errors.append(
                    f"컬럼명 불일치 발생 | 1번 컬럼명: {reference_keys}, {idx+1}번 컬럼명: {current_keys}"
                )
        if self.errors:
            raise ValidationError(self.errors)

        
        