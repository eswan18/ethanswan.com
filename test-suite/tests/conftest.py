import os
import asyncio
from dataclasses import dataclass, field

import pytest
from httpx import AsyncClient


DEFAULT_URL = "https://ethanswan.com"


@dataclass
class SiteClient:
    """A SiteClient is a thin wrapper around an httpx client."""
    url: str
    client: AsyncClient = field(default_factory=AsyncClient)

    def __post_init__(self):
        self.client.base_url = self.url

    async def a_get(self, path: str):
        return await self.client.get(path)


@pytest.fixture(scope="session")
def url():
    return os.environ.get("ES_SITE_URL", DEFAULT_URL)


@pytest.fixture(scope="module")
def client(url):
    return SiteClient(url)
