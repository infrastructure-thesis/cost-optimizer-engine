from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/cost_optimizer"
    AWS_REGION: str = "eu-west-1"
    LOG_LEVEL: str = "INFO"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        
settings = Settings()
