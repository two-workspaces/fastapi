"""Example resource: a small CRUD API kept in memory.

Replace it with your own routers. Data here is lost on every redeploy; add a
database (Railway Postgres + SQLAlchemy or SQLModel) when you need to keep it.
"""
from datetime import datetime, timezone
from itertools import count

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/items", tags=["items"])


class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Coffee"])
    price: float = Field(ge=0, examples=[3.5])
    tags: list[str] = Field(default_factory=list, max_length=10, examples=[["drink"]])


class Item(ItemIn):
    id: int
    created_at: datetime


_items: dict[int, Item] = {}
_ids = count(1)


@router.get("", response_model=list[Item])
async def list_items(limit: int = 50, offset: int = 0) -> list[Item]:
    """List items, oldest first."""
    return list(_items.values())[offset : offset + max(0, min(limit, 500))]


@router.post("", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemIn) -> Item:
    """Create an item. The body is validated against `ItemIn`."""
    item = Item(id=next(_ids), created_at=datetime.now(timezone.utc), **data.model_dump())
    _items[item.id] = item
    return item


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return _items[item_id]


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, data: ItemIn) -> Item:
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    item = _items[item_id].model_copy(update=data.model_dump())
    _items[item_id] = item
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int) -> None:
    if _items.pop(item_id, None) is None:
        raise HTTPException(status_code=404, detail="Item not found")
