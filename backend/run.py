from app import create_app  # app/__init__.py 에 정의된 함수

app = create_app()          # Flask 인스턴스를 생성

if __name__ == '__main__':
    app.run(debug=True)     # 개발용 WAS 구동 (Flask 내부 웹서버)
