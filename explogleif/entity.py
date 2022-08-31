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

    # TODO : method to get parents and children entities
    def get_direct_parents(self):
        pass

    def get_direct_children(self):
        pass
