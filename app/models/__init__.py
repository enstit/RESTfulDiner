# app/models/__init__.py


from sqlalchemy import MetaData

metadata = MetaData()

from app.models._base import BaseModel as Diner
from app.models.cfg_delivery_station import CfgDeliveryStation
from app.models.cfg_department import CfgDepartment
from app.models.sys_order_department import SysOrderDepartment
from app.models.sys_order_department_item import SysOrderDepartmentItem
from app.models.cfg_event import CfgEvent
from app.models.cfg_event_day import CfgEventDay
from app.models.cfg_item import CfgItem
from app.models.cfg_kiosk import CfgKiosk
from app.models.sys_order import SysOrder
from app.models.cfg_printer import CfgPrinter
from app.models.cfg_user import CfgUser

__all__ = [
    "Diner",
    "CfgDeliveryStation",
    "CfgDepartment",
    "SysOrderDepartment",
    "SysOrderDepartmentItem",
    "CfgEvent",
    "CfgEventDay",
    "CfgItem",
    "CfgKiosk",
    "SysOrder",
    "CfgPrinter",
    "CfgUser",
]
