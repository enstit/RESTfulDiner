<div align="center">
  <h1 align="center">🛼 RESTful Diner</h2>
</div>

> [!NOTE]
> This repository is part of the final exam for the *Advanced Data Management
> And Curation* course held by professors Andrea Bignamini, Marco Molinaro,
> Marco Frailis and Stefano Cozzini at
> [University of Trieste](https://www.units.it/en) in the 2024-2025 academic
> year.

In this project, we are going to build a RESTful APIs service to host an Open
Data[^1]-compliant repository to host data about food orders at a restaurant.

## Usage

### Authentication

To interact with the APIs, the first step is to login into the system with a
valid user (we can use the user `John` with password `password`):
```bash
curl -X POST http://127.0.0.1:5000/api/v1/login -H "Content-Type: application/json" -d '{"username": "John", "password": "test"}'

{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MTA3Nzc3NCwianRpIjoiZWY0MzQzZDQtZGQwYS00ZTA0LTlkYjQtZGI2MGZhNDBkNjcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImMxYTk5OGNlLWY4MTYtMTFlZi04Yjc1LTAyNDJhYzE1MDAwMiIsIm5iZiI6MTc0MTA3Nzc3NCwiY3NyZiI6ImFjODdkZjcxLWYzMDQtNDE4Ni05NWQxLWQwM2FhOTY0YmE0ZSIsImV4cCI6MTc0MTA3ODY3NH0.SXFig78k2T4tq35lLA8inu4hDD8ZXVbQ9K_i4OeZj-I"}
```
This should return an object with an `access_token` as above, to be used for all
the next operations with the system.

> [!IMPORTANT]
> At the current state of development, authentication is not being implemented
> on the APIs endpoints. This has to be implemented in future releases.

### Insertions

To insert a new printer in the system:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/printers -H "Content-Type: application/json" -d '{"name": "Printer 01", "mac_address": "00-B0-D0-63-C2-26", "ip_address": "10.0.0.1"}'
```

```bash
curl -X POST http://127.0.0.1:5000/api/v1/departments -H "Content-Type: application/json" -d '{"name": "Kitchen"}'
```

```bash
curl -X POST http://127.0.0.1:5000/api/v1/items -H "Content-Type: application/json" -d '{"name": "Spaghetti Bolognese", "description": "Best Italian Spaghetti ever", "department": "Kitchen", "menu_section": "FIRST_COURSES", "price": 12.50, "initial_status": "COMPLETED"}'
```

### GET operations
```bash
curl -X GET http://127.0.0.1:5000/api/v1/printers/name=Printer%2001
curl -X GET http://127.0.0.1:5000/api/v1/departments/name=Cucina
curl -X GET http://127.0.0.1:5000/api/v1/items/name=Spaghetti%20Bolognese
```

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE)
file for details.


[^1]: Berners-Lee, T., "Linked Data", *w3.org*, 2006. [https://www.w3.org/DesignIssues/LinkedData.html](https://www.w3.org/DesignIssues/LinkedData.html).
