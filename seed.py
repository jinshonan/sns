# seed.py 初期ユーザー作成用
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))  # 現在のフォルダをパスに追加

from app.infrastructure.database import db
from app.domain.models import User
from werkzeug.security import generate_password_hash
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# create_appと同じ設定を直接書く
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idea_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

from app.infrastructure.database import init_db
init_db(app)

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        user = User(
            username='admin',
            password_hash=generate_password_hash('your-password')
        )
        db.session.add(user)
        db.session.commit()
        print('ユーザー作成完了！')
    else:
        print('すでに存在します')
        # パス変更
        try:
            user = User.query.filter_by(username='admin').first()
            user.password_hash = generate_password_hash('pass')
            db.session.commit()
            print('パスワード変更しました！')
        except Exception as e:
            print("パスワード変更が出来ませんでした！", e)