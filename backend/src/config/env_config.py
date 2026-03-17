from pydantic_settings import BaseSettings
from typing import List
class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY:str
    AZURE_OPENAI_ENDPOINT:str
    AZURE_OPENAI_API_VERSION:str
    AZURE_DEPLOYMENT_NAME:str
    TAVILY_API_KEY:str
    DATABASE_URL:str
    JWT_SECRET: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DEFAULT_ROLE:str="user"
    ALLOWED_ROLES:List[str]=[DEFAULT_ROLE,"admin"]

    PORT:int=8000
    

    class Config:
        env_file=r".env"
        env_file_encoding="utf-8"
        extra="ignore"

settings=Settings()

    