import sqlite3
from datetime import date


def create_table_config():

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    sql_query_create = """CREATE TABLE config_bot (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key_bot TEXT NOT NULL
    );"""

    cursor.execute(sql_query_create)
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def create_table_deposit():
    
    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    sql_query_create = """CREATE TABLE deposit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date_deposit TEXT NOT NULL,
        amount_ton INTEGER NOT NULL,
        price_ton INTEGER NOT NULL,
        total_price INTEGER NOT NULL
    );"""

    cursor.execute(sql_query_create)
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def drop_deposit():

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    query_drop = """DROP TABLE deposit"""
    cursor.execute(query_drop)
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def create_table_total_ton():

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    sql_query_create = """CREATE TABLE total_ton (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_ton INTEGER NOT NULL
    )"""

    cursor.execute(sql_query_create)
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def drop_total_ton():

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    query_drop = """DROP TABLE total_ton"""
    cursor.execute(query_drop)
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def drop_config():

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()
    query_drop = """DROP TABLE config_bot"""
    cursor.execute(query_drop)
    sql_conn.commit()
    cursor.close()
    sql_conn.close()


def select_amount_ton(user_id):

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    query_select_amount = """SELECT * FROM total_ton WHERE user_id=?"""
    cursor.execute(query_select_amount, (user_id,))
    result = cursor.fetchall()
    sql_conn.commit()
    cursor.close()
    sql_conn.close()
    
    return result

def update_total_ton(user_id, total_ton):
    
    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    update_query = """UPDATE total_ton SET total_ton = ? WHERE user_id = ?"""
    cursor.execute(update_query, (total_ton, user_id,))
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def insert_total_ton(user_id, total_ton):

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    query_insert_total_ton = """INSERT INTO total_ton(user_id, total_ton) VALUES (?, ?)"""

    cursor.execute(query_insert_total_ton, (user_id, total_ton,))
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def create_table_user_id():

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    sql_query_create = """CREATE TABLE user_id (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL
        );"""

    cursor.execute(sql_query_create)
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def select_user_id(user_id):

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    sql_select_id = """SELECT * FROM user_id WHERE user_id = ?"""
    cursor.execute(sql_select_id, (user_id,))
    select_user_id = cursor.fetchone()

    if select_user_id == None:
        sql_insert_id = """INSERT INTO user_id(user_id) VALUES(?)"""
        cursor.execute(sql_insert_id, (user_id,))
        sql_conn.commit()
        cursor.close()
        sql_conn.close()
        return 0
    elif select_user_id[1] == user_id:
        return 1

    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def insert_deposit(user_id, date_deposit, amount_ton, price_ton, total_price):

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    sql_query_insert = """INSERT INTO deposit(user_id, date_deposit, amount_ton, price_ton, total_price) VALUES(?, ?, ?, ?, ?);"""

    cursor.execute(sql_query_insert, (user_id, date_deposit, amount_ton, price_ton, total_price))
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def insert_first_deposit(user_id, date_deposit, amount_ton, price_ton, total_price):

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    query_add_first_dep = """INSERT INTO deposit(user_id, date_deposit, amount_ton, price_ton, total_price) VALUES(?, ?, ?, ?, ?);"""

    cursor.execute(query_add_first_dep, (user_id, date_deposit, amount_ton, price_ton, total_price))
    sql_conn.commit()
    cursor.close()
    sql_conn.close()

def select_deposit(user_id):

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    sql_select_deposit = """SELECT * FROM deposit WHERE user_id=?"""
    cursor.execute(sql_select_deposit, (user_id,))
    deposit = cursor.fetchall()
    #print(deposit)

    sql_conn.commit()
    cursor.close()
    sql_conn.close()

    return deposit

def select_api_key():

    sql_conn = sqlite3.connect('database.db')
    cursor = sql_conn.cursor()

    query_api_select = """SELECT * FROM config_bot WHERE id=1"""

    cursor.execute(query_api_select)
    api_key = cursor.fetchall()

    sql_conn.commit()
    cursor.close()
    sql_conn.close()

    return api_key[0][1]
