class dev():
    DEBUG = True
    SECRET_KEY = "KSJFNIE23423+-/smdfsd"
    DATABASE = {
        'name' : './db.db',
        'engine' : 'peewee.SqliteDatabase'
    }

class prod():
    DEBUG = False
    SECRET_KEY = 'sjkfdnsKJNDKS+-/smdfsd'
    DATABASE = {
        'name': 'db.sqlite3',
        'engine': 'peewee.SqliteDatabase'
    }