import os
from dataclasses import dataclass
from functools import cache

import pytest
from httpx import AsyncClient, Client
from bs4 import BeautifulSoup


DEFAULT_URL = "https://ethanswan.com"
URL = os.environ.get("ES_SITE_URL", DEFAULT_URL)


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
def client() -> Client:
    return Client(base_url=URL)

@pytest.fixture(scope="session")
def async_client() -> AsyncClient:
    return AsyncClient(base_url=URL)


def links_on_page(page: str | bytes) -> list[str]:
    """Return a list of all the links on a page."""
    soup = BeautifulSoup(page, "html.parser")
    a_tags = soup.find_all("a")
    if not a_tags:
        return []
    links = [link.get("href") for link in a_tags]
    links = filter(lambda link: link is not None and '@' not in link, links)
    return list(links)


@pytest.fixture(scope="session")
def all_links(client: Client) -> SiteLinks:
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
            if link.startswith(URL):
                link = link.removeprefix(URL)
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


@pytest.fixture(scope="session")
def internal_links(all_links: SiteLinks) -> set[str]:
    return all_links.internal


@pytest.fixture(scope="session")
def external_links(all_links: SiteLinks) -> set[str]:
    return all_links.external


@pytest.fixture(scope="session")
def fragment_links(all_links: SiteLinks) -> set[str]:
    return all_links.fragment