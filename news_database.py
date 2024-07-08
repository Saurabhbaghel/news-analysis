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
    cmd = 'CREATE TABLE "{}"(url, headline, content, summary, org, sentiment)'
    cur.execute(cmd.format(name))
        
def insert_values_into_table(cur: Cursor, 
                             table_name: str, 
                             values: tuple[dict[str, str | float]]):
    """Inserts the value into the table

    Args:
        cur (Cursor): _description_
        table_name (str): _description_
        values (list[tuple[str, int]]): _description_
    """
    cmd = 'INSERT INTO "{}" VALUES(:url, :headline, :content, :summary, :org, :sentiment)'
    cur.executemany(cmd.format(table_name), values)

    
def store_data_in_db(db_name: str="News.db", table_name: str="Articles", data: tuple[dict[str, str | float]]=None):
    
    # create a db
    con = create_db(db_name)
    
    # get the cursor
    cur = con.cursor()
    
    # table_name = "Articles"
    # Check if the table exists
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="{}"', table_name)
    table_exists = cursor.fetchone()
    
    if table_exists:
        decision = input(f"Table {table_name} already exists. Do you want to overwrite it? y/n: ")

    if decision.lower().strip() == "y":
        # drop the table
        cursor.execute('DROP TABLE "{}"', table_name)
            
        # create table
        create_table(cur, table_name)     
    
    # insert data into the table
    insert_values_into_table(cur, table_name, data)
    
    # commit the data
    con.commit()
    
    # close the connection
    con.close()
    
