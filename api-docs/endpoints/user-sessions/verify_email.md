# API Documentation – Verify Email

---

## 1. General Information

| Field              | Value                                                          |
|--------------------|----------------------------------------------------------------|
| **API Name**       | Verify Email                                                   |
| **Endpoint**       | `/verify-email/<uidb64>/<token>/`                              |
| **Method**         | GET                                                            |
| **Authentication** | No                                                             |
| **Pagination**     | False                                                          |
| **Caching**        | No                                                             |
| **Purpose**        | Confirms user email via verification link with token & user ID |

---

## 2. Request Details

### Headers

```http
Accept: application/json
```

### Request Body Parameters

N/A — this endpoint uses **URL parameters** only.

| Parameter | Type   | Required | Description                        | Constraints         |
|-----------|--------|----------|------------------------------------|---------------------|
| uidb64    | string | Yes      | Base64-encoded user ID             | Must be valid       |
| token     | string | Yes      | Email verification token           | Must be valid & not expired |

### Sample Request

```http
GET /verify-email/MTE3/tokenvalue123/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response (first-time verification)

```json
{
  "message": "Email successfully verified!"
}
```

### Sample Response (already verified)

```json
{
  "message": "Email already verified."
}
```

### Response Fields

| Field    | Type   | Description                        |
|----------|--------|------------------------------------|
| message  | string | Confirmation of verification state |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: Invalid or expired token, or bad UID  
**Example**:

```json
{
  "error": "Invalid or expired token."
}
```

or

```json
{
  "error": "Invalid user ID."
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
| **QA Notes**           | Try verifying twice and check for "already verified" msg |

---
