import os
from sqlalchemy import create_engine
from api.models.task import Base

# 同期用のURLも環境変数から取るように変更
DB_URL = os.environ.get("DB_URL", "mysql+pymysql://root@db:3306/demo?charset=utf8")

# Render用：postgres:// を postgresql+psycopg2:// に書き換える
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+psycopg2://", 1)

engine = create_engine(DB_URL, echo=True)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()