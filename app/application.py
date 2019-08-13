#!/usr/bin/env python3
"""
ELISABETH'S SPORTS ITEM CATALOG

An application that provides a list of sports items within a variety of
categories as well as provide a user registration and authentication system -
implementing third-party OAuth authentication. Registered users have the
ability to post, edit and delete items.
Users can log in with their Google or Facebook account.
"""

# General imports
import os
import datetime
import sys

# Security-related imports
import random
import string
import json
import httplib2

from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

# Server application-related imports
from flask import Flask, render_template, jsonify, request, redirect, \
    url_for

# Database-related imports
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database.database_setup import Base, Categories, Items

# Error handling-related imports
from werkzeug.exceptions import HTTPException
from flask import abort
from sqlalchemy.exc import SQLAlchemyError


__author__ = "Elisabeth M. Strunk"
__version__ = 1.0
__maintainer__ = "Elisabeth M. Strunk"
__email__ = "elisabeth.maria.strunk@gmail.com"
__status__ = "Development"


'''
# CONNECTION TO THE DATABASE
  *  If the database file does not exist yet, create the database and populate 
     it with dummy data.
  *  Open a connection to the database
  *  Define functions that handle the interaction with the database. 
'''
try:
    if not os.path.exists('item_catalog.db'):
        from app.database.database_setup import create_database
        from app.database.populate_database import populate_database

        create_database()
        populate_database()

    engine = create_engine('sqlite:///item_catalog.db',
                           connect_args={'check_same_thread': False})
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
except SQLAlchemyError as e:
    sys.exit("While initializing the database, an error occurred: " + str(e))


def get_categories_from_db():
    return session.query(Categories).all()


def get_latest_items_from_db():
    return session.query(Items).order_by(text("last_modified DESC")).limit(5)


def get_items_from_db(category):
    return session.query(Items).filter_by(category=category)


def get_item_from_db(item_id):
    return session.query(Items).filter_by(id=item_id).one_or_none()


def edit_item_in_db(edited_item):
    session.add(edited_item)
    session.commit()
    return edited_item


def add_item_to_db(item):
    session.add(item)
    session.commit()
    new_item = session.query(Items).filter_by(
        last_modified=item.last_modified).one_or_none()
    return new_item


def delete_item_from_db(item):
    session.delete(item)
    session.commit()
    return None


