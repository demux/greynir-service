from flask import current_app as app, Response

@app.route('/')
def index():
    return Response('Greynir Service')

from .api import *
