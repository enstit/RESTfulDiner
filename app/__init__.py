### __init__.py

from datetime import date, datetime
from uuid import UUID

from flask import Flask
from flask_restful import Api

from app.config import Config
from app.extensions import db, jwt
from app.models.cfg_department import CfgDepartment
from app.models.sys_order_department import SysOrderDepartment
from app.models.sys_order_department_item import SysOrderDepartmentItem
from app.models.cfg_event import CfgEvent
from app.models.cfg_event_day import CfgEventDay
from app.models.cfg_item import CfgItem, MenuSectionType, AllergenType
from app.models.cfg_kiosk import CfgKiosk
from app.models.sys_order import SysOrder, PaymentMethodType
from app.models.cfg_printer import CfgPrinter
from app.models.cfg_user import CfgUser, UserRoleType
from app.resources import initialize_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize plugins
    db.init_app(app)
    jwt.init_app(app)

    api = Api(app, prefix="/api/v1", catch_all_404s=True)
    api.init_app(app)

    # Initialize routes
    initialize_routes(api)

    with app.app_context():
        db.create_all()

        # Add sample data for README tutorial
        db.session.add(
            event := CfgEvent(
                event_id=UUID("00000000-0000-8000-8000-000100000001"),
                name="Sagra di Primavera 2025",
                location="Piazza Primo Maggio - 33100 Udine UD",
                days=[
                    first_day := CfgEventDay(
                        event_day_date=date(2025, 5, 1),
                        start_datetime=datetime(2025, 5, 1, 10, 0),
                        end_datetime=datetime(2025, 5, 1, 23, 0),
                    ),
                    CfgEventDay(
                        event_day_date=date(2025, 5, 2),
                        start_datetime=datetime(2025, 5, 2, 10, 0),
                        end_datetime=datetime(2025, 5, 2, 23, 0),
                    ),
                    CfgEventDay(
                        event_day_date=date(2025, 5, 3),
                        start_datetime=datetime(2025, 5, 3, 10, 0),
                        end_datetime=datetime(2025, 5, 3, 23, 0),
                    ),
                    CfgEventDay(
                        event_day_date=date(2025, 4, 23),
                        start_datetime=datetime(2025, 4, 23, 0, 0),
                        end_datetime=datetime(2025, 4, 24, 0, 0),
                    ),
                ],
            )
        )
        db.session.add(
            CfgUser(
                user_id=UUID("00000000-0000-8000-8000-000200000001"),
                username="admin",
                password="admin",
                role=UserRoleType.ADMIN,
            )
        )
        db.session.add(
            operator := CfgUser(
                user_id=UUID("00000000-0000-8000-8000-000200000002"),
                username="operator",
                password="operator",
                role=UserRoleType.OPERATOR,
            )
        )
        db.session.add(
            CfgPrinter(
                event=event,
                printer_id=UUID("00000000-0000-8000-8000-000400000001"),
                name="KitchenPrinter",
                mac_address="32:1c:35:93:4e:07",
                ip_address="10.172.54.145",
            )
        )
        db.session.add(
            fried_department := CfgDepartment(
                event=event,
                department_id=UUID("00000000-0000-8000-8000-000300000001"),
                name="Fried Station",
                items=[
                    chicken_item := CfgItem(
                        name="Fried Chicken",
                        price=5.99,
                        menu_section=MenuSectionType.MAIN_COURSES,
                        allergens=[
                            AllergenType.GLUTEN,
                            AllergenType.EGGS,
                            AllergenType.MILK,
                            AllergenType.MUSTARD,
                        ],
                    ),
                    fries_item := CfgItem(
                        name="French Fries",
                        price=2.99,
                        menu_section=MenuSectionType.SIDE_DISHES,
                        allergens=[AllergenType.GLUTEN],
                    ),
                ],
            )
        )
        db.session.add(
            beverages_department := CfgDepartment(
                event=event,
                department_id=UUID("00000000-0000-8000-8000-000300000002"),
                name="Beverages",
                items=[
                    water_item := CfgItem(
                        name="Water",
                        price=0.79,
                        menu_section=MenuSectionType.DRINKS,
                    ),
                    coke_item := CfgItem(
                        name="Coke",
                        price=2.79,
                        menu_section=MenuSectionType.DRINKS,
                    ),
                    beer_item := CfgItem(
                        name="Beer",
                        price=4.49,
                        menu_section=MenuSectionType.DRINKS,
                        allergens=[AllergenType.GLUTEN],
                    ),
                    CfgItem(
                        name="Wine glass",
                        price=6.99,
                        deposit=1.51,
                        menu_section=MenuSectionType.DRINKS,
                    ),
                ],
            )
        )
        db.session.add(
            kiosk := CfgKiosk(
                event=event,
                kiosk_id=UUID("00000000-0000-8000-8000-000500000001"),
                name="Kiosk 1",
            )
        )
        db.session.add(
            SysOrder(
                event_day=first_day,
                payment_method=PaymentMethodType.CASH,
                total_paid=20.00,
                kiosk=kiosk,
                user=operator,
                departments_orders=[
                    SysOrderDepartment(
                        department=fried_department,
                        department_order_items=[
                            SysOrderDepartmentItem(
                                item=chicken_item, quantity=1
                            ),
                            SysOrderDepartmentItem(
                                item=fries_item, quantity=2
                            ),
                        ],
                    ),
                    SysOrderDepartment(
                        department=beverages_department,
                        department_order_items=[
                            SysOrderDepartmentItem(item=coke_item, quantity=2)
                        ],
                    ),
                ],
            )
        )
        db.session.add(
            SysOrder(
                event_day=first_day,
                payment_method=PaymentMethodType.ELECTRONIC,
                total_paid=12.76,
                kiosk=kiosk,
                user=operator,
                departments_orders=[
                    SysOrderDepartment(
                        department=fried_department,
                        department_order_items=[
                            SysOrderDepartmentItem(
                                item=fries_item, quantity=1
                            ),
                        ],
                    ),
                    SysOrderDepartment(
                        department=beverages_department,
                        department_order_items=[
                            SysOrderDepartmentItem(
                                item=water_item, quantity=1
                            ),
                            SysOrderDepartmentItem(item=beer_item, quantity=2),
                        ],
                    ),
                ],
            )
        )
        db.session.commit()

    return app
