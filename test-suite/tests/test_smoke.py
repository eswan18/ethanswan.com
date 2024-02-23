import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope="module")
async def test_homepage_responds(client: AsyncClient):
    response = await client.a_get("/")
    # Should get a successful response
    response.raise_for_status()
    # Should return some content
    assert len(response.content.strip()) > 0


@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "path",
    ["/posts/", "/teaching/", "/appearances/", "/running-blog/", "/nonsense/"],
)
async def test_main_nav_pages_respond(path: str, client: AsyncClient):
    response = await client.a_get(path)
    # Should get a successful response
    response.raise_for_status()
    # Should return some content
    assert len(response.content.strip()) > 0