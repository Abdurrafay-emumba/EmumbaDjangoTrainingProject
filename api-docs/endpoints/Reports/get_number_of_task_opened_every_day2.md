# API Documentation – Task Opened Per Calendar Day

---

## 1. General Information

| Field              | Value                                                                       |
|--------------------|-----------------------------------------------------------------------------|
| **API Name**       | Task Opened Per Calendar Day                                                |
| **Endpoint**       | `/user/tasks/get_number_of_task_opened_every_day2/`                         |
| **Method**         | GET                                                                         |
| **Authentication** | Yes                                                                         |
| **Pagination**     | No                                                                          |
| **Caching**        | Yes                                                                         |
| **Purpose**        | Returns the number of tasks created on each individual date (calendar day). |

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
GET /user/tasks/get_number_of_task_opened_every_day2/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
[
  { "start_date": "2025-06-01", "task_count": 3 },
  { "start_date": "2025-06-03", "task_count": 1 },
  { "start_date": "2025-06-04", "task_count": 5 }
]
```

### Response Fields

| Field       | Type    | Description                                              |
|-------------|---------|----------------------------------------------------------|
| start_date  | string  | Calendar date the task was created (`YYYY-MM-DD`)       |
| task_count  | integer | Number of tasks opened on that date                     |

---

## 4. Error Responses

### 500 Internal Server Error

**Cause**: Unexpected database or aggregation error  
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
| **Cache Storage**      | Redis (preferred); falls back to Django’s default cache if Redis is unavailable                     |
| **Invalidation Rules** | Cache is invalidated when:<br> - A task is created<br> - A task is completed<br> - A task is deleted |
| **QA Notes**           | Create tasks on various dates; verify updated data after cache is cleared                            |

---
