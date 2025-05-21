# This is a self made class
# The classes we made in model and the datatypes we gave them, are not python native, they are django native -
# - serializers help in coverting them into each other
from django.utils import timezone

# Some info about serializers
# serializers are used to convert complex data types (like Django models) into native Python datatypes (like dicts), -
# - which can then be easily rendered into JSON, XML, or other content types — and vice versa.

from rest_framework import serializers
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class OurUserSerializer(serializers.ModelSerializer):
    """
   Serializer Info: This serializer will be used in User creation.
   1) It will not take id from user. id will be managed by django
   2) It will not take the account_date_creation from the user. account_date_creation will be the same day as today.
   3) Rest of the fields will be taken from the user
   """

    # Very important for securely handling passwords in Django REST Framework serializers.
    # This makes the field write-only, which means:
    #   You can send this field in a POST/PUT request (e.g. during registration or password change)
    #   It will NOT be included in the response/output (e.g. when you serialize a user)
    #   This will prevent the password from being exposed
    password = serializers.CharField(write_only=True)

    class Meta:
        model = OurUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        today = timezone.now().date()
        user = OurUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            account_date_creation=today
        )
        return user

class OurUserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer Description: This serializer has all the attributes of the task.
    Use this serializer to get detail info on the task only.
    Do not use it to create task
    """

    # Very important for securely handling passwords in Django REST Framework serializers.
    # This makes the field write-only, which means:
    #   You can send this field in a POST/PUT request (e.g. during registration or password change)
    #   It will NOT be included in the response/output (e.g. when you serialize a user)
    #   This will prevent the password from being exposed
    password = serializers.CharField(write_only=True)

    class Meta:
        model = OurUser
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer Info: This serializer will be used in task creation.
    1) It will not take id from user. id will be manages by django
    2) It will only take title, description and due_date from the user
    3) It will not take the start_date from the user. start_date will be the same day as today.
    4) It will not take the completion_date from the user. completion_date will be set auto, when the task is marked as complete.
    5) completion_status will be by-default false (mentioned in model). When task is marked completed it will be turned to true.
    6) user_id will be taken from the session id
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

    def create(self, validated_data):
        user = self.context['request'].user
        # Getting today date for the creation of task date
        today = timezone.now().date()
        return Task.objects.create(user_id=user, start_date = today,**validated_data)

class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Serializer Description: This serializer has all the attributes of the task.
    Use this serializer to get detail info on the task only.
    Do not use it to create task
    """
    # To ensure the user id exist
    user_id = serializers.PrimaryKeyRelatedField(queryset=OurUser.objects.all())

    class Meta:
        model = Task
        fields = '__all__'

class TaskCompletionUpdationSerializer(serializers.ModelSerializer):
    """
    Serializer Description: We need a new serializer for updating purpose. This is because our other serializers -
    - change things that we do not changed during this update. For example, they update the start_date to today.
    Also it is good practice to have different serializers.

    This serializer will not take any data from the user. It will update the following fields itself:
        1) completion_date = today
        2) completion_status = True
    """
    class Meta:
        model = Task
        # This is empty as we are not expecting any input from the user
        fields = []

    # We do not want to create a new instance, rather, we want to update it.
    # So, we need to override the update function rather than the create one
    def update(self, instance, validated_data):
        instance.completion_status = True
        instance.completion_date = timezone.now().date()
        # Saving and returning the updated status
        instance.save()
        return instance