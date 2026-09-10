"""Skeleton async test that proves the async test harness works.

Ticket 04: no production async code exists yet; this test wires
`httpx.AsyncClient` to the `mock_transport` fixture directly, asserts a
mocked body reaches the caller, and confirms `pytest-asyncio` + the
fixture pattern are functional.
"""
import httpx
import pytest


async def test_mock_transport_returns_body(mock_transport):
    transport = mock_transport({
        ("GET", "/tours/1"): (200, {"id": 1, "name": "Everest"}),
    })
    async with httpx.AsyncClient(transport=transport, base_url="https://api.example.com") as ac:
        response = await ac.get("/tours/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Everest"}


async def test_mock_transport_404_on_unmocked_route(mock_transport):
    transport = mock_transport({})
    async with httpx.AsyncClient(transport=transport, base_url="https://api.example.com") as ac:
        response = await ac.get("/nothing")
    assert response.status_code == 404
