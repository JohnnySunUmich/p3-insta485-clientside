"""REST API for index, likes, comments."""
from flask import Blueprint, request, jsonify, session, Response
from sqlite3 import Connection, Cursor
from insta485 import app, model
from insta485.views.db_scripts import JUST_INSERTED_ID, GET_USER_FULL_INFO, GET_LIKER, GET_LIKEID_FROM_LIKER, GIVE_LIKE, GET_LIKER_FROM_LIKEID, REMOVE_LIKE_BY_LIKEID, NEW_COMMENT, GET_COMMENT, DEL_COMMENT, GET_COMMENT_INFO_PER_POST, GET_POST_FULL_INFO, GET_USER_FULL_INFO, GET_RESULTS
import hashlib
from urllib.parse import urlparse

restapi = Blueprint("restapi", __name__)


class Error(Exception):
    status: int = 400
    def __init__(self, message: str, status: int = None) -> None:
        Exception.__init__(self)
        self.message = message
        if status is not None: self.status = status

@app.errorhandler(Error)
def handle_error(e: Error) -> Response:
    response = jsonify({"message": e.message, "status_code": e.status})
    response.status_code = e.status
    return response



def verify_password(logname: str, auth_pw: str) -> bool:   #Helper function
    _, the_salt, real_pw = model.get_db().cursor().execute(GET_USER_FULL_INFO, (logname,)).fetchone()["password"].split('$')
    entered_pw = hashlib.new("sha512")
    entered_pw.update((the_salt + auth_pw).encode('utf-8'))
    entered_pw = entered_pw.hexdigest()
    return entered_pw == real_pw

def check_authentication_error(postid_oor=False, postid=0) -> None:
    auth = request.authorization
    if (auth is None and "logname" not in session) or (auth is not None and not verify_password(auth["username"], auth["password"])): raise Error("Forbidden", 403)
    if postid_oor and model.get_db().cursor().execute(GET_POST_FULL_INFO, (postid, )).fetchone() is None:
        raise Error("Not Found", 404)


@restapi.route("/")
def resource_urls() -> Response:
    return jsonify(
        {
            "comments": "/api/v1/comments/",
            "likes": "/api/v1/likes/",
            "posts": "/api/v1/posts/",
            "url": "/api/v1/"
        }
    )


@restapi.route("/posts/")
def get_index():
    check_authentication_error()
    username: str = session["logname"] if request.authorization is None else request.authorization['username']
    cursor: Cursor = model.get_db().cursor()
    most_recent: int = cursor.execute(f"{GET_RESULTS} LIMIT 1;", (username, username, float("inf"))).fetchone()["postid"]
    postid_lte: int = request.args.get("postid_lte", default=most_recent, type=int)
    size: int = request.args.get("size", default=10, type=int)
    page: int = request.args.get("page", default=0, type=int)
    if (page is not None and page < 0) or (size is not None and size < 0): raise Error("Bad Request", 400)
    url = urlparse(request.url)
    context: dict = {"next": "", "url": f"{url.path}?{url.query}" if len(url.query) != 0 else url.path}
    context["results"] = cursor.execute(f"{GET_RESULTS} LIMIT {size} OFFSET {page * size};", (username, username, postid_lte)).fetchall()
    if len(context["results"]) == size: context["next"] = f"/api/v1/posts/?size={size}&page={page + 1}&postid_lte={postid_lte}"
    return jsonify(**context)


