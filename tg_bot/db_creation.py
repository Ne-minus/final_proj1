import sqlite3
import pandas as pd

con = sqlite3.connect('server_folder/results.db')  # подключение
cur = con.cursor()

cur.execute("""
CREATE TABLE compete_res (
    user_id INT,
    status INT,
    user_ok INT,
    model_ok INT,
    uwins INT, 
    uloses INT, 
    uequals INT,
    PRIMARY KEY (user_id)
)
""")
