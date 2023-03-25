from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import not_

from blog.models.database import db
from blog.models import Author, Article, Tag
from blog.forms.article import CreateArticleForm
import requests
import json
import os

articles_app = Blueprint("articles_app", __name__)


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():
        article = Article(title=form.title.data.strip(), body=form.body.data)
        db.session.add(article)
        if current_user.author:
            # use existing author if present
            article.author_id = current_user.author.id
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            article.author_id = author.id
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("articles_app.details", article_id=article.id))
    return render_template("articles/create.html", form=form, error=error)


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id):
    article = Article.query.filter_by(id=article_id).options(
        joinedload(Article.tags)
    ).one_or_none()
    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


@articles_app.route("/<string:tag_name>/", endpoint="articles-by-tag")
def articles_by_tag(tag_name):
    target_tag = Tag.query.filter_by(name=tag_name).first()
    target_articles = []
    articles = Article.query.all()
    for article in articles:
        if target_tag in article.tags:
            target_articles.append(article)
    if target_articles is None:
        raise NotFound
    return render_template("articles/list.html", articles=target_articles)


@articles_app.route("/from-api/", methods=["GET"], endpoint="articles-from-api")
def articles_from_api():
    api_url = os.environ.get("API_URL")
    data_dict = requests.get(f'{api_url}/api/articles/').json()
    # data_dict = json.loads(data.text)
    articles = []
    for article in data_dict["data"]:
        articles.append(article["attributes"]["title"])
    return render_template("articles/list_from_api.html", articles=articles)
