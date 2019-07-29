#!/usr/bin/env python3
"""
Item Catalog

TODO: write description
"""

from flask import Flask, Blueprint, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database_setup import Base, Categories, Items

__author__ = "Elisabeth M. Strunk"
__version__ = 1.0
__maintainer__ = "Elisabeth M. Strunk"
__email__ = "elisabeth.maria.strunk@gmail.com"
__status__ = "Development"


app = Flask(__name__)

engine = create_engine('sqlite:///item_catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()


@app.route('/')
@app.route('/catalog/<string:category>/items')
@app.route('/catalog/<string:category>/<string:item_id>')
@app.route('/catalog/<string:item_id>/edit')
@app.route('/catalog/<string:item_id>/delete')
@app.route('/catalog.json')
def show_categories():
    print("CALLED!!")
    categories = session.query(Categories).all()
    return render_template('index.html', categories=categories)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
