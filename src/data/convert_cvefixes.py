import gzip 
import sqlite3
import os


# ---Decompress the .gz file using gzip and create .db file using sqlite3---
db_path = os.path.join('data','raw','CVEfixes.db')
gz_path = os.path.join('data','raw','CVEfixes_v1.0.8.sql.gz')
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with gzip.open(gz_path, 'rt',encoding='utf-8') as f:
        sql_statement = ""
        line_count = 0 
        
        for line in f:
            if line.startswith('--'):
                continue
            
            sql_statement+=line
            
            if sqlite3.complete_statement(sql_statement):
                try:
                    cursor.execute(sql_statement)
                except sqlite3.Error:
                    pass
                
                sql_statement = ""
            
            line_count+=1
                
            
            if line_count % 100000 == 0:
                print(f"Processing... {line_count} lines have been processed so far")
    
    print("File conversion completed successfully without consuming RAM.")                
    
    conn.commit()
    conn.close()

except Exception as e:
    print(f"An error occurred during execution: {e}")
