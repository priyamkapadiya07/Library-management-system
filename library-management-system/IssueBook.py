from db_connection import *

issueTable = "books_issued"
bookTable = "books"

class IssueBook:

    def __init__(self):
        self.allBid = []

    def fetch_all_book_ids(self):
        try:
            cur.execute(f"SELECT bid FROM {bookTable}")
            rows = cur.fetchall()
            self.allBid = [i[0] for i in rows]
        except Exception as e:
            print("Error: Can't fetch Book IDs. Details:", e)

    def is_book_available(self, bid):
        try:
            cur.execute(f"SELECT status FROM {bookTable} WHERE bid = %s", (bid,))
            result = cur.fetchone()
            if result:
                return result[0] == 'avail'
            return False
        except Exception as e:
            print("Error: Can't check book status. Details:", e)
            return False
        
    def validate_mobile_number(self, mobile_no):
        if len(mobile_no) != 10 or not mobile_no.isdigit():
            print("Error: Invalid mobile number. Please enter a 10-digit number.")
            return False
        return True

    def issue_book(self, bid, issueto, mobile_no):
        self.fetch_all_book_ids()

        if bid not in self.allBid:
            print("Error: Book ID not found.")
            return

        if not self.is_book_available(bid):
            print("Message: Book Already Issued or Not Available.")
            return
        
        if not self.validate_mobile_number(mobile_no):
            return

        try:
            issue_sql = f"INSERT INTO {issueTable} (bid, issued_to, mobile_no) VALUES (%s, %s, %s)"
            cur.execute(issue_sql, (bid, issueto, mobile_no))
            con.commit()

            update_status = f"UPDATE {bookTable} SET status = 'issued' WHERE bid = %s"
            cur.execute(update_status, (bid,))
            con.commit()

            print('Success: Book Issued Successfully')

        except Exception as e:
            con.rollback()
            print("Error: The value entered is wrong, or something went wrong. Try again. Details:", e)

    def get_book_and_user_info(self):
        bid = input("Enter Book ID: ").strip()
        issueto = input("Enter the name of the person receiving the book: ").strip()
        mobile_no = input("Enter the mobile number of the person receiving the book: ").strip()
        return bid, issueto, mobile_no

    def execute_issue(self):
        bid, issueto, mobile_no = self.get_book_and_user_info()
        self.issue_book(bid, issueto, mobile_no)
