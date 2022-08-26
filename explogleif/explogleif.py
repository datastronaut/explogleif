# explogleif.py
## custom functions needed to explore gleif API

import requests
import pandas as pd
from explogleif.entity import Entity


def latest_status(country=None, category=None, status=None):
    url = "https://api.gleif.org/api/v1/lei-records"

    params = {
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

    response = requests.get(url, params=params).json()

    # pagination is 1 entity per page, so number of pages = number of entities
    lei_count = response["meta"]["pagination"]["total"]
    latest_entity = Entity(
        name=response["data"][0]["attributes"]["entity"]["legalName"]["name"],
        lei=response["data"][0]["attributes"]["lei"],
        city=response["data"][0]["attributes"]["entity"]["legalAddress"]["city"],
        country=response["data"][0]["attributes"]["entity"]["legalAddress"]["country"],
    )

    answer = {"lei_count": lei_count, "latest_entity": latest_entity}

    return answer


def search_entities(user_input, page_number=1, page_size=200):
    url = "https://api.gleif.org/api/v1/lei-records"

    params = {
        "filter[entity.names]": user_input,
        "page[number]": page_number,
        "page[size]": page_size,
    }

    response = requests.get(url, params=params).json()

    entity_list = []

    for json_entity in response["data"]:
        new_entity = Entity(
            name=json_entity["attributes"]["entity"]["legalName"]["name"],
            lei=json_entity["id"],
            city=json_entity["attributes"]["entity"]["legalAddress"]["city"],
            country=json_entity["attributes"]["entity"]["legalAddress"]["country"],
        )
        entity_list.append(new_entity)

    entity_dict = {"name": [], "lei": [], "city": [], "country": []}

    for entity in entity_list:
        entity_dict["name"].append(entity.name)
        entity_dict["lei"].append(entity.lei)
        entity_dict["city"].append(entity.city)
        entity_dict["country"].append(entity.country)

    entity_df = pd.DataFrame.from_dict(entity_dict)
    entity_df.index = entity_df.index + 1

    total_number_of_results = response["meta"]["pagination"]["total"]

    return entity_df, total_number_of_results