'''
# WEB APPLICATION
  *  Initialize Flask application and set secret key for security
  *  Set up error handler
  *  Define all routes and their endpoint functions
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)


'''
## Error handling
'''


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('error.html',
                           error_text=str(e).replace(str(code), ''),
                           error_code=code), code


app.config['TRAP_HTTP_EXCEPTIONS'] = True
app.register_error_handler(Exception, handle_error)


'''
## Endpoints with rendered frontend:
'''


@app.route('/')
@app.route('/catalog')
@app.route('/catalog/')
def index():
    categories = get_categories_from_db()
    latest_items = get_latest_items_from_db()
    return render_template('index.html', categories=categories,
                           latest_items=latest_items)


@app.route('/catalog/<string:category>')
@app.route('/catalog/<string:category>/items')
def category(category):
    if category in [c.name for c in get_categories_from_db()]:
        categories = get_categories_from_db()
        items = get_items_from_db(category)
        number_of_items = len(items.all())
        return render_template('category.html', categories=categories,
                               category=category, items=items,
                               number_of_items=number_of_items)
    else:
        abort(404, description="No category found with name "
                               "'{}'.".format(category))


@app.route('/catalog/<string:category>/<string:item_id>')
def item(category, item_id):
    if category not in [c.name for c in get_categories_from_db()]:
        abort(404, description="No category found with name "
                               "'{}'.".format(category))
    item = get_item_from_db(item_id)
    if item:
        if item.category != category:
            abort(404, description="The item you requested was not found "
                                   "in category {}.".format(category))
        else:
            return render_template('item.html', item=item)
    else:
        abort(404, description="No item found with id {}.".format(item_id))


@app.route('/catalog/<string:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    item = get_item_from_db(item_id)
    if request.method == 'GET':
        categories = get_categories_from_db()
        return render_template('edit_item.html', categories=categories,
                               item=item)
    elif request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category = request.form['category']
        item.last_modified = datetime.datetime.now()
        edit_item_in_db(item)
        return redirect(url_for('item', item_id=item_id,
                                category=item.category))
    else:
        abort(405)


@app.route('/catalog/<string:item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    item = get_item_from_db(item_id)
    if request.method == 'GET':
        return render_template('delete_item.html', item=item)
    elif request.method == 'POST':
        delete_item_from_db(item)
        return redirect(url_for('category', category=item.category))
    else:
        abort(405)


@app.route('/catalog/add', methods=['GET', 'POST'])
def add_item():
    if 'username' not in login_session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        categories = get_categories_from_db()
        return render_template('add_item.html', categories=categories)
    elif request.method == 'POST':
        if request.form['name'] and request.form['description'] and \
                request.form['category']:
            item_name = request.form['name']
            item_description = request.form['description']
            item_category = request.form['category']
            new_item = add_item_to_db(
                Items(name=item_name,
                      description=item_description,
                      category=item_category,
                      last_modified=datetime.datetime.now()))
            return redirect(url_for('item', item_id=new_item.id,
                                    category=new_item.category))
        else:
            abort(400, description="The transmitted form data was incomplete. "
                                   "Item not added.")
    else:
        abort(405)


'''
## JSON endpoints:
'''


@app.route('/catalog.json')
def index_json():
    categories = get_categories_from_db()
    serialized_catalog = {}
    for category in categories:
        serialized_catalog.update(
            {category.name: {}}
        )
        serialized_items = []
        for item in get_items_from_db(category.name):
            serialized_items.append(item.serialize)
        serialized_catalog[category.name].update(
            {'Items': serialized_items}
        )
    return jsonify(Catalog=serialized_catalog)


@app.route('/catalog/<string:category>.json')
@app.route('/catalog/<string:category>/items.json')
def category_json(category):
    if category in [c.name for c in get_categories_from_db()]:
        items = get_items_from_db(category)
        number_of_items = len(items.all())
        serialized_items = []
        for item in get_items_from_db(category):
            serialized_items.append(item.serialize)
        serialized_category = {
            'Name': category,
            'Number fo items': number_of_items,
            'Items': serialized_items}
        return jsonify(Category=serialized_category)
    else:
        return jsonify({'message': "No category found with name "
                                   "{}.".format(category)}), 404


@app.route('/catalog/<string:category>/<string:item_id>.json')
def item_in_category_json(category, item_id):
    item = get_item_from_db(item_id)
    if item:
        if item.category != category:
            return jsonify({'message': "The item you requested was not found "
                                       "in category {}.".format(category)}), \
                   404
        else:
            return jsonify(Item=item.serialize)
    else:
        return jsonify({'message': "No item found with id "
                                   "{}.".format(item_id)}), 404


'''
# AUTHENTICATION AND AUTHORIZATION
  It is possible to sign in with either Google or Facebook.
  *  Sign-in related endpoints and functions
  *  Sign-out related endpoints and functions
