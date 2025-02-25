<div align="center">
  <h1 align="center">🛼 RESTful Diner</h2>
</div>

In this project...

## Usage

### POST operations
```bash
curl -X POST http://127.0.0.1:5007/api/v1/user -H "Content-Type: application/json" -d '{"username": "John"}'
```

### GET operations
```bash
curl -X GET http://127.0.0.1:5007/api/v1/user/John
```