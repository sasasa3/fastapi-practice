from typing import List
from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession  

import api.schemas.task as task_schema
import api.cruds.task as task_crud  # ← CRUD（DB操作担当）を読み込む
from api.db import get_db  # ← DB接続用関数（電話回線）を読み込む

router = APIRouter()

# 1. 一覧取得（GET）
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):  # ← DB接続をもらう
    # ダミーデータではなく、CRUDを使って本当にDBから取ってくる
    return await task_crud.get_tasks_with_done(db)

# 2. 新規作成（POST）
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)  # ← レスポンスの型も指定
async def create_task(
    task_body: task_schema.TaskCreate,  # ← ユーザーが送ってきたデータ
    db: AsyncSession = Depends(get_db)  # ← DB接続をもらう
):
    # CRUDを使ってDBに保存する
    return await task_crud.create_task(db, task_body)

# 3. タスク変更（PUT）
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, 
    task_body: task_schema.TaskCreate, 
    db: AsyncSession = Depends(get_db)
):
    # まず、変更対象のタスクが存在するか確認（厨房に在庫確認させる）
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # 存在したら、更新を依頼する
    return await task_crud.update_task(db, task_body, original=task)

# 4. タスク削除（DELETE）
@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    # まず、削除対象のタスクが存在するか確認
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # 存在したら、削除を依頼する
    return await task_crud.delete_task(db, original=task)