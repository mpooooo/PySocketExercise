#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys
import sqlite3
class SqliteInterface(object):

	''' the api interface for python sqlite3'''
	
	def __init__(self, db_path):
		self.data_base_path = db_path
		self.connection = None
		self.cursor = None
		self._sql_templates_init()

	def connectDataBase(self):
		conn = sqlite3.connect(self.data_base_path, check_same_thread=False)
		if os.path.exists(self.data_base_path) and os.path.isfile(self.data_base_path):
			self.connection = conn
		else:
			conn = None
			self.connection = sqlite3.connect(':memory:',  check_same_thread=False)

	def getConnection(self):
		return self.connection

	def getCursor(self):
	    self.connection.row_factory = self._dictFactory
	    if self.connection is not None:
	        return self.connection.cursor()

	def closeConnection(self):
	    if self.connection is not None:
	        self.connection.close()
	
	def closeCursor(self, cursor):
		if cursor is not None:
			cursor.close()

	def fetchOne(self, table_name, condition_tuple_list, ret_col = ['*']):
		condition_lst = []
		for tple in condition_tuple_list:
			key = tple[0]
			condition = tple[1]
			value = tple[2]
			if type(value) == type(str()):
				value = '\'' + value + '\''
			link = tple[3]
			condition_lst.extend([key, condition, value, link])
		condition_sql = ''.join(condition_lst[0: len(condition_lst)-1])
		col_lst = []
		for col in ret_col:
			col_lst.append(col)
			col_lst.append(',')
		ret_sql = ''.join(col_lst[0: len(col_lst)-1])
		fetch_sql = self._fetch_template%(ret_sql, condition_sql)
		#print fetch_sql
		ret_code, ret_data = True, None
		try:
			cu = self.getCursor()
			cu.execute(fetch_sql)
			ret_data = cu.fetchone()
			self.closeCursor(cu)
		except sqlite3.Error:
			ret_code = False
		if ret_data is None:
			ret_code = False
		return ret_code, ret_data

	def fetchAll(self, table_name, condition_tuple_list, ret_col = ['*']):
		condition_lst = []
		for tple in condition_tuple_list:
			key = tple[0]
			condition = tple[1]
			value = tple[2]
			if type(value) == type(str()):
				value = '\'' + value + '\''
			link = tple[3]
			condition_lst.extend([key, condition, value, link])
		condition_sql = ''.join(condition_lst[0: len(condition_lst)-1])
		ret_lst = []
		for col in ret_col:
			col_lst.append(col)
			col_lst.append(',')
		ret_sql = ''.join(col_lst[0: len(col_lst)-1])
		fetch_sql = self._fetch_template%(ret_sql, condition_sql)
		ret_code, ret_data = True, None
		try:
			cu = self.getCursor()
			cu.execute(fetch_sql)
			ret_data = cu.fetchone()
			self.closeCursor(cu)
		except sqlite3.Error:
			ret_code = False
		if ret_data is None:
			ret_code = False
		return ret_code, ret_data

	def createTable(self, table_name, col_type_dict):
		col_tpe_sql_list = []
		for col, tpe in col_type_dict.items():
			col_tpe_sql_list.append(col)
			col_tpe_sql_list.append(' ')
			col_tpe_sql_list.append(tpe)
			col_tpe_sql_list.append(',')
		col_tpe_sql = ''.join(map(str, col_tpe_sql_list[0: len(col_tpe_sql_list)-1]))
		create_table_sql = self._create_table_template%(table_name, col_tpe_sql)
		#print create_table_sql
		try:
			cur = self.getCursor()
			cur.execute(create_table_sql)
			self.connection.commit()
			self.closeCursor(cur)
			return True
		except sqlite3.OperationalError:
			return False

	def update(self, table_name, update_tuple_lst, condition_tuple_list):
		condition_lst = []
		for tple in condition_tuple_list:
			key = tple[0]
			condition = tple[1]
			value = tple[2]
			if type(value) == type(str()):
				value = '\'' + value + '\''
			link = tple[3]
			condition_lst.extend([key, condition, value, link])
		condition_sql = ''.join(condition_lst[0: len(condition_lst)-1])
		kv_list = []
		for key, value in update_tuple_lst:
			kv_list.extend([key, '='])
			if type(value) == type(str()):
				value = '\'' + value + '\''
			kv_list.extend([value, ','])
		kv_sql = ''.join(map(str, kv_list[0: len(kv_list)-1]))
		update_sql = self._update_template%(table_name, kv_sql, condition_sql)
		#print update_sql
		try:
			cu = self.getCursor()
			cu.execute(update_sql)
			self.connection.commit()
			self.closeCursor(cu)
			return True
		except sqlite3.OperationalError, e:
			#print e
			return False


	def insert(self, table_name, cols_list, values_list):
		col_sql_list = []
		for col in cols_list:
			col_sql_list.append(col)
			col_sql_list.append(',')
		col_sql = ''.join(map(str,col_sql_list[0: len(col_sql_list)-1]))

		value_sql_list = []
		for val in values_list:
			if type(val) == type(str()):
				val = '\'' + val + '\''
			value_sql_list.append(val)
			value_sql_list.append(',')
		value_sql = ''.join(map(str,value_sql_list[0: len(value_sql_list)-1]))
		insert_sql = self._insert_template%(table_name, col_sql, value_sql)
		#print insert_sql
		#try:
		cu = self.getCursor()
		cu.execute(insert_sql)
		self.connection.commit()
		self.closeCursor(cu)
		return True
	#except:
	#		return False

	def _sql_templates_init(self):
		self._create_table_template = 'create table if not exists %s (%s)'
		self._fetch_template = 'select %s from User where %s'
		self._insert_template = 'insert into %s (%s) VALUES (%s)'
		self._update_template = 'update %s set %s where %s '

	def _dictFactory(self, cursor, row): 
		d = {} 
		for idx, col in enumerate(cursor.description): 
			d[col[0]] = row[idx] 
		return d