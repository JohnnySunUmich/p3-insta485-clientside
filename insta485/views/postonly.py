"""Insta485 post-only view. Handle backend, interact with database.

curl -X POST http://localhost:8000/posts/ -F postid=1 -F operation=delete
--cookie cookies.txt
URLs include:
/likes/
/comments/
/following/
/posts/
/accounts/
"""
from sqlite3 import Connection, Cursor
from pathlib import Path
import uuid
import hashlib
from flask import Blueprint, request, redirect, url_for, session, abort
from insta485 import app, model
from insta485.views.db_scripts import GET_LIKER, GIVE_LIKE, REMOVE_LIKE,\
    NEW_COMMENT, GET_COMMENT, DEL_COMMENT, GET_FOLLOWING, FOLLOW_USER,\
    UNFOLLOW_USER, NEW_POST, GET_POST_FULL_INFO, DEL_POST, GET_USER_FULL_INFO,\
    NEW_USER, GET_POSTS_FOR_USER, DEL_USER, UPDATE_USER, RE_UPDATE_USER,\
    UPDATE_PASSWORD


postonly = Blueprint("postonly", __name__)


def any_empty(*to_check) -> bool:
    """For helper function to check if any is empty."""
    return any(item == "" for item in to_check)


@postonly.route("/likes/", methods=["POST"])
def likes():
    """Interact with likes table."""
    logname: str = session["logname"]
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    url: str = request.args.get("target")
    operation: str = request.form["operation"]
    postid: str = request.form["postid"]
    likers: list = cursor.execute(GET_LIKER, (postid,)).fetchall()
    if (operation == "like" and {"owner": logname} in likers) or\
       (operation == "unlike" and {"owner": logname} not in likers):
        abort(409)
    if operation == "like":
        cursor.execute(GIVE_LIKE, (logname, postid))
    elif operation == "unlike":
        cursor.execute(REMOVE_LIKE, (logname, postid))
    conn.commit()
    conn.close()
    return redirect(url if url else url_for('misc.home'))


@postonly.route("/comments/", methods=["POST"])
def comments():
    """Interact with comments table."""
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    url: str = request.args.get("target")
    operation: str = request.form["operation"]
    if operation == "create":
        postid: str = request.form["postid"]
        text: str = request.form["text"]
        if any_empty(text):
            abort(400)
        cursor.execute(NEW_COMMENT, (session["logname"], postid, text))
    elif operation == "delete":
        commentid: str = request.form["commentid"]
        if cursor.execute(GET_COMMENT, (commentid,)).fetchone()["owner"] !=\
           session["logname"]:
            abort(403)
        cursor.execute(DEL_COMMENT, (commentid,))
    conn.commit()
    conn.close()
    return redirect(url if url else url_for('misc.home'))


@postonly.route("/following/", methods=["POST"])
def following():
    """Interact with following table."""
    logname: str = session["logname"]
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    url: str = request.args.get("target")
    operation: str = request.form["operation"]
    username: str = request.form["username"]
    ln_following: list = cursor.execute(GET_FOLLOWING, (logname,)).fetchall()
    if (operation == "follow" and {"username2": username} in ln_following) or\
       (operation == "unfollow" and {"username2": username} not in
       ln_following):
        abort(409)
    if operation == "follow":
        cursor.execute(FOLLOW_USER, (logname, username))
    elif operation == "unfollow":
        cursor.execute(UNFOLLOW_USER, (logname, username))
    conn.commit()
    conn.close()
    return redirect(url if url else url_for('misc.home'))


@postonly.route("/posts/", methods=["POST"])
def posts():
    """Interact with posts table."""
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    url: str = request.args.get("target")
    operation: str = request.form["operation"]
    if operation == "create":
        file = request.files.get("file")
        if file is None or file == "" or file.filename == "":
            abort(400)
        back = Path(file.filename).suffix.lower()
        filename: Path = f"{uuid.uuid4().hex}{back}"
        file.save(app.config["UPLOAD_FOLDER"]/filename)
        cursor.execute(NEW_POST, (filename, session["logname"]))
    elif operation == "delete":
        postid: str = request.form["postid"]
        if cursor.execute(GET_POST_FULL_INFO, (postid,)).fetchone()["owner"]\
           != session["logname"]:
            abort(403)
        (app.config["UPLOAD_FOLDER"]/cursor.execute(GET_POST_FULL_INFO,
         (postid,)).fetchone()["filename"]).unlink()
        cursor.execute(DEL_POST, (postid,))
    conn.commit()
    conn.close()
    return redirect(url if url else url_for('users.user_profile',
                    username=session["logname"]))


