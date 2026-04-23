# app\infrastructure\database.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # 追加

db = SQLAlchemy()
migrate = Migrate()  # 追加

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)  # 追加：FlaskとDBとMigrateを紐付け
    
    with app.app_context():
        from app.domain.models import User, Idea
        # db.create_all() 
        # ↑ 今後は migrate を使うので、この行はコメントアウト（または削除）してもOKです