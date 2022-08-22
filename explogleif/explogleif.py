# explogleif.py
## custom functions needed to explore gleif API

import requests
from explogleif.entity import Entity


def latest_status(country=None, category=None, status=None):
    url = "https://api.gleif.org/api/v1/lei-records"

    headers = {"Accept": "application/vnd.api+json"}

    payload = {
        # Country code (2 letters)
        "filter[entity.legalAddress.country]": country,
        # Entity category
        # BRANCH, FUND, SOLE_PROPRIETOR, GENERAL, RESIDENT_GOVERNMENT_ENTITY, INTERNATIONAL_ORGANIZATION
        "filter[entity.category]": category,
        # List of status
        # ISSUED, LAPSED, ANNULLED, PENDING_TRANSFER, PENDING_ARCHIVAL, DUPLICATE, RETIRED, MERGED
        "filter[registration.status]": status,
        # pagination
        "page[number]": 1,  # Must be at least 1.
        "page[size]": 1,  # Must be between 1 and 200.
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()

    lei_count = response["meta"]["pagination"][
        "total"
    ]  # pagination is 1 entity per page, so number of pages = number of entities
    latest_entity = Entity(
        name=response["data"][0]["attributes"]["entity"]["legalName"]["name"],
        lei=response["data"][0]["attributes"]["lei"],
        city=response["data"][0]["attributes"]["entity"]["legalAddress"]["city"],
        country=response["data"][0]["attributes"]["entity"]["legalAddress"]["country"],
    )

    answer = {"lei_count": lei_count, "latest_entity": latest_entity}

    return answer
