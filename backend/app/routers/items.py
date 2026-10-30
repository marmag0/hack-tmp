from fastapi import APIRouter, status
from sqlalchemy import select

from app.db import SessionDep
from app.models import ExampleItem
from app.schemas import ItemCreate, ItemRead

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
async def list_items(session: SessionDep) -> list[ExampleItem]:
    result = await session.execute(select(ExampleItem).order_by(ExampleItem.id))
    return list(result.scalars().all())


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, session: SessionDep) -> ExampleItem:
    item = ExampleItem(name=payload.name)
    session.add(item)
    await session.commit()
    return item
