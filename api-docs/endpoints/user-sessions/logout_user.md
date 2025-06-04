# API Documentation – Logout User

---

## 1. General Information

| Field              | Value                                                         |
|--------------------|---------------------------------------------------------------|
| **API Name**       | Logout User                                                   |
| **Endpoint**       | `/logout/`                                                    |
| **Method**         | POST                                                          |
| **Authentication** | Yes (Session-based)                                           |
| **Pagination**     | False                                                         |
| **Caching**        | No                                                            |
| **Purpose**        | Logs out the currently authenticated user and clears session. |

---

## 2. Request Details

### Headers

```http
Content-Type: application/json
Accept: application/json
Authorization: Session or Cookie header (used implicitly by browser/Postman session)
```

### Request Body Parameters

None.

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "Logout successful. User id: 42"
}
```

### Response Fields

| Field    | Type   | Description                           |
|----------|--------|---------------------------------------|
| message  | string | Confirmation message with user ID     |

---

## 4. Error Responses

N/A — The view gracefully handles logout if the user is authenticated.

---

## 5. Caching

| Property               | Description                                           |
|------------------------|-------------------------------------------------------|
| **Cached**             | No                                                    |
| **Cache Duration**     | N/A                                                   |
| **Cache Storage**      | N/A                                                   |
| **Invalidation Rules** | Session is invalidated via logout                    |
| **QA Notes**           | Ensure session cookie is removed post-logout          |

---
