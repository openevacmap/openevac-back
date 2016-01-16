import psycopg2

import config

db = psycopg2.connect("dbname=%s user=%s" % (config.db_name, config.db_user))
