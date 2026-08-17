import os
import sys

import pytest

# ensure src is on sys.path so `myproject` package can be imported
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from myproject.models.models import Base


@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def db(db_engine):
    Session = sessionmaker(bind=db_engine, future=True)
    session = Session()
    try:
        yield session
    finally:
        session.close()
