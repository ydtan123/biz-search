import MySQLdb
import json

EMAIL_PRIORITY_LOW    = 3
EMAIL_PRIORITY_MEDIUM = 2
EMAIL_PRIORITY_HIGH   = 1

def open_db(dbname):
	return MySQLdb.connect(db=dbname)

""" Base class of DB tables """
class DBObj:
	@classmethod
	def insert_one_by_value(self, cursor, *args):
		""" Insert one record to the table
		*args: values of every column in the same order as defined
		"""
		values = ",".join(['"'+str(r)+'"' for r in args])
		print "INSERT INTO {0} ({1}) VALUES ({2})".format(self.table_name, self.cols, values)
		cursor.execute("INSERT INTO {0} ({1}) VALUES ({2})".format(self.table_name, self.cols, values))

	@classmethod
	def insert_one_by_names(self, cursor, **kwargs):
		values = ",".join( "=".join([str(k), v]) for k,v in kwargs )
		cursor.execute("INSERT INTO {0} SET {1}".format(self.table_name, values))

	@classmethod
	def insert_a_batch(self, cursor, records):
		""" Insert a batch of records to the table
		    recods: a list of records.
	            each record is a list of columns in the same order as defined
		    """
		for r in records:
			self.insert_one_by_value(cursor, *r)

	@classmethod
	def fetch_by(self, cursor, cols, **kwargs):
		where = []
		print kwargs
		for k,v in kwargs.iteritems():
			where.append('{0}="{1}"'.format(k, str(v)))
		cols = ",".join(cols) 
		clause = " AND ".join(where)
		cursor.execute("SELECT {0} FROM {1} WHERE {2}".format(cols, self.table_name, clause))  
		return cursor.fetchall()

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
	cols_names = ["address", "biz_id", "last_contacted", "priority"]
	cols = ",".join(cols_names)
		
class Business(DBObj):
	table_name = "business"
	cols_names = ["name", "url", "phone", "category", "country", "status", "owner"]
	cols = ",".join(cols_names)

	
