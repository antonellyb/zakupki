zakupki
=======

Zakupki (закупки) is my personal project. The purpose of the project is research of data that the Russian government provides on government procurement. Right now it is a single `Python` script (in multiple files) that loads the data (zipped `XML` at `ftp://free:free@ftp.zakupki.gov.ru/`) into `MongoDB`. `MongoDB` is used because the data is too irregular for relational databases.

Usage
-----

```sh
update.py <all|inc>
	[-H --mongodb-host, -P --mongodb-port]
	[-mu --mongodb-user, -mp --mongodb-password]
	[-U --mongdo-uri]
	[-c --contracts,  -p --products, -o --organizations]
```

First argument is the type of update.
* `all` does full update - drops collections and loads all available data.
* `inc` does incremental update. It searches maximum publish date in the corresponding collection (by region, if the data is divided this way) and loads the data that is published since that max date. If there is no data in the corresponding document group, `inc` loads all available date.

If you have no data in your `MongoDB`, there's no difference between `all` and `inc`.

You can also provide host address and port if your `MongoDB` is not running on `localhost`. And username-password if you `MongoDB` uses authentication.

OR

you can provide full URI instead. It can be necessary when connecting to SaaS MongDB. For example, the URI can be as follows.
'mongodb://user:pass@host:port/db'

The other arguments are collections to load. If the user provides no additional arguments, all available document types are loaded.

Examples:
```sh
# load all data on products (OKDP classification) to the local mongodb
# (no authentication)
python update.py all -p

# make an incremental update of all available data on server `x.x.x.x`, port `15146`,
# username `putin` and password `medvedev`
python update.py inc -H x.x.x.x -P 15146 -mu putin -mp medvedev
```

Dependencies
------------

The script runs on `Python 2.7` and has two dependencies: `lxml` and `pymongo`.

To install `lxml`:
```sh
apt-get install python-dev libxml2-dev libxslt-dev
pip install lxml
```

To install `pymongo`:
```sh
pip install pymongo
```

And, of course, you have to install `MongoDB`. Current version of the script requires `mongodb-10gen` version `2.4.6`, you can find installation instructions (for Linux Ubuntu) here:
http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

If you are short on time, just run this to install the latest version:
```sh
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get install mongodb-10gen
```

Info
----

You can find information about document contents and FTP server folder structure as well as basic document search at http://zakupki.gov.ru/ the official website.

Additional info on the the script structure can be found in my (rather poor) comments.

This is the file I strongly relied on in parsing XML (Russian, from the same website):
https://www.dropbox.com/s/sq54tv9zl38ojah/%D0%90%D0%BB%D1%8C%D0%B1%D0%BE%D0%BC%2B%D0%A2%D0%A4%D0%A4_0.0.21.0.pdf