from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        database_url = os.getenv("DATABASE_URL_LOCAL")
        self._engine = create_engine(database_url)
        self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @property
    def engine(self):
        return self._engine

    @property
    def SessionLocal(self):
        return self._session_local

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


database_session = DatabaseSession()
engine = database_session.engine
SessionLocal = database_session.SessionLocal
get_db = database_session.get_db
