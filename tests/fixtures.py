# TODO: Replace fixtures by factories (or anything more manageable)
# TODO: Replace hardcoded urls with config.API_ROOT?

PPP_TOUR_DATA = {
    'departures': {'href': 'http://localhost:5000/tours/21346/departures'},
    'departures_end_date': '2013-12-31',
    'departures_start_date': '2013-01-01',
    'tour_dossier': {
        'href': 'http://localhost:5000/tour_dossiers/21346',
        'id': '21346'
    },
    'product_line': 'PPP',
    'href': 'http://localhost:5000/tours/21346',
    'id': '21346'
}


TOUR_DOSSIER_LIST_DATA = {
    'count': 3,
    'max_per_page': 3,
    'current_page': 1,
    'results': [
        {
            'href': 'http://localhost:5000/tour_dossiers/1234',
            'id': '1234',
            'tour_dossier_code': 'ABCD'
        },
        {
            'href': 'http://localhost:5000/tour_dossiers/5678',
            'id': '5678',
            'tour_dossier_code': 'EFGH'
        },
        {
            'href': 'http://localhost:5000/tour_dossiers/9012',
            'id': '9012',
            'tour_dossier_code': 'IJKL'
        }
    ],
    'links': []
}

FIRST_PAGE_LIST_DATA = {
    'count': 6,
    'max_per_page': 3,
    'current_page': 1,
    'results': [
        {
            'href': 'http://localhost:5000/resources/1234',
            'id': '1234',
        },
        {
            'href': 'http://localhost:5000/resources/5678',
            'id': '5678',
        },
        {
            'href': 'http://localhost:5000/resources/9012',
            'id': '9012',
        }
    ],
    'links': [
        {
            'href': 'http://localhost:5000/resources/?page=2',
            'rel': 'next',
        }
    ]
}

