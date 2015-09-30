"""
Just a quick and dirty test to see if there are any major differences using
connection pooling. On this sort of test, against my local gapi, I didn't see
any significant difference:
    ('test_reg()', 17.258477926254272)
    ('test_pool()', 17.658794164657593)

    ('test_reg()', 17.032647132873535)
    ('test_pool()', 18.120828866958618)

    ('test_reg()', 21.509217023849487)
    ('test_pool()', 20.322450160980225)

Hitting rest.g I did start to see some differences:
    ('test_reg()', 39.82205319404602)
    ('test_pool()', 38.13359093666077)

    ('test_reg()', 46.09530687332153)
    ('test_pool()', 38.95572781562805)

    ('test_reg()', 49.59551000595093)
    ('test_pool()', 37.631394147872925)

Further testing is probably necessary, but there you go.

NB: I chose tour_categories as the resource to fetch because it is pretty fast
(as opposed to something like itineraries or tour_dossier). This is certainly
nothing like a realistic workload, but I wanted to be able to make lots of
requests.
"""

from gapipy import Client

CONFIG = {
    'application_key': 'something',
    #'api_root': 'http://localhost:5000',
    'api_root': 'https://rest.gadventures.com',
    'use_connection_pool': False,
}

POOLING_CONFIG = dict(CONFIG)
POOLING_CONFIG['use_connection_pool'] = True

N = 300


def _test(client):
    client.tour_categories.get(15)
    # Is testing a slow resource useful? These values for an itinerary are
    # currently valid, you may need to change 'em if you see 404s:
    # client.itineraries.get(1497, variation_id=2689)


def test_reg():
    _test(Client(**CONFIG))


def test_pool():
    _test(Client(**POOLING_CONFIG))


if __name__ == '__main__':
    import timeit

    print(
        "test_reg()",
        timeit.timeit("test_reg()", number=N, setup="from __main__ import test_reg"))

    print("test_pool()",
        timeit.timeit("test_pool()", number=N, setup="from __main__ import test_pool"))