def verify_password(username: str, password: str) -> tuple[bool, str]:
    """For helper functions to verify password."""
    cursor: Cursor = model.get_db().cursor()
    _, the_salt, real_pw = cursor.execute(
        GET_USER_FULL_INFO, (username,)).fetchone()["password"].split('$')
    entered_pw = hashlib.new("sha512")
    entered_pw.update((the_salt + password).encode('utf-8'))
    entered_pw = entered_pw.hexdigest()
    return entered_pw == real_pw, "$".join([_, the_salt, entered_pw])


def accounts_create(cursor: Cursor):
    """For helper functions to /accounts/ operation=create."""
    username: str = request.form["username"]
    password: str = request.form["password"]
    fullname: str = request.form["fullname"]
    email: str = request.form["email"]
    file = request.files.get("file")
    if any_empty(username, password, fullname, email, file) or file is None or\
       file == "" or file.filename == "":
        abort(400)
    if cursor.execute(GET_USER_FULL_INFO, (username,)).fetchone() is not None:
        abort(409)
    filename: Path = f"{uuid.uuid4().hex}{Path(file.filename).suffix.lower()}"
    file.save(app.config["UPLOAD_FOLDER"]/filename)
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new("sha512")
    hash_obj.update((salt + password).encode('utf-8'))
    pw_str = "$".join(["sha512", salt, hash_obj.hexdigest()])
    cursor.execute(NEW_USER, (username, fullname, email, filename, pw_str))
    session["logname"] = username


@postonly.route("/accounts/", methods=["POST"])
def accounts():
    """Interact with users table and other tables."""
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    url: str = request.args.get("target")
    operation: str = request.form["operation"]
    match operation:
        case "login":
            if any_empty(request.form["username"], request.form["password"]):
                abort(400)
            if cursor.execute(GET_USER_FULL_INFO, (request.form["username"],))\
               .fetchone() is None or not \
               verify_password(request.form["username"],
               request.form["password"])[0]:
                abort(403)
            session["logname"] = request.form["username"]
        case "create":
            accounts_create(cursor)
        case "delete":
            if "logname" not in session:
                abort(403)
            for filedict in cursor.execute(GET_POSTS_FOR_USER,
                                           (session["logname"],)).fetchall():
                (app.config["UPLOAD_FOLDER"]/filedict["filename"]).unlink()
            (app.config["UPLOAD_FOLDER"]/cursor.execute(GET_USER_FULL_INFO,
             (session["logname"],)).fetchone()["filename"]).unlink()
            cursor.execute(DEL_USER, (session["logname"],))
            session.clear()
        case "edit_account":
            if "logname" not in session:
                abort(403)
            logname_ea: str = session["logname"]
            fullname: str = request.form["fullname"]
            email: str = request.form["email"]
            if any_empty(fullname, email):
                abort(400)
            cursor.execute(UPDATE_USER, (fullname, email, logname_ea))
            file = request.files.get("file")
            if file.filename != "":
                (app.config["UPLOAD_FOLDER"]/cursor.execute(GET_USER_FULL_INFO,
                 (logname_ea,)).fetchone()["filename"]).unlink()
                suffix = Path(file.filename).suffix.lower()
                filename: Path = f"{uuid.uuid4().hex}{suffix}"
                file.save(app.config["UPLOAD_FOLDER"]/filename)
                cursor.execute(RE_UPDATE_USER, (filename, logname_ea))
        case "update_password":
            if "logname" not in session:
                abort(403)
            logname_up: str = session["logname"]
            password: str = request.form["password"]
            new_password1: str = request.form["new_password1"]
            new_password2: str = request.form["new_password2"]
            if any_empty(password, new_password1, new_password2):
                abort(400)
            if not verify_password(logname_up, password)[0]:
                abort(403)
            if new_password1 != new_password2:
                abort(401)
            cursor.execute(UPDATE_PASSWORD, (verify_password(
                logname_up, new_password1)[1], logname_up))
    conn.commit()
    conn.close()
    return redirect(url if url else url_for('misc.home'))
