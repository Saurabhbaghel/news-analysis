import sqlite3
from sqlite3 import Cursor, Connection

def create_db(name: str="news.db"):
    """Creates a Database

    Args:
        name (str, optional): _description_. Defaults to "news.db".

    Returns:
        _type_: _description_
    """
    return sqlite3.connect(name)

def create_table(cur: Cursor, name: str="articles"):
    """Creates Table

    Args:
        cur (Cursor): _description_
        name (str, optional): _description_. Defaults to "articles".
    """
    cmd = 'CREATE TABLE "{}"(headline, url, summary, org, sentiment)'
    cur.execute(cmd.format(name))
        
def insert_values_into_table(cur: Cursor, 
                             table_name: str, 
                             values: list[tuple[str, int]]):
    """Inserts the value into the table

    Args:
        cur (Cursor): _description_
        table_name (str): _description_
        values (list[tuple[str, int]]): _description_
    """
    cmd = 'INSERT INTO "{}" VALUES(?, ?, ?, ?, ?)'
    cur.executemany(cmd.format(table_name), values)

    
def store_data_in_db(data: list[tuple[str]]):
    
    # create a db
    con = create_db("news.db")
    
    # get the cursor
    cur = con.cursor()
    
    table_name = "Articles"
    # create table
    create_table(cur, table_name)
    
    # insert data into the table
    insert_values_into_table(cur, table_name, data)
    
    # commit the data
    con.commit()
    
    # close the connection
    con.close()
    
