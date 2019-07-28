#!/usr/bin/env python3
"""
Item Catalog

TODO: write description
"""

from flask import render_template

from app.database_setup import Categories, Items
from app import configure_app, open_db_session

__author__ = "Elisabeth M. Strunk"
__version__ = 1.0
__maintainer__ = "Elisabeth M. Strunk"
__email__ = "elisabeth.maria.strunk@gmail.com"
__status__ = "Development"


# Initialise app
app = configure_app()


@app.route('/')
@app.route('/categories')
def show_categories():
    session = open_db_session()
    print("CALLED!!")
    categories = session.query(Categories).all()
    return render_template('base.html', categories=categories)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
