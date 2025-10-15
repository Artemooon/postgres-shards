from uhashring import HashRing

from db_connection import db_configs

db_hr = HashRing(nodes=list(db_configs.keys()))
