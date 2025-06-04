# API Documentation – Late Task Report (PDF)

---

## 1. General Information

| Field              | Value                                                                            |
|--------------------|----------------------------------------------------------------------------------|
| **API Name**       | Late Task Report                                                                 |
| **Endpoint**       | `/user/tasks/get_late_task_report/`                                              |
| **Method**         | GET                                                                              |
| **Authentication** | Yes                                                                              |
| **Pagination**     | No (returns a PDF file, not a list)                                              |
| **Caching**        | Yes                                                                              |
| **Purpose**        | Returns the number of tasks that were completed late or remain overdue as a PDF. |

---

## 2. Request Details

### Headers

```http
Accept: application/pdf
Authorization: Bearer <token> or Session Cookie
```

### Request Body Parameters

None

### Sample Request

```http
GET /user/tasks/get_late_task_report/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample PDF Response

Content-Disposition header:
```http
Content-Disposition: attachment; filename="tasks.pdf"
```

PDF content includes:
```
Number of task past due date
5
```

---

## 4. Error Responses

### 401 Unauthorized

**Cause**: Missing or invalid authentication  
**Example**:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 5. Caching

| Property               | Description                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------|
| **Cached**             | Yes                                                                                                  |
| **Cache Duration**     | 15 minutes                                                                                           |
| **Cache Storage**      | Redis (preferred); falls back to Django’s cache if Redis is unavailable                             |
| **Invalidation Rules** | Cache is invalidated when:<br> - A task is created<br> - A task is completed<br> - A task is deleted |
| **QA Notes**           | Initial request returns PDF with delay. Repeating it returns cached file. Modify task → recheck report |

---
