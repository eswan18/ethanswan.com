import os
from pathlib import Path
from dataclasses import dataclass

import pytest


ALLOWED_TAGS = ("ci-only",)
IN_CI = os.getenv("CI") == "true"
THIS_DIR = Path(__file__).parent


@dataclass
class DeadLink:
    url: str
    status_codes: list[int]
    tags: list[str]

    def __post_init__(self):
        for tag in self.tags:
            if tag not in ALLOWED_TAGS:
                raise ValueError(f"Unknown tag: {tag}")
    
    @classmethod
    def from_line(cls, line: str):
        codes, url, *tags = line.strip().split()
        return cls(url, [int(c) for c in codes.split(',')], tags)


@pytest.fixture(scope="session")
def known_dead_links() -> dict[str, list[int]]:
    with open(THIS_DIR / 'data' / 'known_dead_links.txt', 'r') as f:
        # Remove "comment" lines
        lines = [line for line in f.readlines() if not line.startswith('#')]
        # Split the code from the URL.
        links = [DeadLink.from_line(line) for line in lines]
        if not IN_CI:
            links = [link for link in links if "ci-only" not in link.tags]
        # Create a mapping from URL to expected status code.
        known_dead_links_and_codes = {link.url: link.status_codes for link in links}
    return known_dead_links_and_codes
