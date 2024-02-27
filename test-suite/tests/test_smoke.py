import asyncio
from pathlib import Path

import pytest
from httpx import AsyncClient


this_dir = Path(__file__).parent

# Headers that make the external sites treat us like a real browser.
EXTERNAL_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
}


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
async def test_all_internal_links_work(all_internal_links, client):
    tasks = [client.a_get(link, follow_redirects=True) for link in all_internal_links]
    dead_links = set()

    for future in asyncio.as_completed(tasks):
        response = await future
        # If the response isn't a success, add the link to our dead links set
        if response.status_code != 200:
            dead_links.add(response.url)
    assert not dead_links, f"Dead links found: {dead_links}"


@pytest.mark.asyncio(scope="module")
async def test_all_external_links_work(all_external_links, client):
    with open(this_dir / 'data' / 'known_dead_links.txt', 'r') as f:
        lines = [line.strip().split(' ') for line in f.readlines()]
        known_dead_links_and_codes = {line[1]: int(line[0]) for line in lines}
    
    async def get_link(link: str):
        response = await client.a_get(link, headers=EXTERNAL_HEADERS, follow_redirects=True)
        return link, response

    tasks = [get_link(link) for link in all_external_links]

    dead_links = {}
    for future in asyncio.as_completed(tasks):
        link, response = await future
        # If the response isn't a success, add the link to our dead links set
        if response.status_code != 200:
            if link in known_dead_links_and_codes:
                if response.status_code == known_dead_links_and_codes[link]:
                    continue
            dead_links[link] = (response.status_code, response.reason_phrase)
    assert not dead_links, f"Dead links found: {dead_links}"