from db_connection import *
from AddBook import AddBook
from DeleteBook import DeleteBook
from ViewBooks import ViewBook
from IssueBook import IssueBook
from ReturnBook import ReturnBook
from EmailSender import EmailSender

class LibraryManagementSystem:

    def __init__(self):
        self.add_book = AddBook()
        self.delete_book = DeleteBook()
        self.view_books = ViewBook()
        self.issue_book = IssueBook()
        self.return_book = ReturnBook()
        self.email_sender = EmailSender()

    def show_menu(self):
        # print("\nPress 1 for Add Books")
        # print("Press 2 for Delete Books")
        # print("Press 3 for View Books")
        # print("Press 4 for Issue Books")
        # print("Press 5 for Return Books")
        # print("Press 6 for Exit")
        print("                 ----------------------------------------------------------------------")
        print("                 | ------------------------------------------------------------------  |")
        print("                 | |                    *📚 LIBRARY MANAGEMENT 📚*                   | |")
        print("                 | |                                                                 | |")
        print("                 | |     1.  Add Books                                               | |")
        print("                 | |                                                                 | |")
        print("                 | |     2.  Delete Books                                            | |")
        print("                 | |                                                                 | |")
        print("                 | |     3.  View Books                                              | |")
        print("                 | |                                                                 | |")
        print("                 | |     4.  Issue Books                                             | |")
        print("                 | |                                                                 | |")
        print("                 | |     5.  Return Books                                            | |")
        print("                 | |                                                                 | |")
        print("                 | |     6.  Send PDF via Email                                      | |")
        print("                 | |                                                                 | |")
        print("                 | |     7.  Exit                                                    | |")
        print("                 | |                                                                 | |")
        print("                 | ------------------------------------------------------------------  |")
        print("                 ----------------------------------------------------------------------")

    def handle_choice(self, choice):
        try:
            if choice == 1:
                self.add_book.add_book()
            elif choice == 2:
                self.delete_book.delete_book()
            elif choice == 3:
                self.view_books.view_books()
            elif choice == 4:
                self.issue_book.execute_issue()
            elif choice == 5:
                self.return_book.execute_return()
            elif choice == 6:
                self.view_books.generate_PDF()
                self.email_sender.send_email()
            elif choice == 7:
                cur.close()
                con.close()
                print("\n-------------------------------------------------------------------------------------")
                print("| Thank you for using the Library Management System!                                |")
                print("| Your reading journey is important to us, and we hope we helped make it easier.    |")
                print("| Have a wonderful day, and we look forward to seeing you again soon!               |")
                print("| Happy reading! 📚                                                                 |")
                print("-------------------------------------------------------------------------------------\n")
                return False
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return True

    def run(self):
        while True:
            self.show_menu()
            choice = input("\nEnter your choice: ")
            
            if choice.isdigit() and int(choice) in range(1, 7):
                choice = int(choice)
                if not self.handle_choice(choice):
                    break
            else:
                print("Invalid choice. Please enter a number between 1 to 6.")

if __name__ == "__main__":
    library_system = LibraryManagementSystem()
    library_system.run()
