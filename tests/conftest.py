"""Shared test fixtures. `mock_transport` builds an httpx.MockTransport from a `{(method, path): (status, body)}` map."""
import json

import httpx
import pytest


@pytest.fixture
def mock_transport():
    def _factory(routes):
        def handler(request: httpx.Request) -> httpx.Response:
            key = (request.method, request.url.path)
            if key not in routes:
                return httpx.Response(404, json={"error": f"unmocked {key}"})
            status, body = routes[key]
            return httpx.Response(status, content=json.dumps(body).encode(), headers={"content-type": "application/json"})
        return httpx.MockTransport(handler)
    return _factory
