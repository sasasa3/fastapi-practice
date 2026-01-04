import pytest
from httpx import AsyncClient

# 1. 作成と読み取りのテスト
@pytest.mark.asyncio
async def test_create_and_read(async_client: AsyncClient):
    # 新規作成 (POST)
    response = await async_client.post("/tasks", json={"title": "テストタスク"})
    assert response.status_code == 200
    response_obj = response.json()
    assert response_obj["title"] == "テストタスク"

    # 一覧取得 (GET)
    response = await async_client.get("/tasks")
    assert response.status_code == 200
    response_obj = response.json()
    assert len(response_obj) == 1
    assert response_obj[0]["title"] == "テストタスク"
    assert response_obj[0]["done"] is False

# 2. 完了フラグ（Done）の切り替えテスト
@pytest.mark.asyncio
async def test_done_flag(async_client: AsyncClient):
    # 準備: テスト用のタスクを1つ作る
    response = await async_client.post("/tasks", json={"title": "完了テスト"})
    task_id = response.json()["id"]

    # アクション1: 完了にする (PUT /done)
    response = await async_client.put(f"/tasks/{task_id}/done")
    assert response.status_code == 200

    # チェック: 本当に完了(true)になったか？
    response = await async_client.get("/tasks")
    assert response.json()[0]["done"] is True

    # アクション2: 未完了に戻す (DELETE /done)
    response = await async_client.delete(f"/tasks/{task_id}/done")
    assert response.status_code == 200

    # チェック: 本当に未完了(false)に戻ったか？
    response = await async_client.get("/tasks")
    assert response.json()[0]["done"] is False

# 3. 編集と削除のテスト
@pytest.mark.asyncio
async def test_update_and_delete(async_client: AsyncClient):
    # 準備: テスト用のタスクを作る
    response = await async_client.post("/tasks", json={"title": "変更前のタイトル"})
    task_id = response.json()["id"]

    # アクション1: タイトルを変更する (PUT)
    response = await async_client.put(f"/tasks/{task_id}", json={"title": "変更後のタイトル"})
    assert response.status_code == 200

    # チェック: タイトルが変わったか？
    response = await async_client.get("/tasks")
    assert response.json()[0]["title"] == "変更後のタイトル"

    # アクション2: 削除する (DELETE)
    response = await async_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # チェック: 本当に消えたか？（リストが空になっているはず）
    response = await async_client.get("/tasks")
    assert len(response.json()) == 0