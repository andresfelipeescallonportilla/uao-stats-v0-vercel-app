#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization.
#######################################################

#Libraries
import dash
import dash_bootstrap_components as dbc


###############
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#server = app.server
##############

#running the app
# Boostrap CSS (passed as external_stylesheets; app.css.append_css is deprecated in recent Dash).
#'https://codepen.io/amyoshino/pen/jzXypZ.css'
#'https://codepen.io/chriddyp/pen/bWLwgP.css'
external_stylesheets = [
    'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# WSGI entrypoint for gunicorn / Vercel (@vercel/python)
server = app.server

app.title = 'UAO Stats' # default project name
#app.css.append_css({'external_url': 'http://code.jquery.com/jquery-3.3.1.min.js'})
#app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'})

# We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True

##########################
#This is the end of app.py
##########################
