# app/dto/event.py


from typing import List

from app.config import Config
from app.models.event import Event


class EventDTO:
    def __init__(self, event: Event):
        self.event_id = str(event.event_id)
        self.name = event.name

    def to_dict(self):
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/events/{self.event_id}",
            "id": self.event_id,
            "name": self.name,
        }

    @staticmethod
    def from_model(event: Event) -> dict:
        return EventDTO(event).to_dict() if event else {}

    @staticmethod
    def from_model_list(events: List[Event]) -> list[dict]:
        return [EventDTO(event).to_dict() for event in events]
