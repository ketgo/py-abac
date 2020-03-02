import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.event import listens_for
from sqlalchemy.exc import OperationalError
from sqlalchemy.pool import Pool

DEFAULT_SQL_HOST = "sqlite:///:memory:"


# Needed for switching on case sensitive LIKE statements on Sqlite
@listens_for(Pool, 'connect')
def run_on_connect(dbapi_con, connection_record):
    try:
        dbapi_con.execute('pragma case_sensitive_like=ON')
    except:  # pragma: no cover
        pass  # pragma: no cover


def create_test_sql_engine():
    url = os.getenv('SQL_HOST', DEFAULT_SQL_HOST)
    engine = create_engine(url, encoding='utf-8')
    try:
        engine.execute(text('select 1'))
    except OperationalError as e:  # pragma: no cover
        pytest.exit('SQL_DATABASE_URL is not correct. Error: %s' % e)  # pragma: no cover
    return engine  # pragma: no cover
