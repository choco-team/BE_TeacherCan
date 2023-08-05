from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

user = "can"
pwd = "1234" # 특수기호 전처리
host = "3.34.99.98"
port = "53866" # 구름 ide 에서 가져오기
db_url = f'mysql+pymysql://{user}:{pwd}@{host}:{quote(port)}/teachercan'

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
