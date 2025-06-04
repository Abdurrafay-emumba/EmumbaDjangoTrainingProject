# API Documentation – User Registration

---

## 1. General Information

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| **API Name**       | User Registration                                                     |
| **Endpoint**       | `/register/`                                                          |
| **Method**         | POST                                                                  |
| **Authentication** | No                                                                    |
| **Pagination**     | False                                                                 |
| **Caching**        | No                                                                    |
| **Purpose**        | Registers a new user and sends a verification email                   |

---

## 2. Request Details

### Headers

```http
Content-Type: application/json
Accept: application/json
```

### Request Body Parameters

| Parameter   | Type   | Required | Description                 | Constraints                |
|-------------|--------|----------|-----------------------------|----------------------------|
| username    | string | Yes      | Unique username             | Required, must be unique   |
| email       | string | Yes      | User's email                | Must be unique & valid     |
| password    | string | Yes      | User's password             | Write-only, min length 8   |
| first_name  | string | No       | User's first name           | Optional                    |
| last_name   | string | No       | User's last name            | Optional                    |

### Sample Request

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

## 3. Success Response

### HTTP Status

`201 Created`

### Sample Response

```json
{
  "message": "User registered successfully"
}
```

### Response Fields

| Field    | Type   | Description                             |
|----------|--------|-----------------------------------------|
| message  | string | Confirmation of successful registration |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: Missing or invalid fields, duplicate email, etc.  
**Example**:

```json
{
  "email": ["user with this email already exists."]
}
```

---

## 5. Caching

| Property               | Description                                               |
|------------------------|-----------------------------------------------------------|
| **Cached**             | No                                                        |
| **Cache Duration**     | N/A                                                       |
| **Cache Storage**      | N/A                                                       |
| **Invalidation Rules** | N/A                                                       |
| **QA Notes**           | Test duplicate email and password constraints             |

---
