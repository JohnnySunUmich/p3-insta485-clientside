"""Insta485 REST API."""
from insta485 import app
from insta485.api.restapi import restapi


app.register_blueprint(restapi, url_prefix='/api/v1/')
