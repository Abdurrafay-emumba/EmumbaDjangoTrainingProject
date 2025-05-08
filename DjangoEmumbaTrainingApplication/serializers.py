# This is a self made class
# The classes we made in model and the datatypes we gave them, are not python native, they are django native -
# - serializers help in coverting them into each other

# Some info about serializers
# serializers are used to convert complex data types (like Django models) into native Python datatypes (like dicts), -
# - which can then be easily rendered into JSON, XML, or other content types — and vice versa.

from rest_framework import serializers
from DjangoEmumbaTrainingApplication.models import OurUser, Task

class OurUserSerializer(serializers.ModelSerializer):
    # Very important for securely handling passwords in Django REST Framework serializers.
    # This makes the field write-only, which means:
    #   You can send this field in a POST/PUT request (e.g. during registration or password change)
    #   It will NOT be included in the response/output (e.g. when you serialize a user)
    #   This will prevent the password from being exposed
    password = serializers.CharField(write_only=True)

    class Meta:
        model = OurUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'account_date_creation']

    def create(self, validated_data):
        user = OurUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            account_date_creation=validated_data.get('account_date_creation')
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    # This will show the user's ID by default.
    user_id = serializers.PrimaryKeyRelatedField(queryset=OurUser.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'start_date', 'due_date', 'completion_date', 'completion_status', 'user_id']