"""
Database Configurations
"""
import json
from from_root import from_root
import sqlalchemy
from sqlalchemy import create_engine

params = {}

with open(from_root('secret.json'), 'r') as c:
    params = json.loads(c.read())


def init_connection_engine():
    db_config = {
        "pool_recycle": 31535999,
    }
    return init_tcp_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    engine = create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=params['db_user'],
            password=params['db_pass'],
            host=params['db_host'],
            port=params['db_port'],
            database=params['db_name'],
        ),
        **db_config
    )

    return engine
