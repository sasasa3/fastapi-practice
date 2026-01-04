import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.db import get_db, Base
from api.main import app

# テスト用のインメモリSQLite（メモリ上で動く使い捨てDB）を使う設定

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def async_client() -> AsyncClient:
    # 1. テスト用のDBエンジンを作る
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # 2. テスト用DBの中にテーブルを作る
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 3. DI（依存性注入）を使って、本番のDB接続を「テスト用DB」にすり替える
    async def get_test_db():
        async with async_session() as session:
            yield session

    # アプリの「get_db」を「get_test_db」に強制的に書き換える（オーバーライド）
    app.dependency_overrides[get_db] = get_test_db

    # 4. テスト用のクライアント（ブラウザ代わり）を返す
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client