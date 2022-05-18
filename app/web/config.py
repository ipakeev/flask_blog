from dataclasses import dataclass


@dataclass
class Config:
    SECRET_KEY: str
    DATABASE_URI: str
