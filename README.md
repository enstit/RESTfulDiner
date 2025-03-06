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
valid user (we can use the user `test` with password `test`):
```bash
foo@bar:~$ curl -X POST http://127.0.0.1:5000/api/v1/login -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'

{"access_token": "<access_token>"}
```
This should return an object with an `access_token` as above, to be used for all
the operations of **POST** type with the system.


### System querying

Let's start by inserting a new Department in the database:
```bash
foo@bar:~$ curl -X POST http://127.0.0.1:5000/api/v1/departments -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"name": "Kitchen"}'

{"id": "1a99585a-fa94-11ef-949e-0242ac120003", "name": "Kitchen"}
```

Now, if we recover all the Departments from the database, the newly inserted
`Kitchen` should be present. Let's verify it with:
```bash
foo@bar:~$ curl -X GET http://127.0.0.1:5000/api/v1/departments

[{"id": "1a99585a-fa94-11ef-949e-0242ac120003", "name": "Kitchen"}, {"id": "2ed2ad8a-fa94-11ef-84db-0242ac120003", "name": "Beverage"}]
```

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE)
file for details.


[^1]: Berners-Lee, T., "Linked Data", *w3.org*, 2006. [https://www.w3.org/DesignIssues/LinkedData.html](https://www.w3.org/DesignIssues/LinkedData.html).
