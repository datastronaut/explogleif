import requests


class Entity:
    def __init__(self, json_data=None, lei=None):
        if not json_data:
            json_data = requests.get(
                f"https://api.gleif.org/api/v1/lei-records/{lei}"
            ).json()["data"]

        self.lei = json_data["attributes"]["lei"]
        self.legal_name = json_data["attributes"]["entity"]["legalName"]["name"]
        self.address_lines = json_data["attributes"]["entity"]["legalAddress"][
            "addressLines"
        ]
        self.postal_code = json_data["attributes"]["entity"]["legalAddress"][
            "postalCode"
        ]
        self.city = json_data["attributes"]["entity"]["legalAddress"]["city"]
        self.country = json_data["attributes"]["entity"]["legalAddress"]["country"]

    def get_direct_parents(self, page_size=200):
        """
        Return a list of objects of class Entity that are direct parents of self
        """
        parents_json = requests.get(
            f"https://api.gleif.org/api/v1/lei-records?filter[owns]={self.lei}&page[size]={page_size}"
        ).json()["data"]
        return [Entity(json_data=parent_json) for parent_json in parents_json]

    def get_direct_children(self, page_size=200):
        """
        Return a list of objects of class Entity that are direct children of self
        """
        children_json = requests.get(
            f"https://api.gleif.org/api/v1/lei-records?filter[ownedBy]={self.lei}&page[size]={page_size}"
        ).json()["data"]
        return [Entity(json_data=child_json) for child_json in children_json]
