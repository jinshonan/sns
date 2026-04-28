# app\interface\routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.infrastructure.database import db
from app.domain.models import User, Idea
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, login_required

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

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # 🔥 THIS IS WHAT YOU WERE MISSING
            return redirect(url_for("main.ideas"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@main_bp.route("/ideas")
def ideas():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    pagination = Idea.query.order_by(Idea.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    ideas = pagination.items

    return render_template(
        'ideas.html',
        ideas=ideas,
        pagination=pagination
    )


@main_bp.route("/create", methods=["GET", "POST"])
def create_idea():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:
            # you can flash message later
            return render_template("create.html", error="All fields are required")

        new_idea = Idea(
            title=title,
            content=content,
            created_by=current_user.id
        )

        db.session.add(new_idea)
        db.session.commit()

        return redirect(url_for("main.my_ideas"))

    return render_template("create.html")


@main_bp.route("/ideas/my", methods=["GET", "POST"])
def my_ideas():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    pagination = Idea.query.filter_by(created_by=current_user.id)\
        .order_by(Idea.created_at.desc())\
        .paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    ideas = pagination.items

    return render_template(
        'myidea.html',
        ideas=ideas,
        pagination=pagination
    )


@main_bp.route("/ideas/delete/<int:idea_id>", methods=["POST"])
def delete_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)

    # 🔒 Ensure user owns the idea
    if idea.created_by != current_user.id:
        abort(403)

    db.session.delete(idea)
    db.session.commit()

    return redirect(url_for("main.my_ideas"))


@main_bp.route("/ideas/edit/<int:idea_id>", methods=["GET", "POST"])
def edit_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)

    if idea.created_by != current_user.id:
        abort(403)

    if request.method == "POST":
        idea.title = request.form.get("title")
        idea.content = request.form.get("content")

        db.session.commit()
        return redirect(url_for("main.my_ideas"))

    return render_template("edit.html", idea=idea)


@main_bp.route("/ideas/like/<int:idea_id>", methods=["POST"])
def toggle_like(idea_id):
    idea = Idea.query.get_or_404(idea_id)

    if current_user.liked_ideas.filter_by(id=idea.id).first():
        # already liked → unlike
        current_user.liked_ideas.remove(idea)
    else:
        # not liked → like
        current_user.liked_ideas.append(idea)

    db.session.commit()

    return redirect(url_for("main.ideas"))