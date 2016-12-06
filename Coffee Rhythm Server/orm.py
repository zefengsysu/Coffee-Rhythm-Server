#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import asyncio, logging
logging.basicConfig(filename='app.log', level = logging.INFO)

import aiomysql

def log(sql):
	logging.info('SQL: %s' % sql)

async def create_pool(loop, **kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = await aiomysql.create_pool(
		host = kw.get('host', 'localhost'),
		port = kw.get('port', 3306),
		user = kw['user'],
		password = kw['password'],
		db = kw['db'],
		charset = kw.get('charset', 'utf8'),
		autocommit = kw.get('autocommit', True),
		maxsize = kw.get('maxsize', 10),
		minsize = kw.get('minsize', 1),
		loop = loop
	)

async def select(sql, args, size = None):
	log(sql)
	global __pool
	async with __pool.get() as conn:
		async with conn.cursor(aiomysql.DictCursor) as cur:
			await cur.execute(sql.replace('?', '%s'), args or ())
			if size:
				rs = await cur.fetchmany(size)
			else:
				rs = await cur.fetchall()
		logging.info('rows returned: %s' % len(rs))
		return rs

async def execute(sql, args, autocommit=True):
	log(sql)
	global __pool
	async with __pool.get() as conn:
		if not autocommit:
			await conn.begin()
		try:
			cur = await conn.cursor()
			await cur.execute(sql.replace('?', '%s'), args)
			affected = cur.rowcount
			await cur.close()
			if not autocommit:
				await conn.commit()
		except BaseException as e:
			if not autocommit:
				await conn.rollback()
			raise
		return affected

def create_args_string(num):
	L = []
	for n in range(num):
		L.append('?')
	return ','.join(L)

class Field(object):
	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default

	def __str__(self):
		return '<%s, %s, %s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
	def __init__(self, name=None, column_type='varchar(100)', primary_key=False, default=None):
		super().__init__(name, column_type, primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class DoubleField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'double', primary_key, default)

class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)

class ModelMetaclass(type):
	def __new__(cls, name, bases, attrs):
		# 排除Model类本身
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)
		# 获取table名称
		tableName = attrs.get('__table__', None) or name
		logging.info('found model: %s (table: %s)' % (name, tableName))
		# 获取所有的Field和主键名
		mappings = dict()
		fields = []
		primaryKeys = []
		for k, v in attrs.items():
			if isinstance(v, Field):
				logging.info('found mapping: %s ==> %s' % (k, v))
				mappings[k] = v
				if v.primary_key:
					primaryKeys.append(k)
				else:
					fields.append(k)
		if not primaryKeys:
			raise RuntimeError('Primary key not found.')
		for k in mappings.keys():
			attrs.pop(k)
		escaped_fields = list(map(lambda f: '`%s`' % f, fields))
		escaped_primaryKeys = list(map(lambda pk: '`%s`' % pk, primaryKeys))
		attrs['__mappings__'] = mappings # 保存属性和列的映射关系
		attrs['__table__'] = tableName
		attrs['__primary_keys__'] = primaryKeys # 主键属性名
		attrs['__fields__'] = fields # 除主键外的属性名
		# 构造默认的SELECT, INSERT, UPDATE和DELETE语句
		attrs['__select__'] = 'select * from `%s`' % (tableName, )
		if escaped_fields:
			attrs['__insert__'] = 'insert into `%s` (%s, %s) values (%s)' % (
				tableName, ', '.join(escaped_fields), ', '.join(escaped_primaryKeys), create_args_string(len(escaped_fields) + len(escaped_primaryKeys)))
		else:
			attrs['__insert__'] = 'insert into `%s` (%s) values (%s)' % (
				tableName, ', '.join(escaped_primaryKeys), create_args_string(len(escaped_primaryKeys)))
		attrs['__update__'] = 'update `%s` set %s where %s' % (
			tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), 
			' and '.join(map(lambda pk: '`%s`=?' % (mappings.get(pk).name or pk), primaryKeys)))
		attrs['__delete__'] = 'delete from `%s` where %s' % (
			tableName, ' and '.join(map(lambda pk: '`%s`=?' % (mappings.get(pk).name or pk), primaryKeys)))

		return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise  AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

	def getValue(self, key):
		return getattr(self, key, None)

	def getValueOrDefault(self, key):
		value = getattr(self, key, None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default value for %s: %s' % (key, str(value)))
				setattr(self, key, value)
		return value

	@classmethod
	async def findAll(cls, where=None, args=None, **kw):
		' find objects by where clause. '
		sql = [cls.__select__]
		if where:
			sql.append('where')
			sql.append(where)
		if args is None:
			args = []
		orderBy = kw.get('orderBy', None)
		if orderBy:
			sql.append('order by')
			sql.append(orderBy)
		limit = kw.get('limit', None)
		if limit is not None:
			sql.append('limit')
			if isinstance(limit, int):
				sql.append('?')
				args.append(limit)
			elif isinstance(limit, tuple) and len(limit) == 2:
				sql.append('?, ?')
				args.extend(limit)
			else:
				raise ValueError('Invalid limit value: %s' % str(limit))
		rs = await select(' '.join(sql), args)
		return [cls(**r) for r in rs]

	@classmethod
	async def findNumber(cls, selectField, where=None, args=None):
		' find number by select and where. '
		sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
		if where:
			sql.append('where')
			sql.append(where)
		rs = await select(' '.join(sql), args, 1)
		if len(rs) == 0:
			return None
		return rs[0]['_num_']

	@classmethod
	async def find(cls, pk): # pk -> []
		' find object by primary key. '
		rs = await select('%s where %s' % (cls.__select__, ' and '.join(map(lambda pk: '`%s`=?' % (cls.__mappings__.get(pk).name or pk), cls.__primary_keys__))), pk, 1)
		if len(rs) == 0:
			return None
		return cls(**rs[0])

	async def save(self):
		args = list(map(self.getValueOrDefault, self.__fields__))
		args += list(map(self.getValueOrDefault, self.__primary_keys__))
		rows = await execute(self.__insert__, args)
		if rows != 1:
			logging.warn('failed to insert record: affected rows: %s' % rows)

	async def update(self):
		args = list(map(self.getValue, self.__fields__))
		args += list(map(self.getValue, self.__primary_keys__))
		rows = await execute(self.__update__, args)
		if rows != 1:
			logging.warn('failed to update by primary key: affected rows: %s' % rows)

	async def remove(self):
		args = []
		for primaryKey in self.__primary_keys__:
			args += self.getValue(primaryKey)
		rows = await execute(self.__delete__, args)
		if rows != 1:
			logging.warn('failed to remove by primary key: affected rows: %s' % rows)
