import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base

db_url = str(os.getenv('DB_URL'))
engine = create_engine(db_url)

POSTGRES_INDEXES_NAMING_CONVENTION = {
    'ix': '%(column_0_label)s_idx',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': '%(table_name)s_%(constraint_name)s_check',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

Base = declarative_base(metadata=metadata)
Base.metadata.create_all(engine)
