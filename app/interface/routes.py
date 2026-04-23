# app\interface\routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.infrastructure.database import db
from app.domain.models import User
from werkzeug.security import check_password_hash
from app.domain.models import Idea

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
    ideas = Idea.query.all()
    return render_template("ideas.html", ideas=ideas)

@main_bp.route("/create")
def create_idea():
    return render_template("create.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("main.ideas"))
        else:
            flash("ユーザー名またはパスワードが違います")
            return redirect(url_for("main.login"))

    return render_template("login.html")