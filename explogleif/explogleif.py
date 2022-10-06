# explogleif.py
## custom functions needed to explore gleif API

import requests
import pandas as pd
from explogleif.entity import Entity
import graphviz
import streamlit as st


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
    latest_entity = Entity(json_data=response["data"][0])

    answer = {"lei_count": lei_count, "latest_entity": latest_entity}

    return answer


def search_entities(
    user_input=None, page_number=1, page_size=200, owns=None, owned_by=None
):
    url = "https://api.gleif.org/api/v1/lei-records"

    params = {
        "filter[entity.names]": user_input,
        "page[number]": page_number,
        "page[size]": page_size,
        "filter[owns]": owns,
        "filter[ownedBy]": owned_by,
    }

    response = requests.get(url, params=params).json()

    entities = []

    for json_entity in response["data"]:
        new_entity = Entity(json_data=json_entity)
        entities.append(new_entity)

    total_number_of_results = response["meta"]["pagination"]["total"]

    return entities, total_number_of_results


def create_graph(entity):

    # get colors from Streamlit app theme
    primary_color = st.get_option("theme.primaryColor")
    background_color = st.get_option("theme.backgroundColor")
    secondary_background_color = st.get_option("theme.secondaryBackgroundColor")
    tc = st.get_option("theme.textColor")

    # style
    graph_attr = {"bgcolor": background_color}
    node_attr = {
        "style": "rounded,filled",
        "shape": "box",
        "color": primary_color,
        "fontcolor": tc,
        "fillcolor": secondary_background_color,
    }
    edge_attr = {"color": primary_color}

    dot = graphviz.Digraph(
        f"graph_{entity.legal_name}",
        comment=f"parents and children of {entity.legal_name}, lei: {entity.lei}",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    )

    # dot.attr(ratio="fill")

    # starting node
    dot.node(entity.lei, entity.legal_name)

    # children nodes
    for idx, child in enumerate(entity.get_direct_children()):
        dot.node(child.lei, child.legal_name)
        dot.edge(entity.lei, child.lei, minlen=str(idx + 1))

    # parents node
    for parent in entity.get_direct_parents():
        dot.node(parent.lei, parent.legal_name)
        dot.edge(parent.lei, entity.lei)

    print(dot.source)

    return dot
