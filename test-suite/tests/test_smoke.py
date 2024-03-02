import asyncio
from pathlib import Path

import pytest
from httpx import AsyncClient
from bs4 import BeautifulSoup


this_dir = Path(__file__).parent

# Headers that make the external sites treat us like a real browser.
EXTERNAL_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
}


@pytest.fixture(scope="session")
def known_dead_links() -> dict[str, int]:
    with open(this_dir / 'data' / 'known_dead_links.txt', 'r') as f:
        # Remove "comment" lines
        lines = [line for line in f.readlines() if not line.startswith('#')]
        # Split the code from the URL.
        lines = [line.strip().split(' ') for line in lines]
        # Create a mapping from URL to expected status code.
        known_dead_links_and_codes = {line[1]: int(line[0]) for line in lines}
    return known_dead_links_and_codes


@pytest.mark.asyncio(scope="module")
async def test_homepage_responds(async_client: AsyncClient):
    response = await async_client.get("/")
    # Should get a successful response
    response.raise_for_status()
    # Should return some content
    assert len(response.content.strip()) > 0


@pytest.mark.asyncio(scope="module")
@pytest.mark.parametrize(
    "path",
    ("/posts/", "/teaching/", "/appearances/", "/running-blog/", "/nonsense/"),
)
async def test_main_nav_pages_respond(path: str, async_client: AsyncClient):
    response = await async_client.get(path)
    # Should get a successful response
    response.raise_for_status()
    # Should return some content
    assert len(response.content.strip()) > 0


@pytest.mark.asyncio(scope="module")
async def test_all_internal_links_work(internal_links: set[str], async_client: AsyncClient):

    async def link_is_valid(link: str) -> tuple[str, bool]:
        response = await async_client.get(link, follow_redirects=True)
        return link, response.status_code == 200

    link_validity = await asyncio.gather(*[link_is_valid(link) for link in internal_links])
    dead_links = [link for link, valid in link_validity if not valid]

    assert not dead_links, f"Dead links found: {dead_links}"


@pytest.mark.asyncio(scope="module")
async def test_all_external_links_work(external_links: set[str], known_dead_links, async_client: AsyncClient):

    async def link_validity_and_code(link: str) -> tuple[str, bool, int]:
        response = await async_client.get(link, headers=EXTERNAL_HEADERS, follow_redirects=True)
        if response.status_code != 200:
            # Ignoring known dead links.
            if link in known_dead_links and response.status_code == known_dead_links[link]:
                return link, True, response.status_code
            return link, False, response.status_code
        return link, True, response.status_code

    link_validity = await asyncio.gather(*[link_validity_and_code(link) for link in external_links])
    dead_links = [(link, code) for link, valid, code in link_validity if not valid]

    assert not dead_links, f"Dead external links found: {dead_links}"


@pytest.mark.asyncio(scope="module")
async def test_fragment_links_work(fragment_links: set[str], async_client: AsyncClient):

    async def fragment_is_valid(link: str) -> tuple[str, bool]:
        url, fragment = link.split("#", 1)
        if url.startswith("/posts"):
            # We ignore fragment links on the posts pages because those pages show
            # article excerpts (including footnotes) but not the rest of the article
            # (where the fragment link leads).
            return link, True
        response = await async_client.get(url, follow_redirects=True)
        soup = BeautifulSoup(response.content, "html.parser")
        target = soup.find(id=fragment)
        return link, target is not None

    fragment_validity = await asyncio.gather(*[fragment_is_valid(link) for link in fragment_links])
    invalid_fragments = [link for link, valid in fragment_validity if not valid]

    assert not invalid_fragments, f"Dead fragment links found: {invalid_fragments}"



@pytest.mark.skip("Not implemented")
def test_all_images_work():
    ...