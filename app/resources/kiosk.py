# app/resources/kiosk.py

from flask_restful import reqparse

from app.dto.kiosk import KioskDTO
from app.extensions import db
from app.models.cfg_kiosk import CfgKiosk
from app.resources.auth import ProtectedResource


class KioskResource(ProtectedResource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)

    def get(
        self, *, kiosk_id: str | None = None
    ) -> tuple[dict | list[dict], int]:
        msg, code = super().authenticate(admin_only=False)
        if code != 200:
            return msg, code
        if kiosk_id:
            kiosk = (
                db.session.query(CfgKiosk)
                .filter(
                    CfgKiosk.event_id == msg.get("event_id"),
                    CfgKiosk.kiosk_id == kiosk_id,
                )
                .one_or_none()
            )
            if kiosk:
                return KioskDTO.from_model(kiosk), 200
            return {
                "error": f"Kiosk {kiosk_id} was not found in the current event"
            }, 404

        kiosks = (
            db.session.query(CfgKiosk)
            .filter(CfgKiosk.event_id == msg.get("event_id"))
            .all()
        )
        return KioskDTO.from_model_list(kiosks), 200

    def post(self) -> tuple[dict, int]:
        msg, code = super().authenticate(admin_only=True)
        if code != 200:
            return msg, code
        data = KioskResource.parser.parse_args()
        new_kiosk = CfgKiosk(
            event_id=msg.get("event_id"),
            name=data["name"],
        )
        db.session.add(new_kiosk)
        db.session.commit()
        return KioskDTO.from_model(new_kiosk), 201
