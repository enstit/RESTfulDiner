<div align="center">
  <h1 align="center">🛼 RESTful Diner</h2>
</div>

> [!NOTE]
> This repository is part of the final exam for the _Advanced Data Management
> And Curation_ course held by professors Andrea Bignamini, Marco Molinaro
> ([`@molinaro-m`](https://github.com/molinaro-m)), Marco Frailis and Stefano
> Cozzini ([`@cozzini`](https://github.com/cozzini)) at
> [University of Trieste](https://www.units.it/en) in the 2024-2025 Academic
> Year.
> The exam was evaluated with the maximum vote (30 over 30).

In this project, we are going to build a RESTful APIs service to host data
about food orders at any food business.


## Usage

### Start up

The application is based on Docker containers. In particular, the system is
composed of two services: a `database` service to persist data, and an `app`
service with all the REST APIs application.

To run the application, we can use the [compose file](compose.yml) already
defined and start it in detached mode:

```bash
foo@bar:~$ git clone git@github.com:enstit/RESTfulDiner.git
foo@bar:~$ cd RESTfulDiner
foo@bar:~$ docker compose up --detach
```

### Authentication

To interact with the APIs, we firstly need to login into the system with a
valid admin user.

First of all, we need to recover the list of configured users in the system
```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/users

[
    {
        "url": "http://127.0.0.1:5000/api/v1/users/5b11618c-51f5-8000-8000-bcd930cbd30d",
        "id": "5b11618c-51f5-8000-8000-bcd930cbd30d",
        "username": "admin",
        "role": "ADMIN"
    },
    {
        "url": "http://127.0.0.1:5000/api/v1/users/5b11618c-51f5-8000-8000-bcd93dab7afd",
        "id": "5b11618c-51f5-8000-8000-bcd93dab7afd",
        "username": "operator",
        "role": "OPERATOR"
    }
]
```

```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/events

[
    {
        "url": "http://127.0.0.1:5000/api/v1/events/5b11618c-51f5-8000-8000-1bacec79bda0",
        "id": "5b11618c-51f5-8000-8000-1bacec79bda0",
        "name": "Sample Event"
    }
]
```
Now we can select a user with `ADMIN` role, for example the `admin` user, and
then call its `login` action providing the password and the kiosk selected for
the access:

```bash
foo@bar:~$ curl -X POST http://127.0.0.1:5000/api/v1/users/5b11618c-51f5-8000-8000-bcd930cbd30d/login?event_id=5b11618c-51f5-8000-8000-1bacec79bda0 \
foo@bar:~$ -H "Content-Type: application/json" \
foo@bar:~$ -d '{"password": "admin"}'

{"access_token": "<access_token>"}
```

This should return an object with an `access_token` as above, to be used for
all restriced operations within the system.

> [!IMPORTANT]
> We need to log in in the system with a user with admin role in order to
> execute **POST**, **PUT**, **PATCH** and **DELETE** operations.
> For simple **GET** operations, we can also log in as a user with operative
> role (e.g., user `operator` with password `operator`).

### System querying

#### `POST` operations

Let's start by inserting a new Department in the database:

```bash
foo@bar:~$ curl -X POST http://127.0.0.1:5000/api/v1/departments \
foo@bar:~$ -H "Authorization: Bearer <access_token>" \
foo@bar:~$ -H "Content-Type: application/json" \
foo@bar:~$ -d '{"name": "Cuisine"}'

{
    "url": "http://127.0.0.1:5000/api/v1/departments/5b11618c-51f5-8000-8000-203b8c4a1499",
    "id": "5b11618c-51f5-8000-8000-203b8c4a1499",
    "name": "Cuisine",
    "printer_url": null
}
```

#### `GET` operations

Now, if we recover all the Departments from the database, the newly inserted
`Cuisine` should be present. Let's verify it with:

```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/departments \
foo@bar:~$ -H "Authorization: Bearer <access_token>"

[
    {
        "url": "http://127.0.0.1:5000/api/v1/departments/5b11618c-51f5-8000-8000-203b8c4a1499",
        "id": "5b11618c-51f5-8000-8000-203b8c4a1499",
        "name": "Cuisine",
        "printer_url": null
    }
]
```

#### `PUT` operations

Mmmh, the term `Cuisine` comes from the French and can not be understand by
everyone. Better to change the Department name to a more universal `Kitchen`.
In order to do that, we simply need to use a **PUT** operation:

```bash
foo@bar:~$ curl -X PUT http://127.0.0.1:5000/api/v1/departments/5b11618c-51f5-8000-8000-203b8c4a1499 \
foo@bar:~$ -H "Authorization: Bearer <access_token>" \
foo@bar:~$ -H "Content-Type: application/json" \
foo@bar:~$ -d '{"name": "Kitchen"}'

{
    "url": "http://127.0.0.1:5000/api/v1/departments/5b11618c-51f5-8000-8000-203b8c4a1499",
    "id": "5b11618c-51f5-8000-8000-203b8c4a1499",
    "name": "Kitchen",
    "printer_url": null
}
```

#### `PATCH` operations

Better now. But the **PUT** operation is useful when we want to modify an object
by providing the whole representation of it, so if the department had a printer
associated, the command above would have overwritten it.
If we take a look at the printers in the system (with a **GET**
request at `http://127.0.0.1:5000/api/v1/printers`) we will see that there is a
`KitchenPrinter` with id `5b11618c-51f5-8000-8000-04e446b2b7c1` that really
sounds to be the printer associated with the Department we just created.

```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/printers \
foo@bar:~$ -H "Authorization: Bearer <access_token>"

[
    {
        "url": "http://127.0.0.1:5000/api/v1/printers/5b11618c-51f5-8000-8000-04e446b2b7c1",
        "id": "5b11618c-51f5-8000-8000-04e446b2b7c1",
        "name": "KitchenPrinter",
        "mac_address": "32:1c:35:93:4e:07",
        "ip_address": "10.172.54.145"
    }
]
```

Here's where the **PATCH** operation comes in our hand:

```bash
foo@bar:~$ curl -X PATCH http://127.0.0.1:5000/api/v1/departments/5b11618c-51f5-8000-8000-203b8c4a1499 \
foo@bar:~$ -H "Authorization: Bearer <access_token>" \
foo@bar:~$ -H "Content-Type: application/json" \
foo@bar:~$ -d '{"printer_id": "5b11618c-51f5-8000-8000-04e446b2b7c1"}'

{
    "url": "http://127.0.0.1:5000/api/v1/departments/5b11618c-51f5-8000-8000-203b8c4a1499",
    "id": "5b11618c-51f5-8000-8000-203b8c4a1499",
    "name": "Kitchen",
    "printer_url": "http://127.0.0.1:5000/api/v1/printers/5b11618c-51f5-8000-8000-04e446b2b7c1"
}
```

And as you can see, the department has been updated with printer link.


## Next steps

- [ ] Use [`marshmallow`](https://github.com/marshmallow-code/marshmallow)
      for serilization and deserialization of model objects
- [ ] Implement `DELETE` methods for the resources
- [ ] Improve authentication mechanism by saving client token to cache, also
      adding expiration time for a single authentication


## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE)
file for details.

