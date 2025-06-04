# API Documentation – Create Task

---

## 1. General Information

| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| **API Name**       | Create Task                                                           |
| **Endpoint**       | `/user/tasks/create_task/`                                            |
| **Method**         | POST                                                                  |
| **Authentication** | Yes (User must be logged in)                                          |
| **Pagination**     | No                                                                    |
| **Caching**        | **No** (but cache invalidation is performed)              |
| **Purpose**        | Creates a new task for the logged-in user with optional file upload   |

---

## 2. Request Details

### Headers

```http
Content-Type: multipart/form-data
Accept: application/json
Authorization: Bearer <token> or Session Cookie
```

### Request Body Parameters

| Parameter       | Type     | Required | Description                                 | Constraints                          |
|-----------------|----------|----------|---------------------------------------------|--------------------------------------|
| title           | string   | Yes      | Title of the task                           | Max length: 100                      |
| description     | string   | Yes      | Detailed description of the task            | Max length: 500                      |
| due_date        | string   | Yes      | Deadline date for the task                  | Format: `YYYY-MM-DD`                |
| file_attachment | file     | No       | Optional file to attach with the task       | Any valid file type                 |

> `start_date` is automatically set to today.  
> `completion_status` is set to `false` by default.  
> `completion_date` is null until marked complete.  
> `user_id` is derived from the session/token.

### Sample Request (Form-Data)

```
title: "Finish report"
description: "Prepare the final report for project"
due_date: "2025-06-10"
file_attachment: [uploaded_file.pdf]
```

---

## 3. Success Response

### HTTP Status

`201 Created`

### Sample Response

```json
{
  "message": "Task created successfully"
}
```

### Response Fields

| Field    | Type   | Description                     |
|----------|--------|---------------------------------|
| message  | string | Confirmation of task creation   |

---

## 4. Error Responses

### 400 Bad Request

**Cause**: Missing or invalid fields  
**Example**:

```json
{
  "title": ["This field is required."],
  "due_date": ["Date has wrong format. Use YYYY-MM-DD."]
}
```

---

## 5. Caching

| Property               | Description                                                                                                                                                             |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Cached**             | No                                                                                                                                                                      |
| **Cache Duration**     | N/A (caches are invalidated on write)                                                                                                                                   |
| **Cache Storage**      | Django's cache layer (likely Redis or in-memory)                                                                                                                        |
| **Invalidation Rules** | On task creation, the following caches are cleared:<br> - Task status report<br> - Average task/day<br> - Late task report<br> - Max tasks/day<br> - Tasks opened daily |
| **QA Notes**           | Create a task and verify cache invalidation by calling affected reporting APIs again                                                                                    |

---
