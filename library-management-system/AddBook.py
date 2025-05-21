from db_connection import *

class AddBook:

    def __init__(self):
        self.logged_in = False

    def login(self):
        default_username = "pripanlib"
        default_password = "20_1"

        username = input("Enter Username: ")
        password = input("Enter Password: ")

        if username == default_username and password == default_password:
            self.logged_in = True
            print("\nLogin successful!\n")
        else:
            print("Error: Invalid username or password. Access denied.")
            self.logged_in = False

    def get_book_info(self):
        bid = input("Enter Book ID: ")
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        
        status = 'avail'
        
        return bid, title, author, status

    def book_register(self, bid, title, author, status):
        try:
            cur.execute("INSERT INTO books (bid, title, author, status) VALUES (%s, %s, %s, %s)", 
                        (bid, title, author, status))
            con.commit()
            print("Book added successfully")
        except Exception as e:
            con.rollback()
            print("Error: Can't add data into Database", e)
    
    def add_book(self):
        if not self.logged_in:
            print("You must be logged in to add a book.")
            self.login()
        
        if self.logged_in:
            bid, title, author, status = self.get_book_info()
            self.book_register(bid, title, author, status)