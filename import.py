# import.py アイデア・インポート

import json
import random
from datetime import datetime, timezone, timedelta

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))  # 現在のフォルダをパスに追加

from app.infrastructure.database import db
from app.domain.models import Idea
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

def random_date_last_year() -> datetime:
    """2025年1月1日〜2025年12月31日のランダムなdatetimeを返す"""
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    end = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

with app.app_context():
    with open("rawdata.json", "r", encoding="utf-8") as f:
        ideas = json.load(f)

    for item in ideas:
        idea = Idea(
            title=item["title"],
            content=item["content"],
            created_by=item["created_by"],
            created_at=random_date_last_year(),
        )
        db.session.add(idea)

    db.session.commit()
    print(f"{len(ideas)}件のアイデアをインポートしました")