SECOND_PAGE_LIST_DATA = {
    'count': 6,
    'max_per_page': 3,
    'current_page': 2,
    'results': [
        {
            'href': 'http://localhost:5000/resources/3456',
            'id': '3456',
        },
        {
            'href': 'http://localhost:5000/resources/7890',
            'id': '7890',
        },
        {
            'href': 'http://localhost:5000/resources/1111',
            'id': '1111',
        }
    ],
    'links': [
        {
            'href': 'http://localhost:5000/resources/',
            'rel': 'prev',
        }
    ]
}
PPP_DOSSIER_DATA = {
    "departures_start_date": "2013-01-01",
    "departures_end_date": "2013-12-31",
    "itineraries": [
        {
            "duration": 15,
            "type": "SUMMARY",
            "days": [
                {
                    "body": "Arrive at any time.",
                    "id": "125737468",
                    "label": "Day 1 Lima"
                },
                {
                    "body": "Fly to Juliaca and transfer to Puno.  Visit the floating Islands of Uros and take a guided tour of Lake Titicaca with a homestay in a small village.   Optional visit to Sillustani burial site.",
                    "id": "125737469",
                    "label": "Days 2-4 Puno/Lake Titicaca (1B,1L,1D)"
                },
                {
                    "body": "Travel day by bus from Puno to Cuzco.",
                    "id": "125737470",
                    "label": "Day 5 Cuzco"
                },
                {
                    "body": "Full day guided tour of the Sacred Valley and Ollantaytambo ruins along with a visit to a Planeterra weaving project in a local community. Shopping opportunities at a local market.",
                    "id": "125737471",
                    "label": "Day 6 Sacred Valley/Ollantaytambo"
                },
                {
                    "body": "4-day guided Inca Trail hike with visit to Machu Picchu. Optional visit to the Inca Bridge before returning to Cuzco.",
                    "id": "125737472",
                    "label": "Days 7-10 Inca Trail/Machu Picchu (3B,3L,3D)"
                },
                {
                    "body": "Free day to explore Cuzco or relax. Active options include whitewater rafting, horseback riding and mountain biking.",
                    "id": "125737473",
                    "label": "Day 11 Cuzco"
                },
                {
                    "body": "Fly to Puerto Maldonado and continue by motorized canoe to our comfortable, intimate and exclusive G Lodge Amazon. Enjoy guided excursions by expert naturalists to spot wildlife at nearby oxbow lakes, clay licks and treetop towers. Included rubber boots while at the lodge. Fly back to Lima on Day 14.",
                    "id": "125737474",
                    "label": "Days 12-14 Amazon Jungle (2B,2L,2D)"
                },
                {
                    "body": "Depart at any time.",
                    "id": "125737475",
                    "label": "Day 15 Lima"
                }
            ]
        }
    ],
    "description": "Spot macaws in the jungle and caimans on the riverbanks, sail the waters of Lake Titicaca, delight in the smells of markets and explore ancient ruins, including a trek along the Inca Trail. As we operate our own treks, our quality equipment and the expertise of our porters and CEOs will ensure that your first glimpse of Machu Picchu will leave you in awe. Whether you're scanning the canopy for wildlife from the comfort of our intimate and exclusive G Lodge Amazon or following in the footsteps of the Incas, this fast-paced adventure provides a sweeping view of this diverse country.",
    "tour": {
        "href": "http://localhost:5000/tours/21346",
        "id": "21346"
    },
    "href": "http://localhost:5000/tour_dossiers/21346",
    "product_line": "PPP",
    "images": [
        {
            "image_href": "https://media.gadventures.com/media-server/dynamic/admin/maps/2013/PPP.jpg",
            "type": "MAP"
        },
        {
            "image_href": "https://media.gadventures.com/media-server/dynamic/admin/trip-banners/south-america/peru/PPP/PPP_banner_peru_landscape_ruins_machu_picchu_clouds.jpg",
            "type": "BANNER"
        }
    ],
    "details": [
        {
            "body": "Meeting the locals at a Lake Titicaca homestay, climbing the Inca Trail to Machu Picchu, spotting wildlife at our exclusive G Lodge Amazon, devouring seafood in Lima.",
            "detail_type": {
                "id": "2",
                "label": "Highlights"
            }
        },
        {
            "body": "16",
            "detail_type": {
                "id": "113",
                "label": "Max Pax"
            }
        },
        {
            "body": "Chief Experience Officer (CEO) throughout, specialist Inca Trail CEO on hike.",
            "detail_type": {
                "id": "18",
                "label": "Group Leader"
            }
        }
    ],
    "geography": {
        "start_city": {
            "name": "Lima"
        },
        "start_country": {
            "href": "http://localhost:5000/countries/PE",
            "id": "PE",
            "name": "Peru"
        },
        "region": {
            "name": "South America"
        },
        "visited_countries": [
            {
                "href": "http://localhost:5000/countries/PE",
                "id": "PE",
                "name": "Peru"
            }
        ],
        "finish_country": {
            "href": "http://localhost:5000/countries/PE",
            "id": "PE",
            "name": "Peru"
        },
        "primary_country": {
            "href": "http://localhost:5000/countries/PE",
            "id": "PE",
            "name": "Peru"
        },
        "finish_city": {
            "name": "Lima"
        }
    },
    "id": "21346",
    "categories": [
        {
            "category_type": {
                "id": "1",
                "label": "Activity"
            },
            "name": "Wildlife/Nature"
        },
        {
            "category_type": {
                "id": "1",
                "label": "Activity"
            },
            "name": "Trekking/Hiking"
        },
        {
            "category_type": {
                "id": "1",
                "label": "Activity"
            },
            "name": "Culture/History"
        },
        {
            "category_type": {
                "id": "16",
                "label": "Trip Style"
            },
            "name": "Classic"
        },
        {
            "category_type": {
                "id": "28",
                "label": "Service Level"
            },
            "name": "Standard"
        },
        {
            "category_type": {
                "id": "33",
                "label": "Physical Grading"
            },
            "name": "4"
        },
        {
            "category_type": {
                "id": "39",
                "label": "Merchandising"
            },
            "name": "Top Seller"
        },
        {
            "category_type": {
                "id": "58",
                "label": "Trip Type"
            },
            "name": "Small Group"
        }
    ],
    "name": "Peru Panorama"
}


