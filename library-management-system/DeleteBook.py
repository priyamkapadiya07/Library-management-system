from db_connection import *
issueTable = "books_issued"
bookTable = "books"
class DeleteBook:

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

    def delete_book_record(self, bid):
        try:
            cur.execute("DELETE FROM " + bookTable + " WHERE bid = %s", (bid,))
            con.commit()

            cur.execute("DELETE FROM " + issueTable + " WHERE bid = %s", (bid,))
            con.commit()

            print("Book Record Deleted Successfully")
        except Exception as e:
            con.rollback()
            print("Error: Please check Book ID. Details:", e)

    def get_book_id(self):
        bid = input("Enter Book ID to delete: ")
        return bid

    def delete_book(self):
        if not self.logged_in:
            print("You must be logged in to delete a book.")
            self.login()
        
        if self.logged_in:
            bid = self.get_book_id()
            self.delete_book_record(bid)