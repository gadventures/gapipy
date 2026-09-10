"""Ticket 07: async terminal ops on AsyncQuery."""
import json

import httpx
import pytest

from gapipy import AsyncClient


def _tour(i):
    return {"id": f"T{i}", "href": f"https://api.example.com/tours/T{i}", "product_line": "SA"}


def _page(results, count=None, next_href=None):
    body = {"results": results}
    if count is not None:
        body["count"] = count
    if next_href:
        body["links"] = [{"rel": "next", "href": next_href}]
    return httpx.Response(200, content=json.dumps(body).encode(),
                          headers={"content-type": "application/json"})


def _client(handler):
    return AsyncClient(
        api_root="https://api.example.com", application_key="k",
        transport=httpx.MockTransport(handler), http2=False,
    )


async def test_afirst_returns_first_record():
    async with _client(lambda r: _page([_tour(1), _tour(2)], count=2)) as ac:
        tour = await ac.tours.afirst()
    assert tour.id == "T1"


async def test_afirst_returns_none_when_empty():
    async with _client(lambda r: _page([], count=0)) as ac:
        result = await ac.tours.afirst()
    assert result is None


async def test_acount_returns_count():
    async with _client(lambda r: _page([_tour(1)], count=42)) as ac:
        count = await ac.tours.acount()
    assert count == 42


async def test_aexists_true_when_results():
    async with _client(lambda r: _page([_tour(1)], count=1)) as ac:
        assert await ac.tours.aexists() is True


async def test_aexists_false_when_empty():
    async with _client(lambda r: _page([], count=0)) as ac:
        assert await ac.tours.aexists() is False


async def test_aexists_short_circuits_before_second_page():
    """A single list_raw call should be enough — don't walk pagination."""
    calls = []

    def handler(request):
        calls.append(str(request.url))
        return _page([_tour(1)], count=99, next_href="https://api.example.com/tours?page=2")

    async with _client(handler) as ac:
        await ac.tours.aexists()
    assert len(calls) == 1


async def test_alist_materializes_all_pages():
    pages = [
        (200, {"results": [_tour(1), _tour(2)], "links": [{"rel": "next", "href": "https://api.example.com/tours?page=2"}]}),
        (200, {"results": [_tour(3)]}),
    ]

    def handler(request):
        page_num = int(request.url.params.get("page", 1))
        status, body = pages[page_num - 1]
        return httpx.Response(status, content=json.dumps(body).encode(),
                              headers={"content-type": "application/json"})

    async with _client(handler) as ac:
        result = await ac.tours.alist()
    assert [t.id for t in result] == ["T1", "T2", "T3"]


async def test_alist_respects_limit():
    async with _client(lambda r: _page([_tour(i) for i in range(1, 6)], count=5)) as ac:
        result = await ac.tours.alist(limit=2)
    assert [t.id for t in result] == ["T1", "T2"]


async def test_aget_still_works():
    """Regression guard: #05 aget path unchanged."""
    def handler(request):
        assert request.url.path == "/tours/SAMPLE"
        return httpx.Response(200, json=_tour("SAMPLE"))

    async with _client(handler) as ac:
        tour = await ac.tours.aget("SAMPLE")
    assert tour.id == "TSAMPLE"
