from flask import Blueprint, render_template

# Blueprintの作成
# 'main'はBlueprintの名前
# template_folderは、このファイル(routes.py)から見た相対パスで指定します
main_bp = Blueprint(
    'main', 
    __name__, 
    template_folder='../templates'  # デフォルト？
)

@main_bp.route("/")
def hello():
    return "Hello World"

@main_bp.route("/index")
def index():
    # template_folderを指定しているので、ファイル名だけでOK
    return render_template("index.html")