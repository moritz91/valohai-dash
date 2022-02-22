import os
from flask import Flask
from werkzeug import run_simple
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

class PrefixMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        for prefix in (
            environ.get("HTTP_X_VH_PREFIX"),
            os.environ.get("VH_DEFAULT_PREFIX"),
        ):
            if not prefix:  # Could have no header or no envvar, so skip
                continue
            if path.startswith(prefix):  # If the path starts with this prefix,
                # ... then strip the prefix out as far as WSGI is concerned.
                environ["PATH_INFO"] = "/" + path[len(prefix) :].lstrip("/")
                break

        return self.app(environ, start_response)

server = Flask(__name__)
server.wsgi_app = PrefixMiddleware(server.wsgi_app)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.config.update({
    'requests_pathname_prefix': os.environ.get("VH_DEFAULT_PREFIX")
})

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == "__main__":
    run_simple("0.0.0.0", 8000, use_reloader=True, application=server)
