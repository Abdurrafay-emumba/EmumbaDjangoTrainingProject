# API Documentation – Initiate Forgotten Password Reset

---

## 1. General Information

| Field              | Value                                                                |
|--------------------|----------------------------------------------------------------------|
| **API Name**       | Initiate Forgotten Password Reset                                    |
| **Endpoint**       | `/initiate_reset_forgotten_password/`                                |
| **Method**         | POST                                                                 |
| **Authentication** | No                                                                   |
| **Pagination**     | False                                                                |
| **Caching**        | No                                                                   |
| **Purpose**        | Sends a password reset email with tokenized reset link to the user.  |

---

## 2. Request Details

### Headers

```http
Content-Type: application/json
Accept: application/json
```

### Request Body Parameters

| Parameter | Type   | Required | Description          | Constraints        |
|-----------|--------|----------|----------------------|--------------------|
| email     | string | Yes      | Registered user email | Must be valid email|

### Sample Request

```json
{
  "email": "john@example.com"
}
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "Password Reset Email Sent!"
}
```

### Response Fields

| Field    | Type   | Description                             |
|----------|--------|-----------------------------------------|
| message  | string | Confirmation that the email was sent    |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: Missing or invalid email, or user does not exist  
**Example**:

```json
{
  "error": "OurUser matching query does not exist."
}
```

---

## 5. Caching

| Property               | Description                                                    |
|------------------------|----------------------------------------------------------------|
| **Cached**             | No                                                             |
| **Cache Duration**     | N/A                                                            |
| **Cache Storage**      | N/A                                                            |
| **Invalidation Rules** | N/A                                                            |
| **QA Notes**           | Test valid/invalid email; check token link in email if received|

---
