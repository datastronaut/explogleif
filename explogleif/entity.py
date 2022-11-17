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

    def get_direct_parent(self):
        """
        Return an object of class Entity that is the direct parent of self
        """
        response = requests.get(
            f"https://api.gleif.org/api/v1/lei-records/{self.lei}/direct-parent"
        )
        if response.status_code == 200:
            direct_parent = Entity(response.json()["data"])
        else:
            direct_parent = None
        return direct_parent

    def get_direct_children(self):
        """
        Return a list of objects of class Entity that are direct children of self
        """

        response = requests.get(
            f"https://api.gleif.org/api/v1/lei-records/{self.lei}/direct-children"
        )

        if response.status_code == 200:
            direct_children = [
                Entity(json_data=child_json) for child_json in response.json()["data"]
            ]
        else:
            direct_children = None

        return direct_children
