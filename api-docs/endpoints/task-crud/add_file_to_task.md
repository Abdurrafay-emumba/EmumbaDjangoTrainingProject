# API Documentation – Add File to Task

---

## 1. General Information

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| **API Name**       | Add File to Task                                                      |
| **Endpoint**       | `/user/tasks/add_file_to_task/`                                       |
| **Method**         | POST                                                                  |
| **Authentication** | Yes                                                                   |
| **Pagination**     | No                                                                    |
| **Caching**        | No                                                                    |
| **Purpose**        | Uploads and attaches a file to an existing user-owned task.           |

---

## 2. Request Details

### Headers

```http
Content-Type: multipart/form-data
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### Request Body Parameters

| Parameter       | Type   | Required | Description                           | Constraints         |
|-----------------|--------|----------|---------------------------------------|---------------------|
| task_id         | int    | Yes      | ID of the task to attach the file to  | Must belong to user |
| file_attachment | file   | Yes      | File to be attached to the task       | Any valid file type |

### Sample Request (Form-Data)

```
task_id: 15
file_attachment: [uploaded_file.pdf]
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

```json
{
  "message": "File added to task successfully."
}
```

### Response Fields

| Field    | Type   | Description                        |
|----------|--------|------------------------------------|
| message  | string | Confirmation of successful upload  |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: No file provided in the request  
**Example**:

```json
{
  "error": "No file provided."
}
```

### 404 Not Found

**Cause**: Task with the given ID not found or not owned by the user  
**Example**:

```json
{
  "error": "Task not found."
}
```

---

## 5. Caching

| Property               | Description                                                   |
|------------------------|---------------------------------------------------------------|
| **Cached**             | No                                                            |
| **Cache Duration**     | N/A                                                           |
| **Cache Storage**      | N/A                                                           |
| **Invalidation Rules** | N/A                                                           |
| **QA Notes**           | Upload a file and verify download endpoint returns the file   |

---
