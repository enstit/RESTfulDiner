<div align="center">
  <h1 align="center">🛼 RESTful Diner</h2>
</div>

> [!NOTE]
> This repository is part of the final exam for the *Advanced Data Management
> And Curation* course held by professors Andrea Bignamini, Marco Molinaro
> ([`@molinaro-m`](https://github.com/molinaro-m)), Marco Frailis and Stefano
> Cozzini ([`@cozzini`](https://github.com/cozzini)) at
> [University of Trieste](https://www.units.it/en) in the 2024-2025 Academic
> Year.

In this project, we are going to build a RESTful APIs service to host an Open
Data[^1]-compliant repository to host data about food orders at a restaurant.


## Usage

### Authentication

To interact with the APIs, the first step is to login into the system with a
valid admin user (we can use the user `admin` with password `admin`):
```bash
foo@bar:~$ curl -X POST http://127.0.0.1:5000/api/v1/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}'

{"access_token": "<access_token>"}
```
This should return an object with an `access_token` as above, to be used for all
the operations of **POST** type with the system.

> [!IMPORTANT]
> We need to log in in the system with a user with admin role in order to
> execute **POST**, **PUT**, **PATCH** and **DELETE** operations.
> For simple **GET** operations, we can also log in as a user with operative
> role (e.g., user `test` with password `test`).

### System querying

Let's start by inserting a new Department in the database:
```bash
foo@bar:~$ curl -X POST http://127.0.0.1:5000/api/v1/departments -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"name": "Cuisine"}'

{"id": "1a99585a-fa94-11ef-949e-0242ac120003", "name": "Cuisine", "printer": null}
```

Now, if we recover all the Departments from the database, the newly inserted
`Cuisine` should be present. Let's verify it with:
```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/departments

[{"id": "1a99585a-fa94-11ef-949e-0242ac120003", "name": "Cuisine", "printer": null}, {"id": "2ed2ad8a-fa94-11ef-84db-0242ac120003", "name": "Beverage", "printer": null}]
```

Mmmh, the term `Cuisine` comes from the French and can not be understand by
everyone. Better to change the Department name to a more universal `Kitchen`.
In order to do that, we simply need to use a **PUT** operation:

```bash
foo@bar:~$ curl -X PUT http://127.0.0.1:5000/api/v1/departments/1a99585a-fa94-11ef-949e-0242ac120003 -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"name": "Kitchen"}'

{"id": "1a99585a-fa94-11ef-949e-0242ac120003", "name": "Kitchen", "printer": null}
```

Better now. But if we take a look at the printers in the system (with a **GET**
request at `http://127.0.0.1:5000/api/v1/printers`) we will see that there is a
`KitchenPrinter` with id `6ab08ed0-fb2f-11ef-96b4-0242ac120003` that really
sounds to be the printer associated with the Department we just created. Here's
where the **PATCH** operation comes in our hand:

```bash
foo@bar:~$ curl -X PATCH http://127.0.0.1:5000/api/v1/departments/7924ec72-fb2f-11ef-8f2c-0242ac120003 -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"printer_id": "6ab08ed0-fb2f-11ef-96b4-0242ac120003"}'

{"id": "1a99585a-fa94-11ef-949e-0242ac120003", "name": "Kitchen", "printer": "6ab08ed0-fb2f-11ef-96b4-0242ac120003"}
```

And as you can see, the department has been updated with printer link.


## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE)
file for details.


[^1]: Berners-Lee, T., "Linked Data", *w3.org*, 2006. [https://www.w3.org/DesignIssues/LinkedData.html](https://www.w3.org/DesignIssues/LinkedData.html).
