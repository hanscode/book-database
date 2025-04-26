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

def submenu():
    while True:
        print(
        """
            \n1. Edit
            \r2. Delete
            \r3. Return to Main Menu""")
        
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input("""
              \rPlease choose one of the options above.
              \rA number from 1 to 3.
              \rPress Enter to try again.""")

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

def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input("""
              \n====== ID ERROR ======
              \rThe id should be a number.
              \rPress Enter to try again.
              \r==========================""")
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f"""
                  \n====== ID ERROR ======
                  \rThe id {book_id} is not in the database.
                  \rPlease choose one of the following ids: {options}
                  \rPress Enter to try again.
                  \r==========================""")
            return


def edit_check(column_name, current_value):
    print(f"\n====== EDIT {column_name} ======")
    if column_name == 'Price':
        print(f"\rCurrent Value: {current_value / 100}")
    elif column_name == 'Date':
        print(f"\rCurrent Value: {current_value.strftime('%B %d, %Y')}")
    else:
        print(f"\rCurrent Value: {current_value}")

    if column_name == "Date" or column_name == "Price":
        while True:
            changes = input("What would you like to change the value to? ")
            if column_name == "Date":
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == "Price":
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input("What would you like to change the value to? ")

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
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
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            
            id_error = True
            while id_error:
                id_choice = input(f"""
                    \nId Options: {id_options}
                    \rBook id: """)
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id == id_choice).first()
            print(f"""
                  \n====== BOOK FOUND ======
                  \rTitle: {the_book.title}
                  \rAuthor: {the_book.author}
                  \rPublished Date: {the_book.published_date}
                  \rPrice: ${the_book.price / 100}
                  \r==========================""")
            sub_choice = submenu()
            if sub_choice == '1':
                # Edit Book 
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check('Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                #print(session.dirty)
                session.commit()
                print('Book Updated Successfully!')
                time.sleep(2)
            
            elif sub_choice == '2':
                # Delete Book 
                session.delete(the_book)
                session.commit()
                print('Book Deleted!')
                time.sleep(2)
            
        elif choice == '4':
            # Book Analysis
            oldest_book = session.query(Book).order_by(Book.published_date).first()
            newest_book = session.query(Book).order_by(Book.published_date.desc()).first()
            total_books = session.query(Book).count()
            python_books = session.query(Book).filter(Book.title.like('%Python%')).count()
    
            print(f"""
                  \n====== BOOK ANALYSIS ======
                  \rOldest Book: {oldest_book.title} | {oldest_book.published_date}
                  \rNewest Book: {newest_book.title} | {newest_book.published_date}
                  \rTotal Books: {total_books}
                  \rNumber of Python Books: {python_books}
                  \r==========================""")
            time.sleep(2)
            input("\nPress Enter to return to the main menu.")
        else:
            # Exit
            print("GOODBYE!")
            app_running = False

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for book in session.query(Book):
    #     print(book)