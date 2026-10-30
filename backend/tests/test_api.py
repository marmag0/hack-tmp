from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import httpx
import pytest

from app.db import get_session
from app.main import app
from app.models import ExampleItem


class FakeResult:
    def __init__(self, items: list[ExampleItem]) -> None:
        self._items = items

    def scalars(self) -> "FakeResult":
        return self

    def all(self) -> list[ExampleItem]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self.items: list[ExampleItem] = []

    async def execute(self, statement: object) -> FakeResult:
        return FakeResult(self.items)

    def add(self, item: ExampleItem) -> None:
        item.id = len(self.items) + 1
        item.created_at = datetime.now(UTC)
        self.items.append(item)

    async def commit(self) -> None:
        pass


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient]:
    session = FakeSession()

    async def override_get_session() -> AsyncGenerator[FakeSession]:
        yield session

    app.dependency_overrides[get_session] = override_get_session
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_health(client: httpx.AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_create_and_list_items(client: httpx.AsyncClient) -> None:
    empty_response = await client.get("/api/items")
    assert empty_response.status_code == 200
    assert empty_response.json() == []

    create_response = await client.post("/api/items", json={"name": "Test item"})
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["name"] == "Test item"
    assert "created_at" in created

    list_response = await client.get("/api/items")
    assert list_response.status_code == 200
    assert list_response.json() == [created]
