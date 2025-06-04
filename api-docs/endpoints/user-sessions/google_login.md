# API Documentation – Google Login

---

## 1. General Information

| Field              | Value                                                                  |
|--------------------|------------------------------------------------------------------------|
| **API Name**       | Google OAuth2 Login                                                    |
| **Endpoint**       | `/google-login/`                                                       |
| **Method**         | POST                                                                   |
| **Authentication** | No                                                                     |
| **Pagination**     | False                                                                  |
| **Caching**        | No                                                                     |
| **Purpose**        | Authenticates a user using Google OAuth2. Creates account if not exists |

---

## 2. Request Details

### Headers

```http
Content-Type: application/json
Accept: application/json
```

### Request Body Parameters

| Parameter | Type   | Required | Description                       | Constraints                     |
|-----------|--------|----------|-----------------------------------|---------------------------------|
| token     | string | Yes      | Google ID token                   | Must be valid OAuth2 token      |

### Sample Request

```json
{
  "token": "ya29.a0AfH6SMCQ..."
}
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "Login successful",
  "username": "john_doe",
  "email": "john@example.com",
  "created": true
}
```

### Response Fields

| Field     | Type    | Description                                     |
|----------|---------|-------------------------------------------------|
| message  | string  | Success message                                 |
| username | string  | Google account’s full name                      |
| email    | string  | Google account’s email                          |
| created  | boolean | `true` if new account was created, else `false` |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: Missing or incomplete token  
**Example**:

```json
{
  "error": "Missing Google ID token"
}
```

or

```json
{
  "error": "Email not available in token"
}
```

### 401 Unauthorized

**Cause**: Invalid or expired token  
**Example**:

```json
{
  "error": "Invalid token"
}
```

---

## 5. Caching

| Property               | Description                                                     |
|------------------------|-----------------------------------------------------------------|
| **Cached**             | No                                                              |
| **Cache Duration**     | N/A                                                             |
| **Cache Storage**      | N/A                                                             |
| **Invalidation Rules** | N/A                                                             |
| **QA Notes**           | Try with expired/forged token, confirm account creation logic   |

---
