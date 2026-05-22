# PC2 Desarrollo de software

### Alumno: Jharvy Jonas Cadillo Tarazona

Este repositorio se implementa 3 patrones de creacion, como se menciona en el univirtual. El proyecto original esta en el siguiente link [Repositorio](https://github.com/S4feR0ute/safe-route)

# Patron singleton

Se implemento el patron singleton en el script `session.py`, para que pueda ser utilizado globalmente como una unica instancia, como se muestra:

``` python
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
```

# Patron Builder

Se implemento el patron builder en el script `crime_stats_builder.py`, para que crear objetos paso a paso, como se muestra:

``` python
from app.models.crime_stats import DistrictCrimeStats


class CrimeStatsBuilder:
    def __init__(self):
        self._data = {
            "district_ubigeo": None,
            "district_name": None,
            "total_incidents_count": 0,
            "violent_incidents_count": 0,
            "weighted_crime_rate": 0.0,
        }

    def with_ubigeo(self, ubigeo: str):
        self._data["district_ubigeo"] = ubigeo
        return self

    def with_name(self, name: str):
        self._data["district_name"] = name
        return self

    def with_total_incidents(self, total: int):
        self._data["total_incidents_count"] = total
        return self

    def with_weighted_rate(self, rate: float):
        self._data["weighted_crime_rate"] = rate
        return self

    def with_violent_incidents(self, violent_count: int):
        self._data["violent_incidents_count"] = violent_count
        return self

    def build(self) -> DistrictCrimeStats:
        return DistrictCrimeStats(
            district_ubigeo=self._data["district_ubigeo"],
            district_name=self._data["district_name"],
            total_incidents_count=self._data["total_incidents_count"],
            violent_incidents_count=self._data["violent_incidents_count"],
            weighted_crime_rate=self._data["weighted_crime_rate"],
        )
```

Se utiliza en el script `crime_analytics_services.py`, para crear un objeto.

``` python
...

    def update_stats_table(self, stats_df):
        """Limpia y actualiza la tabla de estadísticas procesadas."""
        self.db.query(DistrictCrimeStats).delete()
        
        for _, row in stats_df.iterrows():
            stat_entry = CrimeStatsBuilder() \
                .with_ubigeo(row['district_ubigeo']) \
                .with_name(row['district_name']) \
                .with_total_incidents(int(row['total_all'])) \
                .with_violent_incidents(int(row['total_violent'])) \
                .with_weighted_rate(float(row['final_rate'])) \
                .build()
            self.db.add(stat_entry)
        
        self.db.commit()
```

# Patron Faactory

Se implemento el patron Factory en el script `repository_factory.py`, para encapsular la creacion de los repositorios y devolver oobjetos sin mostrar la logica de creacion, como se muestra:

``` python
from app.repositories.sidpol_repository import SIDPOLRepository


class RepositoryFactory:
    @staticmethod
    def create(repository_name: str, db_session):
        """Factory simple para instanciar repositorios por nombre."""
        if repository_name == "sidpol":
            return SIDPOLRepository(db_session)
        raise ValueError(f"Repositorio desconocido: {repository_name}")
```