# app/resources/event.py

from flask_restful import Resource

from app.dto.event import EventDTO
from app.extensions import db
from app.models.cfg_event import CfgEvent


class EventResource(Resource):
    def get(
        self, *, event_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        if event_id:
            event = (
                db.session.query(CfgEvent)
                .filter(CfgEvent.event_id == event_id)
                .one_or_none()
            )
            if not event:
                return {"error": f"Event {event_id} was not found"}, 404
            return EventDTO.from_model(event), 200
        events = db.session.query(CfgEvent).all()
        return EventDTO.from_model_list(events), 200
