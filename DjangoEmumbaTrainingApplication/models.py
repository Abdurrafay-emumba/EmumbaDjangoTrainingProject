from django.db import models
from datetime import date

# I will make my self-made user class inherit from this class, so that it gets all the perks, for example (login, authenticate etc)
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.

# Our self made user class is now inheriting from django in-built user class.
# Our user class will get the in-built perks of login etc
# And since, it is our self made user class, we can make changes as we want in it
class OurUser(AbstractUser):
    # id and name are no longer needed as now these fields will be inherited from the parent class
    # This is the primary key for the user, and will act as the foreign key in task table
    # id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=100)

    # Making email unique, as our logic (authentication) depends on it being unique, would also have had made username unqiue, but it already is so
    # The models.EmailField already checks the format at the model/form level.
    email = models.EmailField(unique=True,null=False,blank=False)

    # Why not make the default here to today's date?
    # The below line will give all the users the date when the server started
    # account_date_creation = models.DateField(default=timezone.now().date())
    # This approach is correct
    account_date_creation = models.DateField(default=timezone.now)

    # Users will by default will not be email verified
    # This field will turn to true after users have verified email
    is_email_verified = models.BooleanField(default=False)

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
    user_id = models.ForeignKey(OurUser, on_delete=models.CASCADE)

    # This is the file attachment field
    # It will not contain the file but the url/link to the file
    # The actual file will be stored in the media folder
    # We will make sure that only authorized people can get the file
    file_attachment = models.FileField(upload_to='task_attachments/', null=True, blank=True)



