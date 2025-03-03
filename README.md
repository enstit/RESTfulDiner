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

### POST operations
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users -H "Content-Type: application/json" -d '{"username": "John", "password": "test", "role": "OPERATOR"}'
```

```bash
curl -X POST http://127.0.0.1:5000/api/v1/printers -H "Content-Type: application/json" -d '{"name": "Printer 01", "mac_address": "00-B0-D0-63-C2-26", "ip_address": "10.0.0.1"}'
```

```bash
curl -X POST http://127.0.0.1:5000/api/v1/departments -H "Content-Type: application/json" -d '{"name": "Cucina"}'
```

```bash
curl -X POST http://127.0.0.1:5000/api/v1/items -H "Content-Type: application/json" -d '{"name": "Spaghetti Bolognese", "description": "Best Italian Spaghetti ever", "department": "Cucina", "menu_section": "FIRST_COURSES", "price": 12.50, "initial_status": "COMPLETED"}'
```

### GET operations
```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/username=John
curl -X GET http://127.0.0.1:5000/api/v1/printers/name=Printer%2001
curl -X GET http://127.0.0.1:5000/api/v1/departments/name=Cucina
curl -X GET http://127.0.0.1:5000/api/v1/items/name=Spaghetti%20Bolognese
```

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.


[^1]: Berners-Lee, T., "Linked Data", *w3.org*, 2006. [https://www.w3.org/DesignIssues/LinkedData.html](https://www.w3.org/DesignIssues/LinkedData.html).
