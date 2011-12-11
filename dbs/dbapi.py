import MySQLdb
import json

EMAIL_PRIORITY_LOW    = 3
EMAIL_PRIORITY_MEDIUM = 2
EMAIL_PRIORITY_HIGH   = 1

#def open_db(dbserver, dbname, dbuser, dbpwd):
#	return MySQLdb.connect(host=dbserver, user=dbuser, passwd=dbpwd, db=dbname)
def open_db(dbname):
	return MySQLdb.connect(db=dbname)

def close_db(db):
	db.close()

""" Base class of DB tables """
class DBObj:
	@classmethod
	def insert_one_by_value(self, cursor, *args):
		""" Insert one record to the table
		*args: values of every column in the same order as defined
		"""
		values = ",".join(['"'+str(r)+'"' for r in args])
		cursor.execute("REPLACE INTO {0} ({1}) VALUES ({2})".format(self.table_name, self.cols, values))

	@classmethod
	def insert_one_by_names(self, cursor, **kwargs):
		cols = []
		for k,v in kwargs.iteritems():
			cols.append("=".join([str(k), '"'+str(v)+'"']))
		values = ",".join(cols)
		cursor.execute("REPLACE INTO {0} SET {1}".format(self.table_name, values))

	@classmethod
	def update_status_by_id(cls, cursor, id, newstatus):
		"""
		update records
		"""
		print "UPDATE {0} SET status = '{1}' WHERE id = {2}".format(cls.table_name, newstatus, id)
		cursor.execute("UPDATE {0} SET status = '{1}' WHERE id = {2}".format(cls.table_name, newstatus, id))


	def insert_a_batch(self, cursor, records):
		""" Insert a batch of records to the table
		    recods: a list of records.
	            each record is a list of columns in the same order as defined
		    """
		for r in records:
			self.insert_one_by_value(cursor, *r)

	@classmethod
	def fetch_by(self, cursor, cols, limit=0, *args):
		""" cols: columns to fetch
		    args: select conditions
	        """
		cols = ",".join(cols)
		cmd = "SELECT {0} FROM {1}".format(cols, self.table_name)
		print "---" , args
		if args:
			clause = " AND ".join(args)
			cmd += " WHERE {0}".format(clause)
		if limit != 0:
			cmd += " LIMIT {0}".format(limit)
		print "+++", cmd
		cursor.execute(cmd)
		return cursor.fetchall()

	@classmethod
	def commit(self, cursor):
		return cursor.execute("COMMIT")

	@classmethod
	def import_from_json(self, cursor, inputfile):
		with open(inputfile) as input:
			for line in input:
				data = json.loads(line)
				record = []
				for c in cols_names:
					record.append(data[c])
				self.insert_one_by_value(cursor, *record)

class Email(DBObj):
	table_name = "email"
	cols_names = ["address", "biz_id", "last_contacted", "priority", "domain"]
	cols = ",".join(cols_names)

class Business(DBObj):
	table_name = "business"
	cols_names = ["name", "url", "phone", "category", "location", "status", "owner", "domain"]
	cols = ",".join(cols_names)


class EmailList(DBObj):
	table_name = "emaillist"
	cols_names = ["address", "domain"]
	cols = ",".join(cols_names)


