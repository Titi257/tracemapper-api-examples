"""Minimal TraceMapper API v1 client. Standard library only (Python 3.9+)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class TraceMapperError(Exception):
    def __init__(self, status: int, code: str | None, message: str | None):
        super().__init__(" ".join(str(part) for part in (status, code, message) if part))
        self.status = status
        self.code = code


class TraceMapper:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 120):
        self.api_key = api_key or os.environ.get("TRACEMAPPER_API_KEY")
        if not self.api_key:
            raise ValueError("Set TRACEMAPPER_API_KEY or pass api_key (Pro or Business plan).")
        self.base_url = (base_url or os.environ.get("TRACEMAPPER_BASE_URL") or "https://tracemapper.com").rstrip("/")
        self.timeout = timeout

    def get(self, path: str, **params: Any) -> Any:
        query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
        url = f"{self.base_url}/api/v1/{path}" + (f"?{query}" if query else "")
        request = urllib.request.Request(url, headers={"Authorization": f"Bearer {self.api_key}"})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            try:
                body = json.load(error)
            except ValueError:
                body = {}
            raise TraceMapperError(error.code, body.get("error"), body.get("message")) from None

    def trace(self, dest: str, source: str = "local", protocol: str = "icmp", max_hops: int = 30) -> dict:
        return self.get("trace", dest=dest, source=source, protocol=protocol, maxHops=max_hops)

    def ping(self, host: str, count: int = 4) -> dict:
        return self.get("ping", host=host, count=count)

    def dns(self, domain: str, type: str = "A") -> dict:
        return self.get("dns", domain=domain, type=type)

    def whois(self, ip: str) -> dict:
        return self.get("whois", ip=ip)

    def bgp(self, target: str) -> dict:
        return self.get("bgp", target=target)
