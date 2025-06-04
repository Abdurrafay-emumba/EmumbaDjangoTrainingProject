# API Documentation – Mark Task as Complete

---

## 1. General Information

| Field              | Value                                                                  |
|--------------------|------------------------------------------------------------------------|
| **API Name**       | Mark Task as Complete                                                  |
| **Endpoint**       | `/user/tasks/mark_task_complete/`                                      |
| **Method**         | PATCH                                                                  |
| **Authentication** | Yes                                                                    |
| **Pagination**     | No                                                                     |
| **Caching**        | **No** (but cache invalidation is performed)                           |
| **Purpose**        | Marks a specific task as completed and updates its completion date.    |

---

## 2. Request Details

### Headers

```http
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### Request Body Parameters

| Parameter | Type   | Required | Description                       | Constraints      |
|-----------|--------|----------|-----------------------------------|------------------|
| id        | int    | Yes      | ID of the task to be marked done  | Must be owned by user |

### Sample Request

```json
{
  "id": 12
}
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "Task marked as complete"
}
```

### Response Fields

| Field    | Type   | Description                          |
|----------|--------|--------------------------------------|
| message  | string | Confirmation of update               |

---

## 4. Error Responses

### 404 Not Found

**Cause**: Task with given ID does not exist for this user  
**Example**:

```json
{
  "error": "Task not found"
}
```

### 400 Bad Request

**Cause**: Invalid request or internal serializer error (rare)  
**Example**:

```json
{
  "non_field_errors": ["Some internal validation failed."]
}
```

---

## 5. Caching

| Property               | Description                                                                                     |
|------------------------|-------------------------------------------------------------------------------------------------|
| **Cached**             | No                                                                                              |
| **Cache Duration**     | N/A                                                                                              |
| **Cache Storage**      | N/A                                                                                              |
| **Invalidation Rules** | Clears cache for:<br> - Task status report<br> - Average tasks/day<br> - Late task report<br> - Max tasks/day<br> - Tasks opened daily |
| **QA Notes**           | Ensure cache invalidation by calling affected report APIs after marking task complete           |

---
