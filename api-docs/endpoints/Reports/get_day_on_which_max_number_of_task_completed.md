# API Documentation – Day With Maximum Task Completion

---

## 1. General Information

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| **API Name**       | Day With Maximum Task Completion                                      |
| **Endpoint**       | `/user/tasks/get_day_on_which_max_number_of_task_completed/`         |
| **Method**         | GET                                                                   |
| **Authentication** | Yes                                                                   |
| **Pagination**     | No                                                                    |
| **Caching**        | Yes                                                                   |
| **Purpose**        | Returns the date on which the user completed the most tasks.          |

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
GET /user/tasks/get_day_on_which_max_number_of_task_completed/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "completion_date": "2025-06-03",
  "task_count": 4
}
```

### Response Fields

| Field           | Type    | Description                                               |
|------------------|---------|-----------------------------------------------------------|
| completion_date | string  | Date on which the most tasks were completed (`YYYY-MM-DD`)|
| task_count      | integer | Number of tasks completed on that day                     |

---

## 4. Error Responses

### 500 Internal Server Error

**Cause**: Unexpected failure in query or data logic  
**Example**:

```json
{
  "Exception occurred": "division by zero"
}
```

---

## 5. Caching

| Property               | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| **Cached**             | Yes                                                                                                  |
| **Cache Duration**     | 15 minutes                                                                                           |
| **Cache Storage**      | Redis (primary); falls back to Django’s cache if Redis is unavailable                               |
| **Invalidation Rules** | Cache is invalidated when:<br> - A task is created<br> - A task is completed<br> - A task is deleted |
| **QA Notes**           | Complete tasks on different days and confirm this API updates result after cache clears             |

---
