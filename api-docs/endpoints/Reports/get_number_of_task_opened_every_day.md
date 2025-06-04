# API Documentation – Task Opened Per Weekday Report

---

## 1. General Information

| Field              | Value                                                                       |
|--------------------|-----------------------------------------------------------------------------|
| **API Name**       | Task Opened Per Weekday Report                                              |
| **Endpoint**       | `/user/tasks/get_number_of_task_opened_every_day/`                          |
| **Method**         | GET                                                                         |
| **Authentication** | Yes                                                                         |
| **Pagination**     | No                                                                          |
| **Caching**        | Yes                                                                         |
| **Purpose**        | Returns how many tasks were opened (created) on each day of the week.       |

---

## 2. Request Details

### Headers

```http
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### Request Body Parameters

None

### Sample Request

```http
GET /user/tasks/get_number_of_task_opened_every_day/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
[
  { "weekday": 2, "task_count": 5 },
  { "weekday": 3, "task_count": 3 },
  { "weekday": 5, "task_count": 2 }
]
```

### Response Fields

| Field       | Type    | Description                                                        |
|-------------|---------|--------------------------------------------------------------------|
| weekday     | integer | Day of the week (`1=Sunday`, `2=Monday`, ..., `7=Saturday`)        |
| task_count  | integer | Number of tasks created (start_date) on that weekday               |

---

## 4. Error Responses

### 500 Internal Server Error

**Cause**: Unexpected database or annotation error  
**Example**:

```json
{
  "Exception occurred": "invalid field name for annotation"
}
```

---

## 5. Caching

| Property               | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| **Cached**             | Yes                                                                                                  |
| **Cache Duration**     | 15 minutes                                                                                           |
| **Cache Storage**      | Redis (primary); falls back to Django’s default cache if Redis is unavailable                       |
| **Invalidation Rules** | Cache is invalidated when:<br> - A task is created<br> - A task is completed<br> - A task is deleted |
| **QA Notes**           | Create tasks on different weekdays and confirm updated output after cache clears                    |

---
