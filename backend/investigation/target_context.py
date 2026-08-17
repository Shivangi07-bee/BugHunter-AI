from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import urlparse


@dataclass
class TargetContext:
    name: str
    base_url: str
    scope: List[str] = field(default_factory=list)
    source: str = "repository"

    def normalized_url(self) -> str:
        url = self.base_url.strip()

        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        parsed = urlparse(url)

        return f"{parsed.scheme}://{parsed.netloc}"

    def target_name(self) -> str:
        parsed = urlparse(self.normalized_url())

        return parsed.netloc or self.name

    def is_valid(self) -> bool:
        parsed = urlparse(self.normalized_url())

        return bool(parsed.netloc)

    def to_dict(self):
        return {
            "name": self.name,
            "base_url": self.normalized_url(),
            "target": self.target_name(),
            "scope": self.scope,
            "source": self.source,
            "valid": self.is_valid(),
        }