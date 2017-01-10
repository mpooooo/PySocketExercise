#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import sqlite3
from db_config import *

user_db_section = "user_db"
user_db_path_key = "path"
user_db_table_create = 'table_create'
user_db_fetch = 'fetch'
user_db_insert = 'insert'

def getUserDataBasePath():
    return getConfig(user_db_section, user_db_path_key)

def createUserTable(connection):
    create_table_sql = getConfig(user_db_section, user_db_table_create)
    return executeWithSql(connection, create_table_sql)

def fetchOneFromUser(conn, col, key):
    fetch_sql = getConfig(user_db_section, user_db_fetch)%( col, key)
    print fetch_sql
    if fetch_sql is not None and fetch_sql != '':
        cu = getCursor(conn)
        cu.execute(fetch_sql)
        return cu.fetchone()
    else:
        print('the [{}] is empty or equal None!'.format(sql)) 

def fetchAllFromUser(conn, col, key):
    fetch_sql = getConfig(user_db_section, user_db_fetch)%( col, key)
    print fetch_sql
    if fetch_sql is not None and fetch_sql != '':
        cu = getCursor(conn)
        cu.execute(fetch_sql)
        return cu.fetchall()
    else:
        print('the [{}] is empty or equal None!'.format(sql)) 

def insertUser(connection, user_id, use_nick_name, user_register_time, user_last_online_time, 
                user_online_time, user_pass_word):
    insert_sql = (getConfig(user_db_section, user_db_insert))%(user_id, use_nick_name, user_register_time,
                  user_last_online_time, user_online_time, user_pass_word)
    if insert_sql is not None and insert_sql != '':
        cu = getCursor(connection)
        cu.execute(insert_sql)
        connection.commit()
        closeCursor(cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))
        return False
    return True

def getConnection(db_path):
    conn = sqlite3.connect(db_path)
    if os.path.exists(db_path) and os.path.isfile(db_path):
        return conn
    else:
        conn = None
        return sqlite3.connect(':memory:')

def getCursor(connection):
    connection.row_factory = dict_factory
    if connection is not None:
        return connection.cursor()
    else:
        return getConnection('').cursor()

def fetchWithSql(connection, sql):
    if sql is not None and sql != '':
        cu = getCursor(connection)
        cu.execute(sql)
        return cu.fetchall()
    else:
        print('the [{}] is empty or equal None!'.format(sql)) 

def executeWithSql(connection, sql):
    if sql is not None and sql != '':
        cur = getCursor(connection)
        cur.execute(sql)
        connection.commit()
        closeCursor(cur)
        return True
    else:
        print('the [{}] is empty or equal None!'.format(sql))
        return False

def closeCursor(cursor):
    if cursor is not None:
        cursor.close()

def closeConnection(connection):
    if connection is not None:
        connection.close()

def closeAll(connection, cu):
    try:
        if cu is not None:
            cu.close()
    finally:
        if connection is not None:
            connection.close()

def dict_factory(cursor, row): 
  d = {} 
  for idx, col in enumerate(cursor.description): 
    d[col[0]] = row[idx] 
  return d

if __name__ == '__main__':
    path = getUserDataBasePath()
    print path
    cnn = getConnection(path)
    print cnn
    createUserTable(cnn)
    print fetchAllFromUser(cnn, '*')