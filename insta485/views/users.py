"""
Insta485 users view.

URLs include:
/users/<username>/
/users/<username>/following/
/users/<username>/followers/
"""
from sqlite3 import Cursor
from flask import Blueprint, render_template, redirect, url_for, session,\
    abort
from insta485 import model
from insta485.views.db_scripts import GET_USER_FULL_INFO, GET_FOLLOWERS,\
    GET_FOLLOWING, GET_PROFILE_POSTS_INFO


users = Blueprint("users", __name__)


@users.route("/<username>/")
def user_profile(username: str):
    """Display /users/<username>/ route.

    context = {
        "logname": ,
        "username": ,
        "range"(func): ,
        "fullname": ,
        "num_followers": ,
        "num_following": ,
        "logname_fol_user"(T/F): ,
        "num_posts": ,
        "posts": [{"postid": , "filename": }, {}]
    }
    """
    if "logname" not in session:
        return redirect(url_for('admin.login'))
    cursor: Cursor = model.get_db().cursor()
    if cursor.execute(GET_USER_FULL_INFO, (username,)).fetchone() is None:
        abort(404)
    logname: str = session["logname"]
    context: dict = {"logname": logname,
                     "username": username, "range": range}
    cursor.execute(GET_USER_FULL_INFO, (username,))
    context["fullname"] = cursor.fetchone()["fullname"]
    cursor.execute(GET_FOLLOWERS, (username, ))
    follower_list: list[dict] = cursor.fetchall()
    context["num_followers"] = len(follower_list)
    cursor.execute(GET_FOLLOWING, (username, ))
    context["num_following"] = len(cursor.fetchall())
    cursor.execute(GET_FOLLOWING, (logname, ))
    context["logname_fol_user"] = {
        "username2": username} in cursor.fetchall()
    cursor.execute(GET_PROFILE_POSTS_INFO, (username,))
    posts: list[dict] = cursor.fetchall()
    context["num_posts"] = len(posts)
    context["posts"] = posts
    return render_template("user.html", **context)


def fol_exp(username: str, explore: bool, template: str, dbscript: str):
    """For following, followers, and explore.

    context = {
        "logname": ,
        "accounts": [{"acc_name": , "pfp": , "logname_fol_acc"}, {}],
        "explore": False
    }
    """
    cursor: Cursor = model.get_db().cursor()
    if not explore and cursor.execute(
            GET_USER_FULL_INFO, (username,)).fetchone() is None:
        abort(404)
    logname: str = session["logname"]
    context: dict = {"logname": logname, "accounts": [], "explore": explore}
    placeholder: set = (username,) if not explore else (logname, logname)
    cursor.execute(dbscript, placeholder)
    for i in cursor.fetchall():
        account: dict = {"acc_name": i["username" if explore else (
            "username1" if dbscript == GET_FOLLOWERS else "username2")]}
        cursor.execute(GET_USER_FULL_INFO, (account["acc_name"],))
        account["pfp"] = cursor.fetchone()["filename"]
        if not explore:
            cursor.execute(GET_FOLLOWERS, (account["acc_name"],))
            account["logname_fol_acc"] = {
                "username1": logname} in cursor.fetchall()
        context["accounts"].append(account)
    return render_template(f"{template}.html", **context)


@users.route("/<username>/followers/")
def user_followers(username: str):
    """Display /users/<username>/followers/ route."""
    return redirect(url_for('admin.login')) if "logname" not in session else\
        fol_exp(username, False, "followers", GET_FOLLOWERS)


@users.route("/<username>/following/")
def user_following(username: str):
    """Display /users/<username>/following/ route."""
    return redirect(url_for('admin.login')) if "logname" not in session else\
        fol_exp(username, False, "following", GET_FOLLOWING)
