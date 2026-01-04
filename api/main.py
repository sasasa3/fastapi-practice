from fastapi import FastAPI

from api.routers import task, done

app = FastAPI()

# 作成したルーター（受付窓口）をアプリに登録する
app.include_router(task.router)
app.include_router(done.router)