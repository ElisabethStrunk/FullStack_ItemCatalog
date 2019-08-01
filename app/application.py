#!/usr/bin/env python3
"""
Item Catalog

TODO: write description
"""

import os
import datetime

from flask import Flask, render_template, jsonify, request, redirect, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database_setup import Base, Categories, Items


__author__ = "Elisabeth M. Strunk"
__version__ = 1.0
__maintainer__ = "Elisabeth M. Strunk"
__email__ = "elisabeth.maria.strunk@gmail.com"
__status__ = "Development"


if not os.path.exists('item_catalog.db'):
    from app.database_setup import create_database
    from app.populate_database import populate_database

    create_database()
    populate_database()

engine = create_engine('sqlite:///item_catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()


def get_categories():
    return session.query(Categories).all()


def get_latest_items():
    return session.query(Items).order_by(text("last_modified DESC")).limit(5)


def get_items(category):
    return session.query(Items).filter_by(category=category)


def get_item(item_id):
    return session.query(Items).filter_by(id=item_id).one()


app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def index():
    categories = get_categories()
    latest_items = get_latest_items()
    return render_template('index.html', categories=categories,
                           latest_items=latest_items)


@app.route('/catalog/<string:category>')
@app.route('/catalog/<string:category>/items')
def category(category):
    categories = get_categories()
    items = get_items(category)
    number_of_items = len(items.all())
    return render_template('category.html', categories=categories,
                           category=category, items=items,
                           number_of_items=number_of_items)


@app.route('/catalog/<string:category>/<string:item_id>')
def item(category, item_id):
    item = get_item(item_id)
    if item:
        if item.category != category:
            return jsonify({'message': "The item you requested was not found "
                                       "in category {}!".format(category)}), \
                   404
        else:
            return render_template('item.html', item=item)
    else:
        return jsonify({'message': "No item found with id "
                                   "{}!".format(item_id)}), 404


@app.route('/catalog/<string:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    item = get_item(item_id)
    if request.method == 'GET':
        categories = get_categories()
        return render_template('edit_item.html', categories=categories,
                               item=item)
    elif request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category = request.form['category']
        session.add(item)
        session.commit()
        return redirect(url_for('item', item_id=item_id,
                                category=item.category))
    else:
        return 405


@app.route('/catalog/<string:item_id>/delete', methods=['GET', 'POST'])
def delete_item(item_id):
    item = get_item(item_id)
    if request.method == 'GET':
        return render_template('delete_item.html', item=item)
    elif request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('category', category=item.category))
    else:
        return 405


@app.route('/catalog/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'GET':
        categories = get_categories()
        return render_template('add_item.html', categories=categories)
    elif request.method == 'POST':
        if request.form['name']:
            item_name = request.form['name']
        if request.form['description']:
            item_description = request.form['description']
        if request.form['category']:
            item_category = request.form['category']
        time = datetime.datetime.now()
        session.add(Items(name=item_name, description=item_description,
                          category=item_category,
                          last_modified=time))
        session.commit()
        item = session.query(Items).filter_by(last_modified=time).one()
        return redirect(url_for('item', item_id=item.id,
                                category=item.category))
    else:
        return 405


'''
JSON endpoints:
'''


@app.route('/catalog.json')
def index_json():
    categories = get_categories()
    serialized_catalog = {}
    for category in categories:
        serialized_catalog.update(
            {category.name: {}}
        )
        serialized_items = []
        for item in get_items(category.name):
            serialized_items.append(item.serialize)
        serialized_catalog[category.name].update(
            {'Items': serialized_items}
        )
    return jsonify(Catalog=serialized_catalog)


@app.route('/catalog/<string:category>.json')
@app.route('/catalog/<string:category>/items.json')
def category_json(category):
    items = get_items(category)
    number_of_items = len(items.all())
    serialized_items = []
    for item in get_items(category):
        serialized_items.append(item.serialize)
    serialized_category = {
        'Name': category,
        'Number fo items': number_of_items,
        'Items': serialized_items}
    return jsonify(Category=serialized_category)


@app.route('/catalog/<string:category>/<string:item_id>.json')
def item_in_category_json(category, item_id):
    item = get_item(item_id)
    if item:
        if item.category != category:
            return jsonify({'message': "The item you requested was not found "
                                       "in category {}!".format(category)}), \
                   404
        else:
            return jsonify(Item=item.serialize)
    else:
        return jsonify({'message': "No item found with id "
                                   "{}!".format(item_id)}), 404


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
