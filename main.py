from fastapi import FastAPI
from routes import router

app = FastAPI()

app.include_router(router)

@app.get('/', tags=['Home'], status_code=200)
async def get():
    return 'Hello World'