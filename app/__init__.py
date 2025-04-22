### __init__.py

from datetime import date, datetime

from flask import Flask
from flask_restful import Api

from app.config import Config
from app.extensions import db, jwt
from app.models.department import Department
from app.models.department_order import DepartmentOrder
from app.models.department_order_item import DepartmentOrderItem
from app.models.event import Event
from app.models.event_day import EventDay
from app.models.item import Item, MenuSectionType, AllergenType
from app.models.kiosk import Kiosk
from app.models.order import Order, PaymentMethodType
from app.models.printer import Printer
from app.models.user import User, UserRoleType
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
            event := Event(
                name="Sample Event",
                description="Sample event",
                location="Via Planis, 93 - 33100 Udine UD",
                days=[
                    first_day := EventDay(
                        event_date=date(2025, 5, 1),
                        start_datetime=datetime(2025, 5, 1, 10, 0),
                        end_datetime=datetime(2025, 5, 1, 23, 0),
                    ),
                    EventDay(
                        event_date=date(2025, 5, 2),
                        start_datetime=datetime(2025, 5, 2, 10, 0),
                        end_datetime=datetime(2025, 5, 2, 23, 0),
                    ),
                    EventDay(
                        event_date=date(2025, 5, 3),
                        start_datetime=datetime(2025, 5, 3, 10, 0),
                        end_datetime=datetime(2025, 5, 3, 23, 0),
                    ),
                    EventDay(
                        event_date=date(2025, 4, 22),
                        start_datetime=datetime(2025, 4, 22, 0, 0),
                        end_datetime=datetime(2025, 4, 22, 23, 0),
                    ),
                ],
            )
        )
        db.session.add(
            User(username="admin", password="admin", role=UserRoleType.ADMIN)
        )
        db.session.add(
            operator := User(
                username="operator",
                password="operator",
                role=UserRoleType.OPERATOR,
            )
        )
        db.session.add(
            Printer(
                event=event,
                name="KitchenPrinter",
                mac_address="32:1c:35:93:4e:07",
                ip_address="10.172.54.145",
            )
        )
        db.session.add(kiosk := Kiosk(event=event, name="Kiosk 1"))
        db.session.add(
            fried_department := Department(
                event=event,
                name="Fried Station",
                items=[
                    chicken_item := Item(
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
                    fries_item := Item(
                        name="French Fries",
                        price=2.99,
                        menu_section=MenuSectionType.SIDE_DISHES,
                        allergens=[AllergenType.GLUTEN],
                    ),
                ],
            )
        )
        db.session.add(
            beverages_department := Department(
                event=event,
                name="Beverages",
                items=[
                    water_item := Item(
                        name="Water",
                        price=0.79,
                        menu_section=MenuSectionType.DRINKS,
                    ),
                    coke_item := Item(
                        name="Coke",
                        price=2.79,
                        menu_section=MenuSectionType.DRINKS,
                    ),
                    beer_item := Item(
                        name="Beer",
                        price=4.49,
                        menu_section=MenuSectionType.DRINKS,
                        allergens=[AllergenType.GLUTEN],
                    ),
                    wine_item := Item(
                        name="Wine glass",
                        price=6.99,
                        deposit=1.51,
                        menu_section=MenuSectionType.DRINKS,
                    ),
                ],
            )
        )
        db.session.add(
            Order(
                event_day=first_day,
                payment_method=PaymentMethodType.CASH,
                total_paid=20.00,
                kiosk=kiosk,
                user=operator,
                departments_orders=[
                    DepartmentOrder(
                        department=fried_department,
                        department_order_items=[
                            DepartmentOrderItem(item=chicken_item, quantity=1),
                            DepartmentOrderItem(item=fries_item, quantity=2),
                        ],
                    ),
                    DepartmentOrder(
                        department=beverages_department,
                        department_order_items=[
                            DepartmentOrderItem(item=coke_item, quantity=2)
                        ],
                    ),
                ],
            )
        )
        db.session.add(
            Order(
                event_day=first_day,
                payment_method=PaymentMethodType.ELECTRONIC,
                total_paid=12.76,
                kiosk=kiosk,
                user=operator,
                departments_orders=[
                    DepartmentOrder(
                        department=fried_department,
                        department_order_items=[
                            DepartmentOrderItem(item=fries_item, quantity=1),
                        ],
                    ),
                    DepartmentOrder(
                        department=beverages_department,
                        department_order_items=[
                            DepartmentOrderItem(item=water_item, quantity=1),
                            DepartmentOrderItem(item=beer_item, quantity=2),
                        ],
                    ),
                ],
            )
        )
        db.session.commit()

    return app
