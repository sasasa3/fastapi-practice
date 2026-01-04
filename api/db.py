import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 環境変数 DB_URL があればそれを取得、なければローカルのMySQL設定を使用
ASYNC_DB_URL = os.environ.get("DB_URL", "mysql+aiomysql://root@db:3306/demo?charset=utf8")

# 【重要】RenderなどのPostgreSQL環境への対応
# 環境変数のURLが "postgres://" または "postgresql://" で始まっている場合、
# SQLAlchemyの非同期処理に必要な "postgresql+asyncpg://" に強制的に書き換える
if ASYNC_DB_URL.startswith("postgres://"):
    ASYNC_DB_URL = ASYNC_DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif ASYNC_DB_URL.startswith("postgresql://"):
    ASYNC_DB_URL = ASYNC_DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# エンジンの作成（echo=Trueでログを出力）
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

# セッション作成クラス
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()

# DBセッションを取得する依存関数
async def get_db():
    async with async_session() as session:
        yield session