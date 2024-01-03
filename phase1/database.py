from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import db_config

SQLALCHEMY_SQLITE_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_PG_DATABASE_URL = db_config.postgresql_path
SQLALCHEMY_MYSQL_DATABASE_URL = db_config.mysql_path

# connect_args only needed for SQLlite, not for other DBs.
# use it to allow multiple threads to connect to DB, not a single thread
# will give each thread its own session explicitly
engine = create_engine(SQLALCHEMY_SQLITE_DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()
