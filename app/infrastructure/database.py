from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        from app.domain.models import User, Idea  # 循環import防止のためここで
        db.create_all()