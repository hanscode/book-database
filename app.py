from models import Base, engine, session, Book

import datetime
import csv
import time

def menu():
    while True:
        print(
        """
            \nPROGRAMMING BOOKS
            \r1. Add Book
            \r2. View All Books
            \r3. Search for Book
            \r4. Book Analysis
            \r5. Exit""")
        
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input("""
              \rPlease choose one of the options above.
              \rA number from 1 to 5.
              \rPress Enter to try again.""")

# add books to the database
# edit books
# delete books
# search for books
# data cleaning

def clean_date(date_str): #clean_date('January 1, 2020') # it prompts in console: ['January', '1,', '2020']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input("""
              \n====== DATE ERROR ======
              \rThe date format should include a valid month, day, and year.
              \rFor example: 'January 1, 2020'
              \rPress Enter to try again.
              \r==========================""")
        return
    else:
        return  return_date

def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input("""
              \n====== PRICE ERROR ======
              \rThe price should be a number without a currency symbol.
              \rFor example: '10.99'
              \rPress Enter to try again.
              \r==========================""")
        return
    else:
        return int(price_float * 100)

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data= csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title == row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commit()

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # Add Book
            title = input("Title: ")
            author = input("Author: ")
            date_error = True
            while date_error:   
                date = input("Published Date (e.g. January 1, 2020): ")
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input("Price (e.g. 19.99): ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print(f"""
                  \n====== BOOK ADDED ======
                  \rTitle: {title}
                  \rAuthor: {author}
                  \rPublished Date: {date}
                  \rPrice: {price / 100}
                  \r==========================""")
            time.sleep(2)
            
        elif choice == '2':
            # View All Books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.published_date} | ${book.price / 100}')
            input("\nPress Enter to return to the main menu.")
        elif choice == '3':
            # Search for Book
            pass
        elif choice == '4':
            # Book Analysis
            pass
        else:
            # Exit
            print("GOODBYE!")
            app_running = False

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    for book in session.query(Book):
        print(book)