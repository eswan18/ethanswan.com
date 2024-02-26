import os
from dataclasses import dataclass, field
from functools import cache
from typing import Mapping, Coroutine, Any

import pytest
from httpx import AsyncClient, Client, Response
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

    async def a_get(
        self,
        path: str,
        headers: Mapping[str, str] | None = None,
        follow_redirects: bool = False
    ) -> Coroutine[Any, Any, Response]:
        return await self._client.get(path, headers=headers, follow_redirects=follow_redirects)
    
    def get(self, path: str, follow_redirects: bool = False):
        return self._sync_client.get(path, follow_redirects=follow_redirects)


@dataclass
class SiteLinks:
    internal: set[str]
    fragment: set[str]
    external: set[str]

    def __str__(self):
        internal = '\n    - ' + '\n    - '.join(sorted(self.internal))
        fragment = '\n    - ' + '\n    - '.join(sorted(self.fragment))
        external = '\n    - ' + '\n    - '.join(sorted(self.external))
        return f"SiteLinks\n- internal\n{internal},\n- fragment\n{fragment},\n- external{external}"
    

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
def get_all_links(client: SiteClient) -> SiteLinks:
    to_process = []
    seen_site_links = set()
    fragment_links = set()
    seen_external_links = set()
    # Start at the homepage and work through all the links.
    to_process.append("/")
    while len(to_process) > 0:
        path = to_process.pop()
        if path in seen_site_links:
            continue
        seen_site_links.add(path)

        response = client.get(path, follow_redirects=True)

        # Add all the links on the page to the list of pages to process
        next_links = links_on_page(response.content)
        for link in next_links:
            if link.startswith(client.url):
                link = link.removeprefix(client.url)
            if link.startswith("/"):
                if link not in seen_site_links:
                    to_process.append(link)
                    # Mark this page as processed.
            elif link.startswith("#"):
                link = path + link
                fragment_links.add(link)
            else:
                if link not in seen_external_links:
                    if link.strip() != "":
                        seen_external_links.add(link)
    links = SiteLinks(seen_site_links, fragment_links, seen_external_links)
    return links


@pytest.fixture
def all_internal_links(client: SiteClient, capsys) -> set[str]:
    with capsys.disabled():
        links = get_all_links(client)
    return links.internal


@pytest.fixture
def all_external_links(client: SiteClient, capsys) -> set[str]:
    with capsys.disabled():
        links = get_all_links(client)
    return links.external


@pytest.fixture
def all_fragment_links(client: SiteClient, capsys) -> set[str]:
    with capsys.disabled():
        links = get_all_links(client)
    return links.fragment