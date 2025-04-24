from models import Base, engine, Session, Book

# import models
# main menu - add, search, anylysis, exit, view
# add books to the database
# edit books
# delete books
# search for books
# data cleaning
# loop runs program

if __name__ == "__main__":
    Base.metadata.create_all(engine)