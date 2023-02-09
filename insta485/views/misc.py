"""
Insta485 misc view.

Renaming columns for sqlite3 ALTER TABLE ? RENAME COLUMN old_col TO new_col;
URLs include:
/
/explore/
/posts/
"""
from sqlite3 import Cursor
from flask import Blueprint, render_template, send_from_directory, redirect,\
    url_for, session, abort
from arrow import utcnow, get
from insta485 import app, model
from insta485.views.users import fol_exp
from insta485.views.db_scripts import GET_HOME_POSTS_ALL_INFO,\
    GET_USER_FULL_INFO, GET_LIKER, GET_COMMENT_INFO_PER_POST, GET_EXPLORE,\
    GET_POST_FULL_INFO


misc = Blueprint("misc", __name__)


@misc.route('/')
def home():
    """Display / route.

    context = {"logname":, "posts": [{post1}, {post2}]}
    each_post = {
        "postid": ,
        "filename"(post-content): ,
        "owner": ,
        "created":  ,
        "pfp": ,
        "likes"(#likes): ,
        "liked"(logname liked?): ,
        "comments": [{"owner": , "text":, "commentid"}, {}]
    }
    """
    if "logname" not in session:
        return redirect(url_for('admin.login'))
    logname: str = session["logname"]
    context: dict = {"logname": logname}
    cursor: Cursor = model.get_db().cursor()
    context["posts"] = cursor.execute(
        GET_HOME_POSTS_ALL_INFO, (logname, logname)).fetchall()
    for post in context["posts"]:
        post["created"] = get(post["created"]).humanize(utcnow())
        post["pfp"] = cursor.execute(
            GET_USER_FULL_INFO, (post["owner"],)).fetchone()["filename"]
        users_liked = cursor.execute(
            GET_LIKER, (post["postid"],)).fetchall()
        post["likes"] = len(users_liked)
        post["liked"] = {"owner": logname} in users_liked
        post["comments"] = cursor.execute(
            GET_COMMENT_INFO_PER_POST, (post["postid"],)).fetchall()
    return render_template("index.html", **context)


@misc.route("/explore/")
def explore():
    """Display /explore/ route."""
    return redirect(url_for('admin.login')) if "logname" not in session else\
        fol_exp("", True, "explore", GET_EXPLORE)


@misc.route("/posts/<postid>/")
def posts(postid: int):
    """Display /posts/<postid>/ route.

    context = {
        "logname": ,
        "postid": ,
        "post":{"postid": , "filename"(pic): , "owner": , "created": , "pfp":,
        "num_likes": , "liked": , "comments": ["owner":,"text":,"commentid":]}
    }
    """
    if "logname" not in session:
        return redirect(url_for('admin.login'))
    logname: str = session["logname"]
    context: dict = {"logname": logname, "postid": postid}
    cursor: Cursor = model.get_db().cursor()
    context["post"] = cursor.execute(
        GET_POST_FULL_INFO, (postid,)).fetchone()
    context["post"]["created"] = get(
        context["post"]["created"]).humanize(utcnow())
    context["post"]["pfp"] = cursor.execute(
        GET_USER_FULL_INFO, (context["post"]["owner"],)).fetchone()["filename"]
    users_liked = cursor.execute(GET_LIKER, (postid, )).fetchall()
    context["post"]["num_likes"] = len(users_liked)
    context["post"]["liked"] = {"owner": logname} in users_liked
    context["post"]["comments"] = cursor.execute(
        GET_COMMENT_INFO_PER_POST, (postid,)).fetchall()
    return render_template("post.html", **context)


@misc.route('/uploads/<filename>')
def render_pic(filename: str):
    """Render picture from /var/uploads/<filename>/ route."""
    if "logname" not in session:
        abort(403)
    if not (app.config["UPLOAD_FOLDER"]/filename).exists():
        abort(404)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
