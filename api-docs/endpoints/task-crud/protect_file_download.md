# API Documentation – Protected File Download

---

## 1. General Information

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| **API Name**       | Protected File Download                                               |
| **Endpoint**       | `/user/tasks/protected_file_download/<task_id>/`                     |
| **Method**         | GET                                                                   |
| **Authentication** | Yes                                                                   |
| **Pagination**     | No                                                                    |
| **Caching**        | No                                                                    |
| **Purpose**        | Downloads the file attached to a user's task, if one exists.          |

---

## 2. Request Details

### Headers

```http
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### URL Parameters

| Parameter | Type | Required | Description                              |
|-----------|------|----------|------------------------------------------|
| task_id   | int  | Yes      | ID of the task containing the file       |

### Request Body Parameters

None.

### Sample Request

```http
GET /user/tasks/protected_file_download/17/
```

---

## 3. Success Response

### HTTP Status

`200 OK`

### Sample Response

**Binary file content will be downloaded as an attachment.**

Content-Disposition header:
```http
Content-Disposition: attachment; filename="report.pdf"
```

---

## 4. Error Responses

### 404 Not Found

**Cause**: Task doesn't exist, user unauthorized to access it, or no file attached  
**Examples**:

```json
{
  "error": "No file attached to this task"
}
```

```json
{
  "error": "File not found or access denied"
}
```

---

## 5. Caching

| Property               | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| **Cached**             | No                                                                          |
| **Cache Duration**     | N/A                                                                         |
| **Cache Storage**      | N/A                                                                         |
| **Invalidation Rules** | N/A                                                                         |
| **QA Notes**           | Test with/without file attachment; ensure only the task owner can download  |

---
