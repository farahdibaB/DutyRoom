import sqlite3
import json


# location of SQLite database file
_path_to_db_file = None


# function to set path to database file
def set_path_to_db_file(path_to_db_file):
    global _path_to_db_file
    _path_to_db_file = path_to_db_file

#function to execute an SQL statement
def _execute_sql(sql, read):
    with sqlite3.connect(_path_to_db_file) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        if read == 'true':
            output = cursor.fetchall()
            print(output)
            return output
        cursor.close()

# function to create database table
def create_table():
    sql_create_table = """CREATE TABLE users(username PRIMARY KEY, password NOT NULL, lem_id NOT NULL);"""
    _execute_sql(sql_create_table)
    # create also table for stores
    sql_create_table = """CREATE TABLE stores(store_id PRIMARY KEY, lem_id NOT NULL, reference NOT NULL);"""
    _execute_sql(sql_create_table, False)
    # create also table for businessLines
    sql_create_table = """CREATE TABLE business(business_line PRIMARY KEY, lem_id NOT NULL, data NOT NULL);"""
    _execute_sql(sql_create_table, False)

# function to insert a user into the database table
def insert_user(user, email, role, description):
    conn = sqlite3.connect(_path_to_db_file)
    cursor = conn.cursor()
    sql_create_table = """CREATE TABLE IF NOT EXISTS usernames(email PRIMARY KEY, user NOT NULL, role NOT NULL, description NOT NULL);"""
    # _execute_sql(sql_create_table, False)
    cursor.execute(sql_create_table)
    sql_insert_user = """INSERT INTO usernames (email, user, role, description) VALUES (?, ?, ?, ?)"""
    cursor.execute(sql_insert_user, (email, user, role, description))
    conn.commit()
    conn.close()
    print("user added")

# function to validate details 
def get_data():
    sql_create_table = """CREATE TABLE IF NOT EXISTS usernames(email PRIMARY KEY, user NOT NULL, role NOT NULL, description NOT NULL);"""
    _execute_sql(sql_create_table, False)
    sql_get_user = "SELECT * FROM usernames"
    read = 'true'
    listData = _execute_sql(sql_get_user, read)
    print(listData)
    return listData

def force_delete_table():
    sql_delete_table = "DROP TABLE usernames"
    _execute_sql(sql_delete_table, False)

def delete_user(email):
    try:
        conn = sqlite3.connect(_path_to_db_file)
        cursor = conn.cursor()
        print("Connected to SQLite")
        sql_delete_user = """DELETE FROM usernames WHERE email = ?"""
        cursor.execute(sql_delete_user, (email,))
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")




