import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.user import user_router
from app.api.auth import auth_router
from app.api.attachment import a_router
from app.api.comment import c_router
from app.api.defect import d_router
from app.api.projects import p_router
from app.database.settings import create_tables, delete_tables
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

@asynccontextmanager
async def life(app: FastAPI):
    await create_tables()
    print("base are create")
    yield
    await delete_tables()
    print("base are delete")

app = FastAPI(lifespan=life)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(a_router)
app.include_router(c_router)
app.include_router(d_router)
app.include_router(p_router)

async def reset_database():
    print("delete database")
    await delete_tables()
    print("create again")
    await create_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)

if __name__ == "__main__":
    asyncio.run(reset_database())
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)