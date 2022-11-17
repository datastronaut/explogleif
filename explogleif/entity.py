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

    def get_direct_parent(self, page_size=200):
        """
        Return an objects of class Entity that is direct parents of self
        """
        parent_json = requests.get(
            f"https://api.gleif.org/api/v1/lei-records/{self.lei}/direct-parent"
        ).json()["data"]
        return Entity(json_data=parent_json)

    def get_direct_children(self, page_size=200):
        """
        Return a list of objects of class Entity that are direct children of self
        """
        children_json = requests.get(
            f"https://api.gleif.org/api/v1/lei-records/{self.lei}/direct-children"
        ).json()["data"]
        return [Entity(json_data=child_json) for child_json in children_json]
