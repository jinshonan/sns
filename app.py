from flask import Flask
from app.interface.routes import main_bp

# Flaskオブジェクトの生成
app = Flask(__name__)

# Blueprintをアプリに登録する
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)