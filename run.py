# run.py

from flask import Flask
from dotenv import load_dotenv
import os

from app.interface.routes import main_bp
from app.infrastructure.database import init_db, migrate  # migrateをインポート

from flask_login import LoginManager
from app.domain.models import User

load_dotenv()  # .envを読み込む

login_manager = LoginManager()

def create_app():
    # Flaskオブジェクトの生成
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

    # DB設定
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idea_hub.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # .envにある

    # ユーザー管理
    login_manager.init_app(app)
    login_manager.login_view = "main.login"  # redirect if not logged in

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # DB初期化
    init_db(app)
    app.register_blueprint(main_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)