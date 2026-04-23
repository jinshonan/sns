# app\domain\models.py

from app.infrastructure.database import db
from datetime import datetime, timezone

# --- 1. 中間テーブル (Association Table) の定義 ---
# 特定のクラスに属さない「テーブル」として定義するのが一般的です
idea_likes = db.Table('idea_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('idea_id', db.Integer, db.ForeignKey('ideas.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=lambda: datetime.now(timezone.utc))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # リレーション：作成したアイデア
    ideas = db.relationship('Idea', backref='author', lazy=True)
    
    # --- 追加：いいねしたアイデア (多対多) ---
    liked_ideas = db.relationship('Idea', 
                                  secondary=idea_likes, 
                                  backref=db.backref('liked_by_users', lazy='dynamic'), 
                                  lazy='dynamic')


class Idea(db.Model):
    __tablename__ = 'ideas'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # 前回の likes_count (数値) は、この中間テーブルの件数を数える形にすれば不要になりますが、
    # パフォーマンスのために「数値カラム」として残しておく手法（キャッシュ）もあります。