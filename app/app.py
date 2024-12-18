#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.models import Item, Order, DepartmentOrder, DepartmentOrderItem
from app.db.models._types import PaymentMethodType

engine = create_engine(
    "postgresql://postgres:postgres@srv-ud01:5432/postgres",
    connect_args={"options": "-csearch_path=sagrevolution"},
    echo=False,
)


app = Flask(__name__)
CORS(app)


# app = Flask(__name__)
# api = Api(
#     app,
#     version="1.0",
#     title="Sagrevolution API",
#     description="A Food and Beverage Ordering system for Friulan events",
# )

# ns = api.namespace("kiosk", description="Kiosk operations")


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/items/", methods=["GET"])
def get_items():
    with Session(engine) as session:
        items = session.query(Item).all()
        return jsonify(
            data={"items": [item.to_dict() for item in items]},
            status=200,
            mimetype="application/json",
        )
    return jsonify(data={"items": []}, status=200, mimetype="application/json")


@app.route("/item/<item_id>/", methods=["GET"])
def get_item(item_id: str):
    with Session(engine) as session:
        item = session.query(Item).where(Item.id == item_id).one_or_none()
        return jsonify(
            data=item.to_dict(),
            status=200,
            mimetype="application/json",
        )
    return jsonify(data={}, status=200, mimetype="application/json")


@app.route("/order/", methods=["GET"])
def order(order: dict = None):
    with Session(engine) as session:
        pizza = (
            session.query(Item)
            .filter(Item.name == "Hawaiian Pizza")
            .one_or_none()
        )
        beer = (
            session.query(Item)
            .filter(Item.name == "Beer (40cl)")
            .one_or_none()
        )

        order = Order(
            payment_method=PaymentMethodType.CASH,
            total_paid=50.0,
            departments_orders=[
                DepartmentOrder(
                    department=pizza.department,
                    department_order_items=[
                        DepartmentOrderItem(item=pizza, quantity=1),
                    ],
                ),
                DepartmentOrder(
                    department=beer.department,
                    department_order_items=[
                        DepartmentOrderItem(item=beer, quantity=2),
                    ],
                ),
            ],
        )
        session.add(order)
        session.commit()
    return jsonify(
        data={"order": order.to_dict()},
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
