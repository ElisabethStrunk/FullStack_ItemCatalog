
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'categories'
    #id = Column(Integer, primary_key=True)
    #name = Column(String(50), nullable=False)
    name = Column(String(50), primary_key=True)


class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    category = Column(Integer, ForeignKey('categories.name'))
    categories = relationship(Categories)
    last_modified = Column(DateTime, nullable=False)


def create_database():
    engine = create_engine('sqlite:///item_catalog.db')
    Base.metadata.create_all(engine)
