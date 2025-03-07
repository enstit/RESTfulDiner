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

#### `POST` operations
Let's start by inserting a new Department in the database:
```bash
foo@bar:~$ curl -X POST http://127.0.0.1:5000/api/v1/departments -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"name": "Cuisine"}'

{
    "@context": {
        "schema": "https://schema.org/",
        "self": "@id",
        "type": "@type",
        "name": "schema:name",
        "printer": {
            "@id": "schema:isRelatedTo",
            "@type": "@id"
        },
        "license": {
            "@id": "schema:license",
            "@type": "@id"
        }
    },
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "data": {
        "self": "http://127.0.0.1:5000/api/v1/departments/851c8de8-fb55-11ef-9aea-0242ac120003",
        "type": "schema:Organization",
        "name": "Cuisine",
        "printer": null
    }
}
```

#### `GET` operations
Now, if we recover all the Departments from the database, the newly inserted
`Cuisine` should be present. Let's verify it with:
```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/departments

{
    "@context": {
        "schema": "https://schema.org/",
        "self": "@id",
        "type": "@type",
        "name": "schema:name",
        "printer": {
            "@id": "schema:isRelatedTo",
            "@type": "@id"
        },
        "license": {
            "@id": "schema:license",
            "@type": "@id"
        }
    },
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "data": [
        {
            "self": "http://127.0.0.1:5000/api/v1/departments/851c8de8-fb55-11ef-9aea-0242ac120003",
            "type": "schema:Organization",
            "name": "Cuisine",
            "printer": null
        }
    ]
}
```

#### `PUT` operations
Mmmh, the term `Cuisine` comes from the French and can not be understand by
everyone. Better to change the Department name to a more universal `Kitchen`.
In order to do that, we simply need to use a **PUT** operation:

```bash
foo@bar:~$ curl -X PUT http://127.0.0.1:5000/api/v1/departments/e5e63c86-fb42-11ef-afda-0242ac120003 -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"name": "Kitchen"}'

{
    "@context": {
        "schema": "https://schema.org/",
        "self": "@id",
        "type": "@type",
        "name": "schema:name",
        "printer": {
            "@id": "schema:isRelatedTo",
            "@type": "@id"
        },
        "license": {
            "@id": "schema:license",
            "@type": "@id"
        }
    },
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "data": {
        "self": "http://127.0.0.1:5000/api/v1/departments/851c8de8-fb55-11ef-9aea-0242ac120003",
        "type": "schema:Organization",
        "name": "Kitchen",
        "printer": null
    }
}
```

#### `PATCH` operations
Better now. But the **PUT** operation is useful when we want to modify an object
by providing the whole representation of it, so if the department had a printer
associated, the command above would have overwritten it.
If we take a look at the printers in the system (with a **GET**
request at `http://127.0.0.1:5000/api/v1/printers`) we will see that there is a
`KitchenPrinter` with id `d2dc99fa-fb42-11ef-929e-0242ac120003` that really
sounds to be the printer associated with the Department we just created.
```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/printers

{
    "@context": {
        "schema": "https://schema.org/",
        "self": "@id",
        "type": "@type",
        "name": "schema:name",
        "mac_address": "schema:macAddress",
        "ip_address": "schema:ipAddress",
        "license": {
            "@id": "schema:license",
            "@type": "@id"
        }
    },
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "data": [
        {
            "self": "http://127.0.0.1:5000/api/v1/printers/67936882-fb55-11ef-b5b9-0242ac120003",
            "type": "Printer",
            "name": "KitchenPrinter",
            "mac_address": "32:1c:35:93:4e:07",
            "ip_address": "10.172.54.145"
        }
    ]
}
```

Here's where the **PATCH** operation comes in our hand:

```bash
foo@bar:~$ curl -X PATCH http://127.0.0.1:5000/api/v1/departments/e5e63c86-fb42-11ef-afda-0242ac120003 -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"printer_id": "d2dc99fa-fb42-11ef-929e-0242ac120003"}'

{
    "@context": {
        "schema": "https://schema.org/",
        "self": "@id",
        "type": "@type",
        "name": "schema:name",
        "printer": {
            "@id": "schema:isRelatedTo",
            "@type": "@id"
        },
        "license": {
            "@id": "schema:license",
            "@type": "@id"
        }
    },
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "data": {
        "self": "http://127.0.0.1:5000/api/v1/departments/851c8de8-fb55-11ef-9aea-0242ac120003",
        "type": "schema:Organization",
        "name": "Kitchen",
        "printer": "http://127.0.0.1:5000/api/v1/printers/67936882-fb55-11ef-b5b9-0242ac120003"
    }
}
```

And as you can see, the department has been updated with printer link.


## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE)
file for details.


[^1]: Berners-Lee, T., "Linked Data", *w3.org*, 2006. [https://www.w3.org/DesignIssues/LinkedData.html](https://www.w3.org/DesignIssues/LinkedData.html).
