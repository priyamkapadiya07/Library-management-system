import psycopg2
con = psycopg2.connect(host="localhost",port="5432", user="postgres", password="pk", database="library")
if con!=None:
    print("Connected to the database")
    cur=con.cursor()
else:
    print("Not Connected to the database")


'''
CREATE TABLE books (
    bid VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL
);
CREATE TABLE books_issued (
    bid VARCHAR(50) NOT NULL,
    issued_to VARCHAR(100) NOT NULL
);

'''