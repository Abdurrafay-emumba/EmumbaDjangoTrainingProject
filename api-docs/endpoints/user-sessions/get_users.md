# API Documentation – Get All Users (Paginated)

---

## 1. General Information

| Field              | Value                                                     |
|--------------------|-----------------------------------------------------------|
| **API Name**       | Get All Users                                             |
| **Endpoint**       | `/get_users/`                                             |
| **Method**         | GET                                                       |
| **Authentication** | Yes (Session or Token-based, depending on backend config) |
| **Pagination**     | True                                                      |
| **Caching**        | No                                                        |
| **Purpose**        | Returns a paginated list of all registered users.         |

---

## 2. Request Details

### Headers

```http
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### Query Parameters

| Parameter | Type   | Required | Description                           | Example     |
|-----------|--------|----------|---------------------------------------|-------------|
| page      | int    | No       | Page number for pagination            | `page=1`    |

### Sample Request

```http
GET /get_users/?page=1
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "first_name": "Admin",
      "last_name": "User",
      "is_email_verified": true,
      "account_date_creation": "2024-01-01",
      ...
    },
    {
      "id": 2,
      "username": "jane_doe",
      "email": "jane@example.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "is_email_verified": true,
      "account_date_creation": "2024-01-05",
      ...
    }
  ]
}
```

### Response Fields

| Field    | Type       | Description                                      |
|----------|------------|--------------------------------------------------|
| count    | integer    | Total number of users                           |
| next     | string     | Link to next page (null if none)                |
| previous | string     | Link to previous page (null if none)            |
| results  | array      | List of user objects (paginated)                |

---

## 4. Error Responses

### 401 Unauthorized

**Cause**: Request made without a valid session or token  
**Example**:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 5. Caching

| Property               | Description                                            |
|------------------------|--------------------------------------------------------|
| **Cached**             | No                                                     |
| **Cache Duration**     | N/A                                                    |
| **Cache Storage**      | N/A                                                    |
| **Invalidation Rules** | N/A                                                    |
| **QA Notes**           | Test pagination (e.g., page=1, page=2) and auth token  |

---
