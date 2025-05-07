from django.db import models
from datetime import date

# Create your models here.
class User(models.Model):
    # This is the primary key for the user, and will act as the foreign key in task table
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    account_date_creation = models.DateField(default=date(2025,1,1))

class Task(models.Model):
    # This will be the primary key for the Task table
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    start_date = models.DateField()
    due_date = models.DateField()

    # Making the completion date optional. Since, if a task is still in doing than it wont have a completion date
    # null = True: Allows the database to store NULL for this field(important for PostgreSQL).
    # blank = True: Allows Django forms(admin, serializers, etc.) to accept empty input for this field.
    completion_date = models.DateField(null=True, blank=True)

    # BooleanField is a non-nullable field.
    # You need to provide a default for it
    completion_status = models.BooleanField(default=False)

    # This is our foreign key, here we specified that the table is User,
    # It will auto take the primary key as the foreign key
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)





