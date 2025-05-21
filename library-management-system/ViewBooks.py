import os
from db_connection import *
import matplotlib.pyplot as plt
import numpy as np
# import pywhatkit as kit
from fpdf import FPDF
# from PIL import Image
from twilio.rest import Client

bookTable = "books"

class ViewBook:

    def __init__(self):
        pass

    def fetch_books(self):
        try:
            cur.execute(f"SELECT * FROM {bookTable} ORDER BY BID")
            return cur.fetchall()  
        except Exception as e:
            print(f"Error: Failed to fetch books from database. Details: {e}")
            return None

    def display_books(self, books):
        if books:
            print("%-10s%-40s%-30s%-20s" % ('BID', 'Title', 'Author', 'Status'))
            print("----------------------------------------------------------------------------")
            for book in books:
                print("%-10s%-40s%-30s%-20s" % (book[0], book[1], book[2], book[3]))
                self.show_summary(book[0])
        else:
            print("No books to display.")
        q=input("Do you want to show books category distributions (yes/no) : ")
        if (q.lower()=='yes'):
            self.display_pie_chart()

    def show_summary(self, book_id):
        summary_file_path = r"book_summaries" + "\\" + f"{book_id}.txt"
        
        if os.path.exists(summary_file_path):
            try:
                with open(summary_file_path, 'r') as file:
                    summary = file.read()  
                    print("\nSummary :")
                    print(summary)
            except Exception as e:
                print(f"Error reading summary file for book {book_id}. Details: {e}")
        else:
            print(f"No summary available for book ID {book_id}.")
        
        print("----------------------------------------------------------------------------")

    def view_books(self):
        books = self.fetch_books()
        self.display_books(books)

    def fetch_category_data(self):
        try:
            cur.execute("""
                SELECT LEFT(bid, 2) AS category, COUNT(*) AS book_count
                FROM books
                GROUP BY LEFT(bid, 2)
                ORDER BY category;
            """)
            return cur.fetchall()
        except Exception as e:
            print(f"Error: Failed to fetch category data. Details: {e}")
            return None

    def display_pie_chart(self):
        category_data = self.fetch_category_data()
        
        if category_data:
            categories = np.array([row[0] for row in category_data])
            book_counts = np.array([row[1] for row in category_data])

            plt.figure(figsize=(7, 7))
            plt.pie(book_counts, labels=categories, autopct=lambda p: f'{int(p * np.sum(book_counts) / 100)}', startangle=90, explode=[0,0.1,0,0],shadow=True)
            plt.title('Book Categories Distribution')
            plt.axis('equal')
            plt.legend(['js:javascript','jv:java','py:python','sh:self-help'], title="Categories", loc="best")
            plt.show()
        else:
            print("No category data available to display in pie chart.")
    
    def create_pdf_report(self, books, category_data, filename="book_report.pdf"):
        # Create a PDF document
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Set title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt="Books Report", ln=True, align='C')
        pdf.ln(10)

        # Set table headers
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(25, 10, 'BID', border=1)
        pdf.cell(90, 10, 'Title', border=1)
        pdf.cell(50, 10, 'Author', border=1)
        pdf.cell(25, 10, 'Status', border=1)
        pdf.ln()

        # Add table rows
        pdf.set_font('Arial', '', 12)
        for book in books:
            pdf.cell(25, 10, str(book[0]), border=1)
            pdf.cell(90, 10, book[1], border=1)
            pdf.cell(50, 10, book[2], border=1)
            pdf.cell(25, 10, book[3], border=1)
            pdf.ln()

        pdf.ln(10)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, txt="Category Distribution Pie Chart", ln=True, align='C')
        
        # Save Pie Chart as an image
        categories = np.array([row[0] for row in category_data])
        book_counts = np.array([row[1] for row in category_data])

        # plt.figure(figsize=(7, 7))
        plt.pie(book_counts, labels=categories, autopct=lambda p: f'{int(p * np.sum(book_counts) / 100)}', startangle=90, explode=[0, 0.1, 0, 0], shadow=True)
        plt.title('Book Categories Distribution')
        plt.axis('equal')
        plt.legend(['js:javascript','jv:java','py:python','sh:self-help'], title="Categories", loc="best")
        chart_image_path = "book_categories_distribution.png"
        plt.savefig(chart_image_path)
        plt.close()

        # Add pie chart image to PDF
        pdf.ln(10)
        pdf.image(chart_image_path, x=60, w=90)

        # Output the PDF to a file
        pdf.output(filename)

        # Clean up the chart image
        os.remove(chart_image_path)

    def generate_PDF(self):
        books = self.fetch_books()
        category_data = self.fetch_category_data()

        if books and category_data:
            self.create_pdf_report(books, category_data)
        else:
            print("Error: Could not fetch the data for the report.")