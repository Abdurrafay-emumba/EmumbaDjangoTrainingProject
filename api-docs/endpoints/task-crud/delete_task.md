# API Documentation – Delete Task

---

## 1. General Information

| Field              | Value                                                               |
|--------------------|---------------------------------------------------------------------|
| **API Name**       | Delete Task                                                         |
| **Endpoint**       | `/user/tasks/delete_task/<task_id>/`                                |
| **Method**         | DELETE                                                              |
| **Authentication** | Yes                                                                 |
| **Pagination**     | No                                                                  |
| **Caching**        | **No** (but cache invalidation is performed)                        |
| **Purpose**        | Deletes a user-owned task permanently and invalidates relevant caches |

---

## 2. Request Details

### Headers

```http
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### URL Parameters

| Parameter | Type | Required | Description                   |
|-----------|------|----------|-------------------------------|
| task_id   | int  | Yes      | ID of the task to be deleted  |

### Request Body Parameters

None — this is a `DELETE` method and the task ID is passed via URL.

### Sample Request

```http
DELETE /user/tasks/delete_task/12/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "Task deleted successfully."
}
```

### Response Fields

| Field    | Type   | Description                         |
|----------|--------|-------------------------------------|
| message  | string | Confirmation message after deletion |

---

## 4. Error Responses

### 404 Not Found

**Cause**: Task with given ID does not exist for the current user  
**Example**:

```json
{
  "error": "Task not found."
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
| **QA Notes**           | Delete a task and confirm that all task-related report endpoints reflect the change             |

---
