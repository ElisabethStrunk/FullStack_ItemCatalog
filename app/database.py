
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, Items

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()
soccer_category = Categories(name='Soccer')
basketball_category = Categories(name='Basketball')

# create:
session.add_all([soccer_category, basketball_category])
session.commit()

# read:
for category in session.query(Categories).all():
    print(category.name, category.id)
print("---------------------------")

# update:
category_id = 1
session.query(Categories).filter(Categories.id == category_id).update(
    {"name": "Modified Category"}, synchronize_session='fetch')
session.commit()

for category in session.query(Categories).all():
    print(category.name, category.id)
print("---------------------------")

# delete:
session.query(Categories).filter(Categories.id == category_id).\
    delete(synchronize_session='fetch')
session.commit()

for category in session.query(Categories).all():
    print(category.name, category.id)
