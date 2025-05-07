# This is a self made class
# The classes we made in model and the datatypes we gave them, are not python native, they are django native -
# - serializers help in coverting them into each other

# Some info about serializers
# serializers are used to convert complex data types (like Django models) into native Python datatypes (like dicts), -
# - which can then be easily rendered into JSON, XML, or other content types — and vice versa.

from rest_framework import serializers
from DjangoEmumbaTrainingApplication.models import User, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'account_date_creation']

class TaskSerializer(serializers.ModelSerializer):
    # This will show the user's ID by default.
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'start_date', 'due_date', 'completion_date', 'completion_status', 'user_id']