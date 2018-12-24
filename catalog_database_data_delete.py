from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, Category, Item, LatestItem

engine = create_engine('sqlite:///catalogitems.db')
DBsession = sessionmaker(bind=engine)
session = DBsession()

items = session.query(Item).all()
for item in items:
    session.delete(item)
    session.commit()

categories = session.query(Category).all()
for category in categories:
    session.delete(category)
    session.commit()

latest_items = session.query(LatestItem).all()
for latest_item in latest_items:
    session.delete(latest_item)
    session.commit()

print ("All the data in 'Item' , 'Category' and "
       "'LatestItem' tables have been deleted!")
