
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from myproject.models.models import Base

# try:
# 	# Preferred: import as package when run with project root on PYTHONPATH
# 		from myproject.models.models import Base
# 	except ImportError:
# 	# Fallback: when running this file directly, ensure `src` is on sys.path
# 	import os
# 	import sys

# 	src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 	if src_path not in sys.path:
# 		sys.path.insert(0, src_path)

# 	from myproject.models.models import Base


project_root = Path(__file__).resolve().parents[2]
db_path = project_root / "my_project.db"
DATABASE_URL = f"sqlite:///{db_path.as_posix()}"


engine = create_engine(
	DATABASE_URL, connect_args={"check_same_thread": False}, future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
	"""Create database tables based on models' metadata."""
	Base.metadata.create_all(bind=engine)


def get_session():
	"""Yield a database session; remember to close it after use."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


if __name__ == "__main__":
	print("Initializing database and creating tables...")
	init_db()
	print(f"Done. SQLite file created at {db_path}")

