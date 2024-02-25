import asyncio

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
    ("/posts/", "/teaching/", "/appearances/", "/running-blog/", "/nonsense/"),
)
async def test_main_nav_pages_respond(path: str, client):
    response = await client.a_get(path)
    # Should get a successful response
    response.raise_for_status()
    # Should return some content
    assert len(response.content.strip()) > 0


@pytest.mark.asyncio(scope="module")
async def test_all_links_work(all_site_links, client):
    tasks = [client.a_get(link, follow_redirects=True) for link in all_site_links]
    dead_links = set()

    for future in asyncio.as_completed(tasks):
        response = await future
        # If the response isn't a success, add the link to our dead links set
        if response.status_code != 200:
            dead_links.add(response.url)
    assert not dead_links, f"Dead links found: {dead_links}"