PRODUCTS_DATA = [
    {
        "href": "https://localhost:5000/departures/1234",
        "id": "1234",
        "type": "departures",
        "sub_type": "Tour",
    },
    {
        "href": "https://localhost:5000/departures/5678",
        "id": "5678",
        "type": "departures",
        "sub_type": "Tour",
    },
    {
        "href": "https://localhost:5000/departures/9012",
        "id": "9012",
        "type": "departures",
        "sub_type": "Tour",
    }
]

DUMMY_DEPARTURE = {
    "sku": "GAPPPP130406-O1",
    "product_line": "PPP",
    "tour_dossier": {
        "href": "https://rest.gadventures.com/tour_dossiers/9882",
        "id": "9882",
        "name": "Peru Panorama"
    },
    "date_last_modified": "2013-06-10T19:12:04Z",
    "finish_date": "2013-04-20",
    "lowest_pp2a_prices": [
        {
            "currency": "USD",
            "amount": "3099.00"
        },
        {
            "currency": "AUD",
            "amount": "2999.00"
        },
        {
            "currency": "CHF",
            "amount": "2949.00"
        },
        {
            "currency": "GBP",
            "amount": "1749.00"
        },
        {
            "currency": "NZD",
            "amount": "3999.00"
        },
        {
            "currency": "CAD",
            "amount": "3299.00"
        },
        {
            "currency": "EUR",
            "amount": "2149.00"
        }
    ],
    "availability": {
        "status": "NOT_BOOKABLE",
        "total": 8
    },
    "tour": {
        "href": "https://rest.gadventures.com/tours/9882",
        "id": "9882"
    },
    "nearest_finish_airport": {
        "code": "LIM"
    },
    "id": "419504",
    "latest_arrival_time": "2013-04-06T23:59:59",
    "href": "https://rest.gadventures.com/departures/419504",
    "flags": [],
    "earliest_departure_time": "2013-04-20T00:00:00",
    "addons": [
        {
            "product": {
                "id": "54",
                "href": "https://rest.gadventures.com/accommodations/54",
                "name": "San Agustin Colonial",
                "type": "accommodations",
                "sub_type": "Hotel"
            },
            "start_date": "2013-04-02",
            "finish_date": "2013-04-06",
            "min_days": 1,
            "max_days": 5,
            "request_space_date": "2013-04-01",
            "halt_booking_date": "2013-04-01",
        },
        {
            "product": {
                "id": "54",
                "href": "https://rest.gadventures.com/accommodations/54",
                "name": "San Agustin Colonial",
                "type": "accommodations",
                "sub_type": "Hotel"
            },
            "start_date": "2013-04-20",
            "finish_date": "2013-04-24",
            "min_days": 1,
            "max_days": 5,
            "request_space_date": "2013-04-01",
            "halt_booking_date": "2013-04-01",
        },
        {
            "product": {
                "id": "298",
                "href": "https://rest.gadventures.com/transports/298",
                "name": "Airport to Hotel Transfer",
                "type": "transports",
                "sub_type": "Transfer"
            },
            "start_date": "2013-04-02",
            "finish_date": "2013-04-06",
            "min_days": 1,
            "max_days": 1,
            "request_space_date": "2013-04-01",
            "halt_booking_date": "2013-04-01",
        },
        {
            "product": {
                "id": "4486",
                "href": "https://rest.gadventures.com/activities/4486",
                "name": "Peru Culinary Theme Pack",
                "type": "activities",
                "sub_type": "Product"
            },
            "start_date": "2013-04-16",
            "finish_date": "2013-04-17",
            "min_days": 1,
            "max_days": 1,
            "request_space_date": "2013-04-01",
            "halt_booking_date": "2013-04-01",
        }
    ],
    "date_created": "2012-01-26T20:29:07Z",
    "nearest_start_airport": {
        "code": "LIM"
    },
    "start_date": "2013-04-06",
    "rooms": [
        {
            "code": "STANDARD",
            "name": "Standard",
            "flags": [],
            "price_bands": [
                {
                    "max_age": 100,
                    "code": "ADULT",
                    "name": "Adult",
                    "max_travellers": 16,
                    "min_age": 12,
                    "prices": [
                        {
                            "promotions": [
                                {
                                    "amount": "2199.20",
                                    "href": "https://rest.gadventures.com/promotions/48500",
                                    "id": "48500"
                                },
                            ],
                            "currency": "AUD",
                            "amount": "2999.00",
                            "deposit": "250.00"
                        },
                        {
                            "promotions": [
                                {
                                    "amount": "2199.20",
                                    "href": "https://rest.gadventures.com/promotions/48500",
                                    "id": "48500"
                                },
                            ],
                            "currency": "CAD",
                            "amount": "3299.00",
                            "deposit": "250.00"
                        },
                        {
                            "promotions": [
                                {
                                    "amount": "2199.20",
                                    "href": "https://rest.gadventures.com/promotions/48500",
                                    "id": "48500"
                                },
                            ],
                            "currency": "CHF",
                            "amount": "2949.00",
                            "deposit": "250.00"
                        },
                        {
                            "promotions": [
                                {
                                    "amount": "2199.20",
                                    "href": "https://rest.gadventures.com/promotions/48500",
                                    "id": "48500"
                                },
                            ],
                            "currency": "EUR",
                            "amount": "2149.00",
                            "deposit": "250.00"
                        },
                        {
                            "promotions": [
                                {
                                    "amount": "2199.20",
                                    "href": "https://rest.gadventures.com/promotions/48500",
                                    "id": "48500"
                                },
                            ],
                            "currency": "GBP",
                            "amount": "1749.00",
                            "deposit": "100.00"
                        },
                        {
                            "promotions": [
                                {
                                    "amount": "2199.20",
                                    "href": "https://rest.gadventures.com/promotions/48500",
                                    "id": "48500"
                                },
                            ],
                            "currency": "NZD",
                            "amount": "3999.00",
                            "deposit": "250.00"
                        },
                        {
                            "promotions": [
                                {
                                    "amount": "2199.20",
                                    "href": "https://rest.gadventures.com/promotions/48500",
                                    "id": "48500"
                                },
                            ],
                            "currency": "USD",
                            "amount": "3099.00",
                            "deposit": "250.00"
                        }
                    ],
                    "min_travellers": 1
                }
            ],
            "addons": [
                {
                    "product": {
                        "id": "T419504",
                        "href": "https://rest.gadventures.com/single_supplements/T419504",
                        "name": "My Own Room",
                        "type": "single_supplements",
                        "sub_type": "Single Supplement"
                    },
                    "start_date": "2013-04-06",
                    "finish_date": "2013-04-20",
                    "min_days": 14,
                    "max_days": 14,
                    "request_space_date": "2013-04-01",
                    "halt_booking_date": "2013-04-01",
                }
            ],
            "availability": {
                "status": "NOT_BOOKABLE",
                "total": 8,
                "male": None,
                "female": None
            }
        }
    ]
}


DUMMY_PROMOTION = {
    "currencies": ["AUD", "CAD", "CHF", "EUR", "GBP", "NZD", "USD"],
    "name": "10% off North America",
    "commission_rate": 0,
    "sale_finish_date": "2012-08-27",
    "discount_percent": "10.00",
    "id": "18336",
    "terms_and_conditions": "From big cities to untamed wildlife and scenic landscapes, there's a North American adventure for everyone.\r\n<ul><li>Travellers receive 10% off all North America tours (valid for all North America trip codes).</li>\r\n<li>Book by August 27, 2012 for departures through December 16, 2012.</li></ul>\r\nFor general Terms and Conditions please visit our <a href=http://www.gadventures.com/terms-and-conditions/>Terms and Conditions page.</a>",
    "product_finish_date": None,
    "discount_amount": None,
    "href": "https://localhost:5000/promotions/18336",
    "sale_start_date": "2012-08-14",
    "product_start_date": None,
    "room_codes": None,
    "flags": None,
    "products": PRODUCTS_DATA,
    "promotion_code": "BZ-NOAM10",
    "min_travellers": 0
}
