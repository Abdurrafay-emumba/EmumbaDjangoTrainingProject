# API Documentation – Get All Tasks (Paginated)

---

## 1. General Information

| Field              | Value                                                      |
|--------------------|------------------------------------------------------------|
| **API Name**       | Get All Tasks                                              |
| **Endpoint**       | `/user/tasks/getAllTask/`                                  |
| **Method**         | GET                                                        |
| **Authentication** | Yes                                                        |
| **Pagination**     | True                                                       |
| **Caching**        | No                                                         |
| **Purpose**        | Retrieves all tasks created by the authenticated user.     |

---

## 2. Request Details

### Headers

```http
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### Query Parameters

| Parameter | Type | Required | Description                          | Example   |
|-----------|------|----------|--------------------------------------|-----------|
| page      | int  | No       | Page number for paginated results    | `page=1`  |

### Sample Request

```http
GET /user/tasks/getAllTask/?page=1
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
      "title": "Finish assignment",
      "description": "Complete the math assignment",
      "start_date": "2025-06-01",
      "due_date": "2025-06-05",
      "completion_date": null,
      "completion_status": false,
      "user_id": 4,
      "file_attachment": null
    },
    ...
  ]
}
```

### Response Fields

| Field       | Type     | Description                                |
|-------------|----------|--------------------------------------------|
| count       | integer  | Total number of user tasks                 |
| next        | string   | URL to the next page of results            |
| previous    | string   | URL to the previous page of results        |
| results     | array    | List of task objects (paginated)           |

---

## 4. Error Responses

### 401 Unauthorized

**Cause**: Request made without proper authentication  
**Example**:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 5. Caching

| Property               | Description                                           |
|------------------------|-------------------------------------------------------|
| **Cached**             | No                                                    |
| **Cache Duration**     | N/A                                                   |
| **Cache Storage**      | N/A                                                   |
| **Invalidation Rules** | N/A                                                   |
| **QA Notes**           | Test multiple pages, ensure only user's tasks appear  |

---
