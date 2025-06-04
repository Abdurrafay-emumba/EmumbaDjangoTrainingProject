# API Documentation – Similar Task Matching

---

## 1. General Information

| Field              | Value                                                                     |
|--------------------|---------------------------------------------------------------------------|
| **API Name**       | Similar Task Matching                                                     |
| **Endpoint**       | `/user/tasks/SimilarTask/`                                                |
| **Method**         | GET                                                                       |
| **Authentication** | Yes                                                                       |
| **Pagination**     | Yes                                                                       |
| **Caching**        | No                                                                        |
| **Purpose**        | Returns pairs of tasks with similar descriptions owned by the same user.  |

---

## 2. Request Details

### Headers

```http
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### Query Parameters

| Parameter | Type | Required | Description                        | Example   |
|-----------|------|----------|------------------------------------|-----------|
| page      | int  | No       | Page number for paginated results | `page=1`  |

### Sample Request

```http
GET /user/tasks/SimilarTask/?page=1
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "task_1": {
        "id": 4,
        "title": "Write article",
        "description": "Write about Django REST framework",
        "start_date": "2025-06-01",
        "due_date": "2025-06-05",
        "completion_date": null,
        "completion_status": false,
        "user_id": 3,
        "file_attachment": null
      },
      "task_2": {
        "id": 5,
        "title": "Framework article",
        "description": "Django REST framework overview",
        "start_date": "2025-06-02",
        "due_date": "2025-06-06",
        "completion_date": null,
        "completion_status": false,
        "user_id": 3,
        "file_attachment": null
      }
    }
  ]
}
```

### Response Fields

| Field     | Type   | Description                                              |
|-----------|--------|----------------------------------------------------------|
| task_1    | object | One task with description similar to another             |
| task_2    | object | Another task whose description overlaps with task_1      |
| count     | int    | Total number of similar task pairs                       |
| results   | array  | Paginated list of similar task pairs                     |

---

## 4. Error Responses

### 401 Unauthorized

**Cause**: Missing or invalid authentication token/session  
**Example**:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 5. Caching

| Property               | Description                                              |
|------------------------|----------------------------------------------------------|
| **Cached**             | No                                                       |
| **Cache Duration**     | N/A                                                      |
| **Cache Storage**      | N/A                                                      |
| **Invalidation Rules** | N/A                                                      |
| **QA Notes**           | Add/edit similar tasks and verify output updates         |

---
