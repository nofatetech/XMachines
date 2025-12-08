from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MACHINE_UUID: str           # e.g. "xc-07"
    MACHINE_NAME: str = "XCar"
    DB_URL: str                 # postgresql://user:pass@192.168.1.10/vehiclegotchi
    IS_LEADER: bool = False     # only one car serves the web dashboard

    class Config:
        env_file = ".env"

settings = Settings()