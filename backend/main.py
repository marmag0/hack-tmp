from datetime import datetime

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, text

from config import settings
from db import SessionDep
from models import ExampleItem


class ItemCreate(BaseModel):
    name: str


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health(session: SessionDep) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/api/items", response_model=list[ItemRead])
async def list_items(session: SessionDep) -> list[ExampleItem]:
    result = await session.execute(select(ExampleItem).order_by(ExampleItem.id))
    return list(result.scalars().all())


@app.post("/api/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, session: SessionDep) -> ExampleItem:
    item = ExampleItem(name=payload.name)
    session.add(item)
    await session.commit()
    return item
