from flask import Flask
from flask_restful import Api

from app.config import Config
from app.extensions import db, jwt
from app.models.department import Department
from app.models.department_order import DepartmentOrder
from app.models.department_order_item import DepartmentOrderItem
from app.models.item import Item, MenuSectionType
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
        db.session.add(kiosk := Kiosk(name="Kiosk 1"))
        db.session.add(
            fried_department := Department(
                name="Fried Station",
                items=[
                    chicken_item := Item(
                        name="Fried Chicken",
                        price=5.99,
                        menu_section=MenuSectionType.MAIN_COURSES,
                    ),
                    fries_item := Item(
                        name="French Fries",
                        price=2.99,
                        menu_section=MenuSectionType.SIDE_DISHES,
                    ),
                ],
            )
        )
        db.session.add(
            beverages_department := Department(
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
                    ),
                ],
            )
        )
        db.session.add(
            Order(
                payment_method=PaymentMethodType.CASH,
                total_paid=20.00,
                kiosk=kiosk,
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
                payment_method=PaymentMethodType.ELECTRONIC,
                total_paid=12.76,
                kiosk=kiosk,
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
        db.session.bulk_save_objects(
            [
                User(username="admin", password="admin", role=UserRoleType.ADMIN),
                User(
                    username="operator",
                    password="operator",
                    role=UserRoleType.OPERATOR,
                ),
                Printer(
                    name="KitchenPrinter",
                    mac_address="32:1c:35:93:4e:07",
                    ip_address="10.172.54.145",
                ),
            ]
        )
        db.session.commit()

    return app
