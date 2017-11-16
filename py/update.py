import argparse
from ftplib import FTP
from pymongo import MongoClient
import traceback

from etl import *
from utils import *

'''
	This is the main script that provides the
	functionality.
	
	conf dict is a configuration.

	For each possible document type it provides
	FTP connection to use and an ETL function to
	execute.

	ETL functions contain the higher-level logic
	that depends on FTP folder structure and
	document type.

	These functions call lower-level functions
	such as extract() function that loads
	the file from FTP server, unzips it and
	returns a file-like object.

	That object is parsed with etree.iterparse
	(memory-efficient and fast), and for each
	document in XML file transform_*() is called
	that takes XML-etree object and returns the
	corresponding dict.

	Dicts are then inserted (or upserted) into
	the database with load() function.

	All ETL functions are stored in etl.py,
	transform_*() functions are in transform.py,
	all the other are in utils.py.
'''
conf = {
	# 'notifications': {
	# 	'etl': notifications_etl,
	# 	'ftp': FTP('ftp.zakupki.gov.ru', 'free', 'free')
	# },
	'contracts': {
		'etl': contracts_etl,
		'ftp': ('ftp.zakupki.gov.ru', 'free', 'free')
	},
	'products': {
		'etl': products_etl,
		'ftp': ('ftp.zakupki.gov.ru', 'anonymous', None)
	},
	'organizations': {
		'etl': organizations_etl,
		'ftp': ('ftp.zakupki.gov.ru', 'anonymous', None)
	}
}

if __name__ == '__main__':
	# collect arguments
	parser = argparse.ArgumentParser(description='Update zakupki database.')
	'''
		 The first argument is for update type:
		 'all' means wipe database and load all data again,
		 'inc' means load data that is absent in the db.

		 The second and third arguments are for MongoDB authentication.
		 If provided, the script uses auth, if your database uses no
		 authentication, just ommit them.

		 The other arguments are one per collection in mongodb
		 or per document type on the source FTP server.
	'''
	parser.add_argument(choices=['all', 'inc'], dest='type', action='store')
	parser.add_argument('-H', '--mongodb-host', dest='host', action='store', default='127.0.0.1')
	parser.add_argument('-P', '--mongodb-port', dest='port', action='store', default=27017, type=int)
	parser.add_argument('-mu', '--mongodb-user', dest='user', action='store')
	parser.add_argument('-mp', '--mongodb-password', dest='passwd', action='store')
	parser.add_argument('-U', '--mongodb-uri', dest='uri', action='store')	
	
	# parser.add_argument('-n', '--notifications', dest='collections', action='append_const', const='notifications')
	parser.add_argument('-c', '--contracts', dest='collections', action='append_const', const='contracts')
	parser.add_argument('-p', '--products', dest='collections', action='append_const', const='products')
	parser.add_argument('-o', '--organizations', dest='collections', action='append_const', const='organizations')
	args = parser.parse_args()
	if not args.collections: # if no collections provided, use all
		args.collections = ['contracts', 'products', 'organizations']

	print ts(), 'Starting {type} update'.format(type=args.type)
	print ts(), 'Connecting mongodb'
	if args.uri:
	    client = MongoClient(args.uri)
	else:
	    client = MongoClient(args.host, args.port)

	db = client.zakupki

	if args.user and args.passwd: # if user provides auth credentials, authenticate
		try:
			db.authenticate(args.user, args.passwd)
		except:
			print 'MongoDB authentication failed!\nMake sure your MongoDB uses authentication and this user exists.'
			# traceback.print_exc()
			exit()

	for coll in args.collections:
		print ts(), 'Updating {coll}'.format(coll=coll)
		collection = db[coll]
		if args.type == 'all':
			db[coll + '_meta'].drop() # drop metadata
			collection.drop()
		print ts(), 'Connecting FTP'
		ftp = FTP(conf[coll]['ftp'][0], conf[coll]['ftp'][1], conf[coll]['ftp'][2])
		conf[coll]['etl'](ftp, collection, args.type)
		ftp.close()
	client.close()