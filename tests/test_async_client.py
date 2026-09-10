"""Ticket 05: async tracer bullet — AsyncClient.<resource>.aget."""
import os

import pytest

from gapipy import AsyncClient
from gapipy.resources import Tour


TOUR_PAYLOAD = {
    "id": "SAMPLE",
    "href": "https://api.example.com/tours/SAMPLE",
    "product_line": "SA",
}


async def test_aget_returns_hydrated_resource(mock_transport):
    transport = mock_transport({("GET", "/tours/SAMPLE"): (200, TOUR_PAYLOAD)})
    async with AsyncClient(api_root="https://api.example.com", application_key="k", transport=transport, http2=False) as ac:
        tour = await ac.tours.aget("SAMPLE")

    assert isinstance(tour, Tour)
    assert tour.id == "SAMPLE"
    assert tour.product_line == "SA"


async def test_aget_variation_id_appended(mock_transport):
    transport = mock_transport({("GET", "/tours/SAMPLE/2"): (200, TOUR_PAYLOAD)})
    async with AsyncClient(api_root="https://api.example.com", application_key="k", transport=transport, http2=False) as ac:
        tour = await ac.tours.aget("SAMPLE", variation_id=2)
    assert isinstance(tour, Tour)


async def test_response_callback_fires(mock_transport):
    transport = mock_transport({("GET", "/tours/SAMPLE"): (200, TOUR_PAYLOAD)})
    seen = []
    async with AsyncClient(api_root="https://api.example.com", application_key="k", transport=transport, http2=False) as ac:
        ac.on_response(lambda resp: seen.append(resp.status_code))
        await ac.tours.aget("SAMPLE")
    assert seen == [200]


async def test_get_resource_class_by_name_registry():
    async with AsyncClient(application_key="k", http2=False) as ac:
        assert ac.get_resource_class_by_name("Tour") is Tour
        assert ac.get_resource_class_by_name("tours") is Tour


@pytest.mark.integration
async def test_live_api_http2_negotiation():
    """Smoke test — confirms HTTP/2 negotiation against rest.gadventures.com."""
    key = os.environ.get("GAPI_APPLICATION_KEY")
    if not key:
        pytest.skip("GAPI_APPLICATION_KEY not set")
    async with AsyncClient(application_key=key, http2=True) as ac:
        # Any real GET; we care about the negotiated protocol.
        response = await ac._httpx.get(
            f"{ac.api_root}/tour_dossiers", params={"per_page": 1},
            headers={"X-Application-Key": key},
        )
        assert response.http_version == "HTTP/2", f"expected HTTP/2, got {response.http_version}"
