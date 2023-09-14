import sqlite3
import json
from main.store import get_stores_for_le

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
    sql_create_table = """CREATE TABLE IF NOT EXISTS usernames(email PRIMARY KEY, user NOT NULL, role NOT NULL, description NOT NULL);"""
    _execute_sql(sql_create_table, False)
    sql_insert_user = "INSERT INTO usernames VALUES ('" + email + "', '" + user + "', '" + role + "', '" + description + "');"
    _execute_sql(sql_insert_user, False)
    print("user added")

# function to validate login details and retrieve lemId
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



# def delete_table():
#     sql_delete_table = "DROP TABLE stores"
#     _execute_sql(sql_delete_table, False)

def force_create_table():
    sql_create_table = """CREATE TABLE business(business_line PRIMARY KEY, lem_id NOT NULL, data NOT NULL);"""
    _execute_sql(sql_create_table, False)

# function to insert business lines association into the database table
def insert_business(business_line, lem_id, data):
    sql_insert_business = "INSERT INTO business VALUES ('" + business_line + "', '" + lem_id + "', '" + data + "');"
    _execute_sql(sql_insert_business, False)

def get_business(lem_id):
    sql_get_business = """SELECT business_line FROM business WHERE lem_id = ?"""
    try:
        conn = sqlite3.connect(_path_to_db_file)
        cursor = conn.cursor()
        print("Connected to SQLite")
        cursor.execute(sql_get_business, (lem_id,))
        businessIds = cursor.fetchall()
        print("Printing lem_id ", lem_id)
        print(businessIds)
        business = businessIds[0][0]
        print(business)
        # businessList = []
        # allBusiness = []
        # for businessArray in businessIds:
        #     business = businessArray[0]
        #     result = get_bl_for_le(business)
        #     businessList.append(result)
        #     print("BusinessID:\n"+ business)
        #     print(result)
        #     businessResult = json.loads(result)
        #     storeName = businessResult['reference']
        #     storeStatus = businessResult['status']
        #     storeObj = {"storeName": storeName, "storeId":store, "status":storeStatus}
        #     print(businessResult['reference'])
        #     allStores.append(storeObj)
        #     print(allStores)
        cursor.close()
        return business
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

# function to insert stores association into the database table
def insert_store(store_id, lem_id, reference):
    sql_insert_store = "INSERT INTO stores VALUES ('" + store_id + "', '" + lem_id + "', '" + reference + "');"
    _execute_sql(sql_insert_store, False)

# function to validate login details and retrieve lemId
def get_stores(lem_id):
    sql_get_stores = """SELECT store_id FROM stores WHERE lem_id = ?"""
    sql_get_reference = """SELECT reference FROM stores WHERE store_id = ?"""
    try:
        conn = sqlite3.connect(_path_to_db_file)
        cursor = conn.cursor()
        print("Connected to SQLite")
        cursor.execute(sql_get_stores, (lem_id,))
        storeIds = cursor.fetchall()
        print("Printing lem_id ", lem_id)
        print(storeIds)
        storesList = []
        allStores = []
        for storeArray in storeIds:
            store = storeArray[0]
            cursor.execute(sql_get_reference, (store,))
            referenceFetch = cursor.fetchall()
            reference = referenceFetch[0][0]
            # result = get_stores_for_le(store)
            storeObj = {"storeId": store, "storeName": reference}
            # storesList.append(result)
            print("StoreID:\n"+ store)
            print(storeObj)
            # storeResult = json.loads(result)
            # storeName = storeResult['reference']
            # storeStatus = storeResult['status']
            # storeObj = {"storeName": storeName, "storeId":store, "status":storeStatus}
            # print(storeResult['reference'])
            allStores.append(storeObj)
            print(allStores)
        cursor.close()
        return allStores
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


