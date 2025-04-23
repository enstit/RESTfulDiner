# app/resources/kiosk.py

from flask_restful import reqparse

from app.dto.kiosk import KioskDTO
from app.extensions import db
from app.models.kiosk import Kiosk
from app.resources.auth import ProtectedResource


class KioskResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)

    def get(self, *, kiosk_id: str | None = None) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if kiosk_id:
            kiosk = (
                db.session.query(Kiosk)
                .filter(
                    Kiosk.event_id == msg.get("event_id"),
                    Kiosk.kiosk_id == kiosk_id,
                )
                .one_or_none()
            )
            if kiosk:
                return KioskDTO.from_model(kiosk), 200
            return {"message": "Kiosk was not found"}, 404

        kiosks = (
            db.session.query(Kiosk)
            .filter(Kiosk.event_id == msg.get("event_id"))
            .all()
        )
        return KioskDTO.from_model_list(kiosks), 200

    def post(self) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = KioskResource.parser.parse_args()
        new_kiosk = Kiosk(
            event_id=msg.get("event_id"),
            name=data["name"],
        )
        db.session.add(new_kiosk)
        db.session.commit()
        return KioskDTO.from_model(new_kiosk), 201