@restapi.route("/posts/<int:postid>/")
def get_post(postid: int) -> Response:
    """Return post on postid."""
    check_authentication_error(True, postid)
    username: str = session["logname"] if request.authorization is None else request.authorization['username']
    cursor: Cursor = model.get_db().cursor()
    context = {"postShowUrl": f"/posts/{postid}/", "postid": postid, "url": f"/api/v1/posts/{postid}/", "comments_url": f"/api/v1/comments/?postid={postid}"}
    postinfo: dict = cursor.execute(GET_POST_FULL_INFO, (postid, )).fetchone()
    poster = postinfo["owner"]
    context["owner"] = poster
    context["ownerShowUrl"] = f"/users/{poster}/"
    context["created"] = postinfo["created"]
    context["imgUrl"] = "/uploads/" + postinfo["filename"]
    context["ownerImgUrl"] = "/uploads/" + cursor.execute(GET_USER_FULL_INFO, (poster, )).fetchone()["filename"]
    comments: list[dict] = cursor.execute(GET_COMMENT_INFO_PER_POST, (postid, )).fetchall()
    for comment in comments:
        comment["lognameOwnsThis"] = username == comment["owner"]
        comment["ownerShowUrl"] = "/users/" + comment["owner"] + "/"
        comment["url"] = "/api/v1/comments/" + str(comment["commentid"]) + "/"
    context["comments"] = comments
    likers: list[dict] = cursor.execute(GET_LIKER, (postid, )).fetchall()
    lognameLikesThis: bool = {"owner": username} in likers
    likes: dict = {"lognameLikesThis": lognameLikesThis, "numLikes": len(likers), "url": None if not lognameLikesThis else "/api/v1/likes/"}
    if lognameLikesThis:
        likeid: str = str(cursor.execute(GET_LIKEID_FROM_LIKER, (username, postid)).fetchone()["likeid"]) + "/"
        likes["url"] += likeid
    context["likes"] = likes
    return jsonify(**context), 200


@restapi.route("/likes/", methods=["POST"])
def give_like() -> Response:
    check_authentication_error()
    username: str = session["logname"] if request.authorization is None else request.authorization['username']
    postid: int = request.args.get("postid")
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    likers: list[dict] = cursor.execute(GET_LIKER, (postid,)).fetchall()
    if {"owner": username} in likers:
        likeid: int = cursor.execute(GET_LIKEID_FROM_LIKER, (username, postid)).fetchone()["likeid"]
        return jsonify(likeid=likeid, url=f"/api/v1/likes/{likeid}/"), 200
    else:
        cursor.execute(GIVE_LIKE, (username, postid))
        likeid = cursor.execute(JUST_INSERTED_ID).fetchone()["last_insert_rowid()"]
        conn.commit()
        conn.close()
        return jsonify(likeid=likeid, url=f"/api/v1/likes/{likeid}/"), 201

@restapi.route("/likes/<int:likeid>/", methods=["DELETE"])
def delete_like(likeid: int) -> Response:
    check_authentication_error()
    username: str = session["logname"] if request.authorization is None else request.authorization['username']
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    liker = cursor.execute(GET_LIKER_FROM_LIKEID, (likeid, )).fetchone()
    if liker is None: return jsonify(), 404
    if liker["owner"] != username: return jsonify(), 403
    cursor.execute(REMOVE_LIKE_BY_LIKEID, (likeid, ))
    conn.commit()
    conn.close()
    return jsonify(), 204


@restapi.route("/comments/", methods=["POST"])
def give_comment() -> Response:
    check_authentication_error()
    username: str = session["logname"] if request.authorization is None else request.authorization['username']
    postid: int = request.args.get("postid")
    comment: str = request.json.get("text")
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    cursor.execute(NEW_COMMENT, (username, postid, comment))
    commentid: int = cursor.execute(JUST_INSERTED_ID).fetchone()["last_insert_rowid()"]
    conn.commit()
    conn.close()
    return jsonify(commentid=commentid, lognameOwnsThis=True, owner=username, ownerShowUrl=f"/users/{username}/", text=comment, url=f"/api/v1/comments/{commentid}/"), 201

@restapi.route("/comments/<int:commentid>/", methods=["DELETE"])
def delete_comment(commentid: int) -> Response:
    check_authentication_error()
    username: str = session["logname"] if request.authorization is None else request.authorization['username']
    conn: Connection = model.get_db()
    cursor: Cursor = conn.cursor()
    commenter = cursor.execute(GET_COMMENT, (commentid, )).fetchone()
    if commenter is None: return jsonify(), 404
    if commenter["owner"] != username: return jsonify(), 403
    cursor.execute(DEL_COMMENT, (commentid, ))
    conn.commit()
    conn.close()
    return jsonify(), 204
