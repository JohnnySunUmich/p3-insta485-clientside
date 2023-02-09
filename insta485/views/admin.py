"""
Insta485 admin view.

URLs include:
/accounts/login/
/accounts/logout/
/accounts/create/
/accounts/edit/
/accounts/delete/
/accounts/password/
"""

from flask import Blueprint, render_template, redirect, url_for, session,\
    Response
from insta485 import model
from insta485.views.db_scripts import GET_USER_FULL_INFO


admin = Blueprint("admin", __name__)


@admin.route("/login/")
def login():
    """Display /accounts/login/ route."""
    return render_template("login.html") if "logname" not in session else\
        redirect(url_for('misc.home'))


@admin.route("/logout/", methods=["POST"])
def logout() -> Response:
    """Display /accounts/logout/ route."""
    session.clear()
    return redirect(url_for('admin.login'))


@admin.route("/create/")
def create():
    """Display /accounts/create/ route."""
    return render_template("create.html") if "logname" not in session else\
        redirect(url_for('admin.edit'))


@admin.route("/delete/")
def delete():
    """Display /accounts/delete/ route."""
    return redirect(url_for('admin.login')) if "logname" not in session else\
        render_template("delete.html", logname=session["logname"])


@admin.route("/edit/")
def edit():
    """Display /accounts/edit/ route.

    context = {"fullname": , "email": , "filename": , "logname": }
    """
    if "logname" not in session:
        return redirect(url_for('admin.login'))
    context: dict = model.get_db().cursor().execute(
        GET_USER_FULL_INFO, (session["logname"],)).fetchone()
    context["logname"] = context.pop("username")
    return render_template("edit.html", **context)


@admin.route("/password/")
def password():
    """Display /accounts/password/ route."""
    return redirect(url_for('admin.login')) if "logname" not in session else\
        render_template("password.html", logname=session["logname"])
