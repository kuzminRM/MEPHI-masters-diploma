from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = 'workflow_bot'
    POSTGRES_ECHO: bool = False

    QUADRANT_HOST: str = 'localhost'
    QUADRANT_PORT: int = 6333

    @property
    def POSTGRES_CONNECTION_STRING_BASE(self) -> str:
        """SQLAlchemyБез имени базы данных (POSTGRES_DB)"""
        return (
            f'postgresql+psycopg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}'
        )

    @property
    def POSTGRES_CONNECTION_STRING(self) -> str:
        return f'{self.POSTGRES_CONNECTION_STRING_BASE}/{self.POSTGRES_DB}'

    @property
    def QUADRANT_CONNECTION_STRING(self) -> str:
        return f'http://{self.QUADRANT_HOST}:{self.QUADRANT_PORT}'


settings = Settings(_env_file='/home/roman/PycharmProjects/personal/diploma/.env')  # type: ignore[call-arg]
