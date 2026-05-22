from app.repositories.sidpol_repository import SIDPOLRepository


class RepositoryFactory:
    @staticmethod
    def create(repository_name: str, db_session):
        """Factory simple para instanciar repositorios por nombre."""
        if repository_name == "sidpol":
            return SIDPOLRepository(db_session)
        raise ValueError(f"Repositorio desconocido: {repository_name}")
