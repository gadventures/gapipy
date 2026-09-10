"""Ticket 09: async parity for `on_response`. Mirrors `test_client_seams.OnResponseTests`."""
import httpx
import pytest

from gapipy import AsyncClient


TOUR_PAYLOAD = {"id": "SAMPLE", "href": "https://api.example.com/tours/SAMPLE", "product_line": "SA"}


def _client(transport):
    return AsyncClient(
        api_root="https://api.example.com", application_key="k",
        transport=transport, http2=False,
    )


async def test_sync_callback_fires_on_200(mock_transport):
    transport = mock_transport({("GET", "/tours/SAMPLE"): (200, TOUR_PAYLOAD)})
    seen = []
    async with _client(transport) as ac:
        ac.on_response(lambda resp: seen.append(resp.status_code))
        await ac.tours.aget("SAMPLE")
    assert seen == [200]


async def test_async_callback_awaited(mock_transport):
    transport = mock_transport({("GET", "/tours/SAMPLE"): (200, TOUR_PAYLOAD)})
    seen = []
    async def cb(resp):
        seen.append(resp.status_code)
    async with _client(transport) as ac:
        ac.on_response(cb)
        await ac.tours.aget("SAMPLE")
    assert seen == [200]


async def test_callback_fires_on_4xx(mock_transport):
    transport = mock_transport({("GET", "/tours/SAMPLE"): (404, {"error": "not found"})})
    seen = []
    async with _client(transport) as ac:
        ac.on_response(lambda resp: seen.append(resp.status_code))
        try:
            await ac.tours.aget("SAMPLE")
        except httpx.HTTPStatusError:
            pass
    assert seen == [404]


async def test_multiple_callbacks_fire_in_registration_order(mock_transport):
    transport = mock_transport({("GET", "/tours/SAMPLE"): (200, TOUR_PAYLOAD)})
    order = []
    async def second(resp):
        order.append("second")
    async with _client(transport) as ac:
        ac.on_response(lambda resp: order.append("first"))
        ac.on_response(second)
        await ac.tours.aget("SAMPLE")
    assert order == ["first", "second"]


async def test_callback_sees_303_status(mock_transport):
    """Async twin of `test_callback_sees_redirect_history`.

    httpx.AsyncClient defaults to `follow_redirects=False`, so the callback observes
    the 303 directly — the exact context the gapipy-private Profile POST hook needs.
    """
    transport = mock_transport({("GET", "/tours/SAMPLE"): (303, {"location": "https://api.example.com/tours/OTHER"})})
    seen = []
    async with _client(transport) as ac:
        ac.on_response(lambda resp: seen.append((resp.status_code, str(resp.url))))
        try:
            await ac.tours.aget("SAMPLE")
        except httpx.HTTPStatusError:
            pass
    assert seen == [(303, "https://api.example.com/tours/SAMPLE")]
