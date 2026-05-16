import sqlite3
from tabulate import tabulate
import os

#--------------Explore the structure of the CVEfixes dataset and how it is organized----------- 

db_path = os.path.join('data','raw','CVEfixes.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'               
""") 

tables = cursor.fetchall() 

print("\nDatabase Tables:\n")

print(
    tabulate(
        tables,
        headers = ['Table Name'],
        tablefmt="fancy_grid"
    )
)

cursor.execute("PRAGMA table_info(method_change)")

columns = cursor.fetchall()

print("\nmethod_change Table Schema:\n")

print(
    tabulate(
        columns,
        headers=[
            "CID",
            "Column Name",
            "Data Type",
            "Not Null",
            "Default Value",
            "Primary Key"
        ],
        tablefmt="fancy_grid"
    )
)


cursor.execute("""
SELECT code
FROM method_change
WHERE before_change = 'True'
LIMIT 1         
""")

before_change = cursor.fetchall()

cursor.execute("""
SELECT code
FROM method_change
WHERE before_change = 'False'
LIMIT 1         
""")

after_change = cursor.fetchall()

print("=== BEFORE CHANGE ===")
print(tabulate(before_change, headers=["code"], tablefmt="grid"))

print("\n=== AFTER CHANGE ===")
print(tabulate(after_change, headers=["code"], tablefmt="grid"))