'''
'''
## Sign-in
'''


@app.route('/login')
def login():
    if login_session.get('provider'):
        # current user is already logged in
        return render_template('login.html',
                               user_found=True,
                               user_name=login_session.get('username'),
                               user_picture=login_session.get('picture'))
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))  # anti-forgery state token
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def google_connect():
    """
    Code of this function adapted from the code provided by Udacity instructor
    Lorenzo Brown at
    https://github.com/udacity/ud330/blob/master/Lesson2/step5/project.py
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        abort(401, description="Login failed. Invalid state parameter.")

    # Obtain authorization code
    code = request.data

    # Upgrade the authorization code into a credentials object
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        abort(401, description="Login failed. Failed to upgrade the "
                               "authorization code.")

    # Check that the access token is valid
    access_token = credentials.access_token
    url = (
        f'https://www.googleapis.com/oauth2/v1/'
        f'tokeninfo?access_token={access_token}')
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort
    if result.get('error'):
        abort(500, description="Login failed. " + result.get('error'))

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        abort(401, description="Login failed. Token's user ID doesn't "
                               "match given user ID.")

    # Verify that the access token is valid for this app
    if result['issued_to'] != json.loads(open('client_secrets.json',
                                              'r').read())['web']['client_id']:
        abort(401, description="Login failed. Token's client ID does not "
                               "match app's.")

    # Check if current user is already signed in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if (stored_access_token is not None) and (gplus_id == stored_gplus_id):
        # user is already connected
        # -> return "old_user" so the frontend can show an appropriate message
        return jsonify({'status': 'old_user', 'content': ''}), 200

    # Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(user_info_url, params=params)
    data = answer.json()

    # Store user data
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # return "new_user" together with the users name and profile picture path,
    # so the frontend can show an appropriate message
    return jsonify({'status': 'new_user',
                    'content': {'username': login_session["username"],
                                'picture': login_session["picture"]}}), 200


@app.route('/fbconnect', methods=['POST'])
def facebook_connect():
    """
    Code of this function adapted from the code provided by Udacity instructor
    Lorenzo Brown at
    https://github.com/udacity/ud330/blob/master/Lesson4/step2/project.py
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        abort(401, description="Login failed. Invalid state parameter.")

    # Obtain access token
    access_token_byte = request.data
    access_token = access_token_byte.decode("utf-8")

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').
                        read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r')
                            .read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?' \
          'grant_type=fb_exchange_token&' \
          f'client_id={app_id}&' \
          f'client_secret={app_secret}&' \
          f'fb_exchange_token={access_token}'
    result = httplib2.Http().request(url, 'GET')[1]
    token = json.loads(result.decode("utf-8"))["access_token"]

    # Store the access token in the session for later use
    login_session['access_token'] = token

    # Get user info
    url = 'https://graph.facebook.com/v2.8/me?' \
          f'access_token={token}&' \
          'fields=name,id,email'
    result = httplib2.Http().request(url, 'GET')[1]
    user_info = json.loads(result.decode("utf-8"))

    # Check if current user is already signed in
    stored_access_token = login_session.get('access_token')
    stored_fb_id = login_session.get('facebook_id')
    if (stored_access_token is not None) and (user_info["id"] == stored_fb_id):
        # user is already connected
        # -> return "old_user" so the frontend can show an appropriate message
        return jsonify({'status': 'old_user', 'content': ''}), 200

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?' \
          f'access_token={token}&' \
          'redirect=0&' \
          'height=200&' \
          'width=200'
    result = httplib2.Http().request(url, 'GET')[1]
    data = json.loads(result)

    # Store user data
    login_session['provider'] = 'facebook'
    login_session['username'] = user_info["name"]
    login_session['email'] = user_info["email"]
    login_session['facebook_id'] = user_info["id"]
    login_session['picture'] = data["data"]["url"]

    # return "new_user" together with the users name and profile picture path,
    # so the frontend can show an appropriate message
    return jsonify({'status': 'new_user',
                    'content': {'username': login_session["username"],
                                'picture': login_session["picture"]}}), 200


@app.route('/is_user_connected')
def check_if_user_connected():
    if login_session.get('provider') is None:
        return jsonify({'status': 'no_user_connected', 'content': ''})
    return jsonify({'status': 'user_connected',
                    'content': {'username': login_session.get("username"),
                                'picture': login_session.get("picture")}}), 200


'''
## Sign-out
'''


@app.route('/disconnect')
def sign_out():
    session_provider = login_session.get('provider')
    if session_provider == 'google':
        return google_disconnect()
    elif session_provider == 'facebook':
        return facebook_disconnect()
    elif session_provider is None:
        return render_template('logout.html',
                               result='Current user not connected.')
    else:
        abort(500, description="An error occurred during sign-out. "
                               f"Session provider unknown.")


def google_disconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        return render_template('logout.html',
                               result='Current user not connected.')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=' \
          '{}'.format(login_session['access_token'])
    result = httplib2.Http().request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['provider']
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return render_template('logout.html',
                               result='You have been successfully '
                                      'disconnected.')
    else:
        abort(500, 'Failed to revoke token for given user.')


def facebook_disconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        return render_template('logout.html',
                               result='Current user not connected.')
    facebook_id = login_session.get('facebook_id')
    url = 'https://graph.facebook.com/{}/permissions?access_token=' \
          '{}'.format(facebook_id, access_token)
    result = httplib2.Http().request(url, 'DELETE')[1]
    data = json.loads(result)
    if data['success'] is True:
        del login_session['provider']
        del login_session['access_token']
        del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return render_template('logout.html',
                               result='You have been successfully '
                                      'disconnected.')
    else:
        abort(500, 'Failed to revoke token for given user.')


'''
# RUN SERVER APPLICATION
'''

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
