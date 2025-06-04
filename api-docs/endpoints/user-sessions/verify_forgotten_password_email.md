# API Documentation – Verify Forgotten Password Email

---

## 1. General Information

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| **API Name**       | Verify Forgotten Password Email                                       |
| **Endpoint**       | `/verify_forgotten_password_email/<uidb64>/<token>/`                 |
| **Method**         | POST                                                                  |
| **Authentication** | No                                                                    |
| **Pagination**     | False                                                                 |
| **Caching**        | No                                                                    |
| **Purpose**        | Validates the password reset token and sets a new user password       |

---

## 2. Request Details

### Headers

```http
Content-Type: application/json
Accept: application/json
```

### Request Body Parameters

| Parameter     | Type   | Required | Description                     | Constraints         |
|---------------|--------|----------|---------------------------------|---------------------|
| new_password  | string | Yes      | New password to be set          | Should be secure    |

> URL Parameters:
- `uidb64`: Base64-encoded user ID
- `token`: Password reset token (must be valid and unexpired)

### Sample Request

```json
{
  "new_password": "MyNewSecurePassword123"
}
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "Password reset successful!"
}
```

### Response Fields

| Field    | Type   | Description                             |
|----------|--------|-----------------------------------------|
| message  | string | Confirmation that password was updated  |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: Invalid or expired token, bad UID, or missing password  
**Example**:

```json
{
  "error": "Invalid user ID."
}
```

or

```json
{
  "error": "Invalid token"
}
```

---

## 5. Caching

| Property               | Description                                                      |
|------------------------|------------------------------------------------------------------|
| **Cached**             | No                                                               |
| **Cache Duration**     | N/A                                                              |
| **Cache Storage**      | N/A                                                              |
| **Invalidation Rules** | N/A                                                              |
| **QA Notes**           | Use both valid and expired tokens, check behavior on re-use      |

---
