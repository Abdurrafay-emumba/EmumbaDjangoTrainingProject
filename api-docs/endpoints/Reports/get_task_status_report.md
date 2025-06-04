# API Documentation – Task Status Report (CSV)

---

## 1. General Information

| Field              | Value                                                                             |
|--------------------|-----------------------------------------------------------------------------------|
| **API Name**       | Task Status Report                                                                |
| **Endpoint**       | `/user/tasks/get_task_status_report/`                                             |
| **Method**         | GET                                                                               |
| **Authentication** | Yes                                                                               |
| **Pagination**     | No                                                                                |
| **Caching**        | Yes                                                                               |
| **Purpose**        | Generates a CSV report showing total, completed, and incomplete task counts.      |

---

## 2. Request Details

### Headers

```http
Accept: text/csv
Authorization: Bearer <token> or Session Cookie
```

### Request Body Parameters

None

### Sample Request

```http
GET /user/tasks/get_task_status_report/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample CSV Response

Content-Disposition header:
```http
Content-Disposition: attachment; filename="tasks.csv"
```

CSV Content:
```
Total tasks,Completed Task,Incompleted Task
15,9,6
```

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

| Property               | Description                                                                                  |
|------------------------|----------------------------------------------------------------------------------------------|
| **Cached**             | Yes                                                                                          |
| **Cache Duration**     | 15 minutes                                                                                   |
| **Cache Storage**      | Redis (primary). Falls back to Django's default cache if Redis is unavailable.              |
| **Invalidation Rules** | Cache is invalidated on:<br> - Task creation<br> - Task completion<br> - Task deletion        |
| **QA Notes**           | Download once → cache hit; modify task → download again → ensure updated CSV (cache cleared) |


---
