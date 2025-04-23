# app/dto/item.py


from typing import List

from app.config import Config
from app.models.item import Item


class ItemDTO:
    CONTEXT = {
        "@context": {
            "schema": "https://schema.org/",
            "self": "@id",
            "type": "@type",
            "name": "schema:name",
            "description": "schema:description",
            "department": {"@id": "schema:isRelatedTo", "@type": "@id"},
            "menu_section": "schema:category",
            "price": "schema:price",
            "deposit": "schema:price",
            "availability": "schema:inventoryLevel",
            "initial_status": "schema:itemCondition",
            "license": {"@id": "schema:license", "@type": "@id"},
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    def __init__(self, item: Item):
        self.event_id = str(item.event_id)
        self.item_id = str(item.item_id)
        self.name = item.name
        self.description = item.description
        self.department = item.department
        self.menu_section = item.menu_section
        self.price = item.price
        self.deposit = item.deposit
        self.availability = item.availability
        self.initial_status = item.initial_status

    def to_dict(self) -> dict:
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/items/{self.item_id}",
            "type": "schema:Product",
            "name": self.name,
            "description": self.description,
            "department": (
                f"{Config.APP_URL}{Config.API_URI}/departments/{self.department.department_id}"
                if self.department
                else None
            ),
            "menu_section": self.menu_section.name,
            "price": round(self.price, 2),
            "deposit": round(self.deposit, 2) if self.deposit else None,
            "availability": self.availability,
            "initial_status": self.initial_status.name,
        }

    @staticmethod
    def from_model(item: Item) -> dict:
        return {
            **ItemDTO.CONTEXT,
            "data": ItemDTO(item).to_dict() if item else None,
        }

    @staticmethod
    def from_model_list(items: List[Item]) -> dict:
        return {
            **ItemDTO.CONTEXT,
            "data": [ItemDTO(item).to_dict() for item in items],
        }
