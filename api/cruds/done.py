from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model

# 完了フラグが立っているかチェックする（判定用）
async def get_done(db: AsyncSession, task_id: int) -> task_model.Task | None:
    result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == task_id)
    )
    return result.scalars().first()

# 完了にする（PUT）
async def create_done(db: AsyncSession, task_id: int) -> task_model.Task:
    task = await get_done(db, task_id)
    if task:
        task.done = True
        await db.commit()
        await db.refresh(task)
    return task

# 完了を取り消す（DELETE）
async def delete_done(db: AsyncSession, task_id: int) -> task_model.Task:
    task = await get_done(db, task_id)
    if task:
        task.done = False
        await db.commit()
        await db.refresh(task)
    return task