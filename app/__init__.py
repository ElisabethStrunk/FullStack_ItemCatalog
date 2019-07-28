

def configure_app():
    import os

    from flask import Blueprint, Flask

    main_blueprint = Blueprint('main_blueprint', __name__,
                               template_folder='templates')
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    app.config['SECRET_KEY'] = os.urandom(16)
    return app


def open_db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from .database_setup import Base, Categories, Items

    engine = create_engine('sqlite:///item_catalog.db')
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session
