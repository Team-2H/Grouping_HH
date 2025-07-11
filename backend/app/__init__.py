from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)           # Flask 인스턴스 생성
    CORS(app)                       # CORS 허용 (프론트엔드가 다른 도메인에서 접근 가능하게)
    from .routes import main        # 라우트 등록
    app.register_blueprint(main)    # /api/hello 등록됨
    return app                      
