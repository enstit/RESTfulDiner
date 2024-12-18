from ipaddress import IPv4Address

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import BaseModel
from models import Printer, Kiosk, Department, DeliveryStation, Item
from models._types import MenuSectionType
from models._types import OrderStatusType
from models._types import AllergenType

if __name__ == "__main__":

    engine = create_engine(
        "postgresql://postgres:postgres@srv-ud01:5432/postgres",
        connect_args={"options": "-csearch_path=sagrevolution"},
        echo=False,
    )

    with engine.connect() as connection:
        BaseModel.metadata.create_all(bind=engine)
        connection.commit()

    with Session(engine) as session:

        # Add kiosks to the database
        session.add(
            Kiosk(
                name="Kiosk 01",
                printer=Printer(
                    name="Printer 01",
                    mac_address="02:1F:E0:13:F9:60",
                    ip_address=IPv4Address("10.0.0.65"),
                ),
            )
        )
        session.add(
            Kiosk(
                name="Kiosk 02",
                printer=Printer(
                    name="Printer 02",
                    mac_address="02:1F:E0:13:A5:22",
                    ip_address=IPv4Address("10.0.0.66"),
                ),
            )
        )
        session.add(Kiosk(name="Kiosk 03", printer=None))

        # Add delivery stations to the database
        session.add(DeliveryStation(name="Table 101"))
        session.add(DeliveryStation(name="Table 102"))
        session.add(DeliveryStation(name="Table 201"))
        session.add(DeliveryStation(name="Table 202"))
        session.add(DeliveryStation(name="Table 301", active_flag=False))
        session.add(DeliveryStation(name="Table 302", active_flag=False))

        # Add departments to the database

        session.add(
            department_kitchen := Department(
                name="Kitchen",
                color="lightblue",
                printer=Printer(
                    name="Printer 03",
                    mac_address="02:1F:E0:13:A4:96",
                    ip_address=IPv4Address("10.0.0.67"),
                ),
            )
        )
        session.add(
            department_grill := Department(
                name="Grill",
                color="lightblue",
                printer=department_kitchen.printer,
            )
        )
        session.add(
            department_desserts := Department(
                name="Desserts", color="pink", printer=None
            )
        )
        session.add(
            department_beverage := Department(
                name="Beverages", color="green", printer=None
            )
        )

        # Add items to the database
        session.add(
            Item(
                name="Spaghetti Bolognese",
                description="Best Spaghetti ever.",
                price=7.50,
                department=department_kitchen,
                menu_section=MenuSectionType.FIRST_COURSES,
                initial_status=OrderStatusType.PENDING,
                allergens=[
                    AllergenType.GLUTEN,
                    AllergenType.MILK,
                    AllergenType.CELERY,
                ],
            )
        )

        session.add(
            Item(
                name="Fettuccine Alfredo",
                description="You thought Italians really know what this is? Think again.",
                price=6.50,
                department=department_kitchen,
                menu_section=MenuSectionType.FIRST_COURSES,
                initial_status=OrderStatusType.PENDING,
                allergens=[AllergenType.GLUTEN, AllergenType.MILK],
            )
        )

        session.add(
            Item(
                name="Hawaiian Pizza",
                description="A Neapolitan pizza that has a topping of tomato sauce, cheese, pineapple, and ham.",
                price=8.50,
                department=department_grill,
                menu_section=MenuSectionType.SINGLE_DISHES,
                initial_status=OrderStatusType.PENDING,
                allergens=[AllergenType.GLUTEN, AllergenType.MILK],
            )
        )

        session.add(
            Item(
                name="French Fries",
                description="Thinly cut deep-fried potatoes.",
                price=4.00,
                department=department_grill,
                menu_section=MenuSectionType.SIDE_DISHES,
                initial_status=OrderStatusType.IN_PROGRESS,
                allergens=[AllergenType.GLUTEN],
            )
        )

        session.add(
            Item(
                name="Cheeseburger",
                description="Once you try it, you'll never go to McDonald's again.",
                price=9.00,
                department=department_grill,
                menu_section=MenuSectionType.MAIN_COURSES,
                initial_status=OrderStatusType.PENDING,
                allergens=[
                    AllergenType.GLUTEN,
                    AllergenType.MILK,
                    AllergenType.MUSTARD,
                    AllergenType.SESAME_SEEDS,
                ],
            )
        )

        session.add(
            Item(
                name="Coca-Cola (33cl)",
                price=2.50,
                department=department_beverage,
                menu_section=MenuSectionType.DRINKS,
            )
        )
        session.add(
            Item(
                name="Beer (20cl)",
                price=2.50,
                department=department_beverage,
                menu_section=MenuSectionType.DRINKS,
            )
        )
        session.add(
            Item(
                name="Beer (40cl)",
                price=4.50,
                department=department_beverage,
                menu_section=MenuSectionType.DRINKS,
            )
        )

        # Commit the changes to the database
        session.commit()
