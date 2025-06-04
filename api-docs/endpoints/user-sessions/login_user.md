# API Documentation – User Login

---

## 1. General Information

| Field              | Value                                                           |
|--------------------|-----------------------------------------------------------------|
| **API Name**       | User Login                                                      |
| **Endpoint**       | `/login/`                                                       |
| **Method**         | POST                                                            |
| **Authentication** | No                                                              |
| **Pagination**     | False                                                           |
| **Caching**        | No                                                              |
| **Purpose**        | Logs in the user using username/email and password combination. |

---

## 2. Request Details

### Headers

```http
Content-Type: application/json
Accept: application/json
```

### Request Body Parameters

| Parameter         | Type   | Required | Description                                   | Constraints         |
|-------------------|--------|----------|-----------------------------------------------|---------------------|
| username          | string | Yes      | Either the username or email of the user      | Must match existing |
| password          | string | Yes      | Password of the user                          | Required            |

> Note: The parameter `username` can be either a username **or** an email address.

### Sample Request

```json
{
  "username": "john@example.com",
  "password": "securePassword123"
}
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "Login successful!",
  "username": "john_doe"
}
```

### Response Fields

| Field     | Type   | Description                            |
|-----------|--------|----------------------------------------|
| message   | string | Confirmation of successful login       |
| username  | string | The username of the logged-in user     |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: Missing `username` or `password`  
**Example**:

```json
{
  "error": "Username (or Email) and password are required."
}
```

### 401 Unauthorized

**Cause**: Invalid login credentials  
**Example**:

```json
{
  "error": "Invalid credentials."
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
| **QA Notes**           | Test with valid/invalid username and email combinations   |

---
