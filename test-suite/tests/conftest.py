import os
from dataclasses import dataclass, field
from functools import cache

import pytest
from httpx import AsyncClient, Client
from bs4 import BeautifulSoup


DEFAULT_URL = "https://ethanswan.com"
URL = os.environ.get("ES_SITE_URL", DEFAULT_URL)


@dataclass(eq=True, frozen=True)
class SiteClient:
    """A SiteClient is a thin wrapper around an httpx client."""
    url: str
    _client: AsyncClient = field(default_factory=AsyncClient, hash=False, compare=False)
    _sync_client: Client = field(default_factory=Client, hash=False, compare=False)

    def __post_init__(self):
        self._client.base_url = self.url
        self._sync_client.base_url = self.url

    async def a_get(self, path: str, follow_redirects: bool = False):
        return await self._client.get(path, follow_redirects=follow_redirects)
    
    def get(self, path: str, follow_redirects: bool = False):
        return self._sync_client.get(path, follow_redirects=follow_redirects)



@pytest.fixture(scope="session")
def client() -> SiteClient:
    return SiteClient(URL)


def links_on_page(page: str | bytes) -> list[str]:
    """Return a list of all the links on a page."""
    soup = BeautifulSoup(page, "html.parser")
    a_tags = soup.find_all("a")
    if not a_tags:
        return []
    links = [link.get("href") for link in a_tags]
    links = filter(lambda link: link is not None, links)
    return list(links)


@cache
def get_all_relative_links(client: SiteClient) -> set[str]:
    to_process = []
    processed = set()
    # Start at the homepage and work through all the links.
    to_process.append("/")
    while len(to_process) > 0:
        path = to_process.pop()
        if path in processed:
            continue
        response = client.get(path, follow_redirects=True)
        response.raise_for_status()

        # Add all the links on the page to the list of pages to process
        for link in links_on_page(response.content):
            if link.startswith("/") and link not in processed:
                to_process.append(link)
        # Mark this page as processed.
        processed.add(path)
    return processed


@pytest.fixture
def all_relative_links(client: SiteClient, capsys) -> set[str]:
    with capsys.disabled():
        links = get_all_relative_links(client)
    return links