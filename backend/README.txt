## 🔧 Run Backend (Flask)

# VSCode에서 Python, Python Debugger 확장 설치

# 터미널에서 백엔드 폴더 접근
cd backend

# 파이썬 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# requirements.txt 문서에 쓰인 모듈들 일괄 설치
pip install -r requirements.txt

# Flask WAS 실행 명령어
python run.py


## Debug 방법
# Run and Debug(실행 및 디버그) 탭 클릭
# 탭창 상단에 초록색 재생버튼 클릭
# - 디버그 설정은 .vscode/launch.json 파일로 변경 가능



## 🔧 백엔드 테스트 자동화

# 설치
pip install pytest requests


## requirements.txt 갱신
pip freeze > requirements.txt
