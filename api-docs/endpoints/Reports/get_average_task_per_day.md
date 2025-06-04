# API Documentation – Average Tasks Completed Per Day

---

## 1. General Information

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| **API Name**       | Average Tasks Completed Per Day                                       |
| **Endpoint**       | `/user/tasks/get_average_task_per_day/`                               |
| **Method**         | GET                                                                   |
| **Authentication** | Yes                                                                   |
| **Pagination**     | No                                                                    |
| **Caching**        | Yes                                                                   |
| **Purpose**        | Returns the average number of tasks completed per day since user joined. |

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
GET /user/tasks/get_average_task_per_day/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "User ID": 4,
  "Average task completed per day": 1.25
}
```

### Response Fields

| Field                             | Type    | Description                                      |
|----------------------------------|---------|--------------------------------------------------|
| User ID                          | integer | ID of the currently logged-in user               |
| Average task completed per day   | float   | Total completed tasks ÷ days since account created |

---

## 4. Error Responses

### 500 Internal Server Error

**Cause**: Unexpected runtime exception  
**Example**:

```json
{
  "Exception occured": "division by zero"
}
```

---

## 5. Caching

| Property               | Description                                                                                         |
|------------------------|-----------------------------------------------------------------------------------------------------|
| **Cached**             | Yes                                                                                                 |
| **Cache Duration**     | 15 minutes                                                                                          |
| **Cache Storage**      | Redis (primary); falls back to Django’s default cache if Redis is unavailable                      |
| **Invalidation Rules** | Cache is invalidated when:<br> - A task is created<br> - A task is completed<br> - A task is deleted |
| **QA Notes**           | Simulate long run (5s delay); repeat request → expect faster response from cache. Modify task → cache clears |

---
