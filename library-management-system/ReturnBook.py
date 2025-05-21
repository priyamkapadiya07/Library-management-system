from db_connection import *

issueTable = "books_issued" 
bookTable = "books"         

class ReturnBook:

    def __init__(self):
        self.allBid = []

    def fetch_all_issued_book_ids(self):
        try:
            cur.execute(f"SELECT bid FROM {issueTable}")
            rows = cur.fetchall()
            self.allBid = [i[0] for i in rows]
        except Exception as e:
            print(f"Error: Can't fetch Book IDs from {issueTable}. Details: {e}")

    def is_book_issued(self, bid):
        try:
            cur.execute(f"SELECT status FROM {bookTable} WHERE bid = %s", (bid,))
            result = cur.fetchone()
            if result:
                return result[0] == 'issued'
            return False
        except Exception as e:
            print(f"Error: Can't check book status for {bid}. Details: {e}")
            return False

    def return_book(self, bid):
        self.fetch_all_issued_book_ids()

        if bid not in self.allBid:
            print("Error: Book ID not found in issued books.")
            return

        if not self.is_book_issued(bid):
            print("Message: Book is not currently issued.")
            return

        try:
            issue_sql = f"DELETE FROM {issueTable} WHERE bid = %s"
            cur.execute(issue_sql, (bid,))
            con.commit()

            update_status = f"UPDATE {bookTable} SET status = 'avail' WHERE bid = %s"
            cur.execute(update_status, (bid,))
            con.commit()

            print("Success: Book Returned Successfully")
        except Exception as e:
            con.rollback()
            print(f"Error: An issue occurred while returning the book. Details: {e}")

        self.allBid.clear()

    def get_book_id(self):
        bid = input("Enter Book ID to return: ").strip()
        return bid

    def execute_return(self):
        bid = self.get_book_id()
        self.return_book(bid)