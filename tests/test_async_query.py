"""Ticket 06: async iteration + pagination on AsyncQuery."""
import json

import httpx
import pytest

from gapipy import AsyncClient
from gapipy.async_client import AsyncQuery
from gapipy.resources import Tour


TOUR_PAYLOAD_BASE = {"href": "https://api.example.com/tours/x", "product_line": "SA"}


def _tour(i):
    return {"id": f"T{i}", "href": f"https://api.example.com/tours/T{i}", "product_line": "SA"}


def _paged_transport(pages):
    """Build a MockTransport that walks `pages` in order.

    Each page is a list of records; the transport links them via `links[rel=next]`
    pointing at `/tours?page=<n+1>`.
    """
    def handler(request):
        # first page has no `page` query; subsequent pages have `page=N`.
        page_num = int(request.url.params.get("page", 1))
        idx = page_num - 1
        if idx >= len(pages):
            return httpx.Response(404, json={"error": "no such page"})
        results = pages[idx]
        body = {"results": results}
        if idx + 1 < len(pages):
            body["links"] = [{
                "rel": "next",
                "href": f"https://api.example.com/tours?page={page_num + 1}",
            }]
        return httpx.Response(200, content=json.dumps(body).encode(),
                              headers={"content-type": "application/json"})
    return httpx.MockTransport(handler)


def _client(transport):
    return AsyncClient(
        api_root="https://api.example.com", application_key="k",
        transport=transport, http2=False,
    )


async def test_aiter_yields_all_records_single_page():
    transport = _paged_transport([[_tour(1), _tour(2), _tour(3)]])
    async with _client(transport) as ac:
        ids = [t.id async for t in ac.tours]
    assert ids == ["T1", "T2", "T3"]


async def test_aiter_follows_next_links_across_pages():
    pages = [
        [_tour(1), _tour(2)],
        [_tour(3), _tour(4)],
        [_tour(5)],
    ]
    transport = _paged_transport(pages)
    async with _client(transport) as ac:
        ids = [t.id async for t in ac.tours]
    assert ids == ["T1", "T2", "T3", "T4", "T5"]


async def test_aiter_stops_when_no_next_link():
    transport = _paged_transport([[_tour(1)]])
    async with _client(transport) as ac:
        count = 0
        async for _ in ac.tours:
            count += 1
    assert count == 1


async def test_all_respects_limit():
    pages = [[_tour(i) for i in range(1, 6)], [_tour(i) for i in range(6, 11)]]
    transport = _paged_transport(pages)
    async with _client(transport) as ac:
        collected = []
        async for t in ac.tours.all(limit=3):
            collected.append(t.id)
    assert collected == ["T1", "T2", "T3"]


async def test_filter_returns_async_query():
    async with AsyncClient(application_key="k", http2=False) as ac:
        q = ac.tours.filter(name="Peru")
        assert isinstance(q, AsyncQuery)
        # Immutable clone: original filters untouched
        assert ac.tours._filters == {}
        assert q._filters == {"name": "Peru"}


async def test_chained_filter_order_returns_async_query():
    async with AsyncClient(application_key="k", http2=False) as ac:
        q = ac.tours.filter(name="Peru").filter(status="active")
        assert isinstance(q, AsyncQuery)
        assert q._filters == {"name": "Peru", "status": "active"}


async def test_filter_params_sent_on_wire():
    seen_params = []

    def handler(request):
        seen_params.append(dict(request.url.params))
        return httpx.Response(200, json={"results": []})

    transport = httpx.MockTransport(handler)
    async with _client(transport) as ac:
        async for _ in ac.tours.filter(name="Peru", status="active"):
            pass
    assert seen_params == [{"name": "Peru", "status": "active"}]


async def test_hydrated_objects_are_stubs():
    transport = _paged_transport([[_tour(1)]])
    async with _client(transport) as ac:
        async for t in ac.tours:
            assert isinstance(t, Tour)
            assert t.is_stub is True
            assert t.id == "T1"
