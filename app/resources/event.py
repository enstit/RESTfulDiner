# app/resources/event.py

from flask_restful import Resource

from app.dto.event import EventDTO
from app.extensions import db
from app.models.event import Event


class EventResource(Resource):
    def get(
        self, *, event_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        if event_id:
            event = (
                db.session.query(Event)
                .filter(Event.event_id == event_id)
                .one_or_none()
            )
            if not event:
                return {"error": f"Event {event_id} was not found"}, 404
            return EventDTO.from_model(event), 200
        events = db.session.query(Event).all()
        return EventDTO.from_model_list(events), 200
