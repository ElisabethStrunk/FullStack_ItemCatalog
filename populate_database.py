
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database_setup import Base, Categories, Items

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

soccer_category = Categories(name='Soccer')
basketball_category = Categories(name='Basketball')

# create:
session.add_all([Categories(name='Soccer'),
                 Categories(name='Basketball'),
                 Categories(name='Baseball'),
                 Categories(name='Frisbee'),
                 Categories(name='Snowboarding'),
                 Categories(name='Rock Climbing'),
                 Categories(name='Foosball'),
                 Categories(name='Skating'),
                 Categories(name='Hockey')])
session.commit()
session.close()
