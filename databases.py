from model import Base, User

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_user(name,secret_word):
    """Add a user to the DB."""
    user = User(username=name)
    user.hash_password(secret_word)
    session.add(user)
    session.commit()

def get_user(username):
    """Find the first user in the DB, by their username."""
    return session.query(User).filter_by(username=username).first()

def edit_food(username, food):
	get_user(username).fav_food = food
	session.commit()

def edit_path(username, path):
	get_user(username).pic_path = path
	session.commit()