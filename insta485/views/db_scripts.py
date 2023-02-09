"""SQL scripts.

sqlite3 var/insta485.sqlite3 ""
"""
JUST_INSERTED_ID = "SELECT last_insert_rowid();"
GET_EXPLORE = "SELECT username FROM users WHERE username NOT IN "\
    "(SELECT username2 FROM following WHERE username1 = ?) AND username != ?;"


# table: users
GET_USER_FULL_INFO = "SELECT * FROM users WHERE username = ?;"
NEW_USER = "INSERT INTO users (username, fullname, email, filename, password)"\
    " VALUES (?, ?, ?, ?, ?);"
DEL_USER = "DELETE FROM users WHERE username = ?;"
UPDATE_USER = "UPDATE users SET fullname = ?, email = ? WHERE username = ?;"
RE_UPDATE_USER = "UPDATE users SET filename = ? WHERE username = ?;"
UPDATE_PASSWORD = "UPDATE users SET password = ? WHERE username = ?;"


# table: posts
GET_HOME_POSTS_ALL_INFO = "SELECT DISTINCT posts.* FROM posts INNER JOIN "\
    "following ON posts.owner = following.username1 WHERE posts.owner = ? OR "\
    "following.username2 = ? GROUP BY posts.postid ORDER BY posts.postid DESC"
GET_RESULTS = f"WITH results AS (SELECT postid, '/api/v1/posts/' || postid ||"\
    f" '/' AS url FROM ({GET_HOME_POSTS_ALL_INFO}) WHERE postid <= ?) "\
    "SELECT * FROM results"
GET_POST_FULL_INFO = "SELECT * FROM posts WHERE postid = ?;"
GET_PROFILE_POSTS_INFO = "SELECT posts.postid, posts.filename FROM users "\
    "INNER JOIN posts ON users.username = posts.owner WHERE "\
    "users.username = ?;"
GET_POSTS_FOR_USER = "SELECT filename FROM posts WHERE owner = ?;"
DEL_POST = "DELETE FROM posts WHERE postid = ?;"
NEW_POST = "INSERT INTO posts(filename, owner) VALUES (?, ?);"


# table: likes
GET_LIKER = "SELECT owner FROM likes WHERE postid = ?;"
GET_LIKEID_FROM_LIKER = "SELECT likeid FROM likes WHERE owner = ? AND "\
    "postid = ?;"
GET_LIKER_FROM_LIKEID = "SELECT owner FROM likes WHERE likeid = ?;"
GIVE_LIKE = "INSERT INTO likes(owner, postid) VALUES (?, ?);"
REMOVE_LIKE = "DELETE FROM likes WHERE owner = ? AND postid = ?;"
REMOVE_LIKE_BY_LIKEID = "DELETE FROM likes WHERE likeid = ?;"

# table: comments
GET_COMMENT_INFO_PER_POST = "SELECT owner, text, commentid FROM comments "\
    "WHERE postid = ?;"
GET_COMMENT = "SELECT owner FROM comments WHERE commentid = ?;"
NEW_COMMENT = "INSERT INTO comments(owner, postid, text) VALUES (?, ?, ?);"
DEL_COMMENT = "DELETE FROM comments WHERE commentid = ?;"

# table: following
GET_FOLLOWERS = "SELECT username1 FROM following WHERE username2 = ?;"
GET_FOLLOWING = "SELECT username2 FROM following WHERE username1 = ?;"
FOLLOW_USER = "INSERT INTO following(username1, username2) VALUES (?, ?);"
UNFOLLOW_USER = "DELETE FROM following WHERE username1 = ? AND username2 = ?;"
