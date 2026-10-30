"""Vercel serverless entrypoint (@vercel/python): exposes the Dash Flask server as a WSGI app."""
import os
import sys

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")

# The dashboard modules use paths relative to app/ (data/, assets/) and import `app` / `lib` as top-level.
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from index_h import app as dash_flask_app  # noqa: E402

flask_app = dash_flask_app.server
application = flask_app
app = flask_app
