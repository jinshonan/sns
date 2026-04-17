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
    return "Bye Bye World"

@main_bp.route("/index")
def index():
    # template_folderを指定しているので、ファイル名だけでOK
    return render_template("index.html")

@main_bp.route("/ideas")
def ideas():
    return render_template("ideas.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")
