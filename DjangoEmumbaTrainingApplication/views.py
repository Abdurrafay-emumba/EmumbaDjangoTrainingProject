# IN this class we will write our APIs
import csv
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from datetime import date

from django.contrib import messages
from django.db.models import Q, F
# Importing libraries
from django.shortcuts import render, redirect  # This is a auto-included library
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt # To allow other domains to access our api method
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser # to parse the incoming data into data model
from django.http.response import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response # More flexible than JsonResponse

from DjangoEmumbaTrainingApplication.middleware import Custom_Authenticate, paginate_queryset, send_verification_email
# importing our models
from DjangoEmumbaTrainingApplication.models import OurUser
from DjangoEmumbaTrainingApplication.models import Task

# Importing their serializers
from DjangoEmumbaTrainingApplication.serializers import OurUserSerializer, TaskDetailSerializer, \
    OurUserDetailSerializer, TaskCompletionUpdationSerializer
from DjangoEmumbaTrainingApplication.serializers import TaskSerializer

from reportlab.pdfgen import canvas

from django.db.models import Count
from django.db.models.functions import TruncDate, ExtractWeekDay

# TODO :: IMPORTANT :: Wrap all the APIs in try-catch blocks

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Function Definition: API endpoint to register a new user.
    We can no longer just INSERT data to the database, as the passwords will be hashed and stored in it
    BY adding users this way, the password will be hashed by django

    TODO_DONE :: Much can be improved here. For example:
        1) Same email cannot be used for registration again :: DONE :: Made email unique+NON_NULL+NON_EMPTY in OurUser model
        2) Verifying the email etc :: DONE :: Email verification implemented
    """
    # Our Serializer
    serializer = OurUserSerializer(data=request.data)

    # If the received data seems valid, then ok register the user
    # Other wise don't
    if serializer.is_valid():
        # This actually saves and returns the instance to you, so we dont need the below line
        user = serializer.save()
        # Sending the user email so they may confirm their email
        # Since the user has been saved, he can be looked up (no longer needed/redundant)
        # user = OurUser.objects.get(email=request.data.get('email'))
        send_verification_email(user, request)

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = OurUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, OurUser.DoesNotExist):
        return Response({'error': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

    if default_token_generator.check_token(user, token):
        if user.is_email_verified:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_200_OK)

        user.is_email_verified = True
        user.save()
        return Response({'message': 'Email successfully verified!'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Function Description: Our Users will login using this function.
    Other report functions will require the user being logged in
    :param request:
    :return:
    """
    userNameOrEmail = request.data.get('username')
    password = request.data.get('password')

    if not userNameOrEmail or not password:
        return Response({"error": "Username (or Email) and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # This line checks the user's credentials, it checks username and password
    # But this in-built function only works for username + password
    # user = authenticate(username=username, password=password)

    # This is our custom authenticator, it will work for (username+password) or (email+password)
    user = Custom_Authenticate(userNameOrEmail, password)

    if user is not None:
        login(request, user)  # This is the line that logs the user in (for sessions)
        return Response({"message": "Login successful!", "username": user.username}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Function Description: This function will handle the OAuth2 login from google.
                            1) Check if the google OAuth2 request is valid
                            2) Get the required info from it
                            3) If the user is not registered, register him
                            4) Login the user

    Following Data is provided by the Google token:
        sub:	        str	    The user's unique Google ID (never changes)
        email:	        str	    The user's email address
        email_verified:	bool	Whether the email is verified by Google
        name:       	str	    The user's full name
        given_name: 	str	    The user's first name
        family_name:	str	    The user's last name
        picture:    	str	    URL of the user's Google profile picture
        locale:     	str	    User's locale (e.g. "en", "fr", "en-GB")
        hd:         	str	    Hosted domain (only for GSuite/Google Workspace accounts — optional)
        iat:        	int	    Issued at time (UNIX timestamp)
        exp:        	int	    Expiration time (UNIX timestamp)
        aud:        	str	    Audience — should match your Google Client ID
        iss:        	str	    Issuer — typically accounts.google.com or https://accounts.google.com

    :param request:
    :return:
    """
    token = request.data.get('token')

    if not token:
        return Response({'error': 'Missing Google ID token'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # This is our main line
        # This verifies the token and gets user info from Google
        idinfo = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            '491997536958-mhn8pth51deeqsfhmvpjle5ij3acimj5.apps.googleusercontent.com',  # This is our Google OAuth2 ID
        )

        # Extract details
        username = idinfo.get('name')
        email = idinfo.get('email')
        password = "We_should_take_username_and_password_from_the_front_end"
        first_name = idinfo.get('given_name')
        last_name = idinfo.get('family_name')

        if not username:
            return Response({'error': 'username not available in token'}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            return Response({'error': 'Email not available in token'}, status=status.HTTP_400_BAD_REQUEST)

        # Find or create the user
        # get_or_create tries to fetch a user matching a given field (email=email in this case) -
        # - If such a user exists, it returns that user and created = False
        # If no such user exists:
        #     It creates a new one using the defaults dictionary.
        #     Returns the new user and created = True.
        user, created = OurUser.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'account_date_creation':timezone.now().date(),
                'is_email_verified':True
            }
        )

        # This is the line that logs the user in (for sessions)
        login(request, user)

        return Response({
            'message': 'Login successful',
            'username': user.username,
            'email': user.email,
            'created': created,
        })

    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Function Definition: This function will logout your user. Will only work with session authentication -
    - Which we are using
    """
    str_user_id = str(request.user.id)
    logout(request)  # Clears the session
    return Response({"message": "Logout successful. User id: " + str_user_id }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    """
    Function Definition: This function is for testing purpose only. It will get us all the users that are registered.
    UPDATE: This API was not paginated. Paginating the APIs.
    :param request:
    :return: All the users in a dict/json format
    """

    # Our Query dataset
    users = OurUser.objects.all()

    # Paginating the query
    return paginate_queryset(users, request, OurUserDetailSerializer)


# Task Functions
# 1) Create
# 2) Edit
# 3) Delete
# 4) Get all task

# TODO_DONE :: Make the creation date for both (the task and user account) to be the current date.
# TODO_DONE :: Don't let the task specify its own user_id. Make it so that the id of the logged in person is used.
# TODO_DONE :: Don't let the task specify its own id. Let Django handle it.
# TODO :: Put checks on task due date, completion date etc, so that they are not before the creation date
# TODO_DONE :: When the user marks the task as complete, only then update it's completion date and set it to today's date

# TODO_DONE :: May have to define different serializers for data input and data output

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    """
    Function Definition: This function will receive a task data from the user and it will create that task
    :param request:
    :return: an OK response or a bad response
    """

    # Our Serializer, providing it with more context.
    serializer = TaskSerializer(data=request.data, context={'request': request})

    # If the received data seems valid, then ok add the task
    # Otherwise don't
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Task created successfully'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# We could have used PUT here, but PATCH is more resource light, and should be used when updating some values -
# - like in our case
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
# TODO :: Add more try-catch
def mark_task_complete(request):
    try:
        task_id = request.data.get('id')
        # Making sure to get the task of the user with the desired id
        task = Task.objects.get(id=task_id, user_id=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    # So, in this line, we are:
    #   Telling the serialzier to update our object 'task'
    #   Since our serilizer does not require any data, we are passing it empty data, otherwise we would have done response.data
    #   partial =True, means we want to update
    serializer = TaskCompletionUpdationSerializer(task, data={}, partial=True)

    if serializer.is_valid():
        # This serializer.save() is calling the update function we had overidden in our serializer
        serializer.save()
        return Response({"message": "Task marked as complete"})
    return Response(serializer.errors, status=400)

# We can use POST here, but that would voilate standards and it may cause confusion and UI incomptatability
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    """
    Function definition: This API will be used to delete a task., we have to send the data by url.
    DELETE does not carry data like POST.
    This function will not need a serializer
    :param request:
    :return:
    """
    try:
        # To specify the task and user
        task = Task.objects.get(id=task_id, user_id=request.user)
        # This is enough to delete the object
        task.delete()
        return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllTask(request):
    """
    Function Definition: This function requires being logged in.
    It will get all the task of the user for us

    UPDATE: This API was not paginated. Paginating the API
    :param request:
    :return: All the user task
    """

    # Getting the user id of the logged in person
    user_id = request.user.id
    # Getting the task of the person
    tasks = Task.objects.filter(user_id= user_id)

    # Function called for pagination
    return paginate_queryset(tasks, request, TaskDetailSerializer)


# Since for the report functions, we are requiring the user to be logged in
# So, we no longer require the user_id, instead we will take the user_id of the logged in user
# We dont really require @permission_classes([IsAuthenticated]) as we have already implemented in settings.py that every api needs -
# - authentication

@api_view(['GET'])  # Required to make Response work properly
@permission_classes([IsAuthenticated])
def SimilarTask(request):
    """
    Function Description: This function will get all task of the user. And will check one-by-one -
    - If the description of task A is present in task B or vice versa, return true. Other wise false

    UPDATE: This API was not paginated. Paginating the API.

    :param request, user_id is the id of the current logged in user (user_id removed after implementing authentication)
    :Assumption: We will not check which request type it is, since this function will only do one thing
    :return: return a json or list
    """

    user_id = request.user.id
    tasks = Task.objects.filter(user_id= user_id)

    resultant_task = []

    for task in tasks:
        # icontains is not case sensitive
        # The below commented will not work as the issue is that -
        # - you're using Python's != directly inside the .filter() method, -
        # - but Django ORM expects keyword arguments, not Python expressions.
        # filtered_task = tasks.filter(description__icontains=task.description, id != task.id)
        filtered_tasks = tasks.filter(description__icontains=task.description).exclude(id=task.id)

        for filtered_task in filtered_tasks:
            resultant_task.append({
                'task_1': TaskDetailSerializer(task).data,
                'task_2': TaskDetailSerializer(filtered_task).data
            })

    # Since the serializer class was not passed, it will assume that the data is already serialized (in the form of dict or list)
    return paginate_queryset(resultant_task, request)

# Reports start from here

# TODO_DONE :: Implement a landing page sort of for these download report functions :: Landing page not required
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_status_report(request):
    """
    TFunction definition: This function will generate a report for us that will -
    - Count of total tasks, completed tasks, and remaining tasks

    UPDATE: This API was not paginated. I would have paginated it, but it is returning a csv so we will leave it as it is.

    :return: csv file
    """
    user_id = request.user.id

    tasks = Task.objects.filter(user_id=user_id)

    total_task = len(tasks)

    # Get all completed tasks
    completed_tasks = len(tasks.filter(completion_status=True))

    # Get all incomplete tasks
    # incomplete_tasks = tasks.filter(completion_status=False)
    # The above one works, but for optimization
    incomplete_tasks = total_task - completed_tasks

    # csv creation starts here
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Total tasks', 'Completed Task', 'Incompleted Task'])
    writer.writerow([total_task, completed_tasks, incomplete_tasks])

    return response

# Average number of tasks completed per day since creation of account
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_average_task_per_day(request):
    """
    Function Definition: This function will give us the average number of task completed per day
    Logic: To keep it optimized, we will use this formula:
            (number of completed task)/(total number of days till today since joining)

    Update: THis API is not paginated. And will not be paginated. As it is returning a single dict.
            Also dict are not paginable objects

    :param request:
    :param user_id:
    :return: Not a csv or pdf report, but rather a json/dict
    """
    try:
        user_id = request.user.id

        # Getting the user so that we can have the account creation date
        # The reason the below mentioned line did not work is because filter returns a queryset of zero or more objects -
        # - while I was expecting and using it like a object, when in fact it is like a list (queryset to be exact)
        # user = User.objects.filter(id=user_id) # This is the line that did not work
        # Replacing it with get(), which is like filter, but will give us only 1 object
        user = OurUser.objects.get(id=user_id)

        # Getting all the task of a person having the desired user_id
        tasks = Task.objects.filter(user_id=user_id)

        # Number of completed task
        completed_tasks = len(tasks.filter(completion_status=True))

        days_difference = (date.today() - user.account_date_creation).days

        count_of_average_task_completed_per_day = completed_tasks/days_difference

        response_dict = dict()
        response_dict['User ID'] = user_id
        response_dict["Average task completed per day"] = count_of_average_task_completed_per_day

        # @api_view(['GET'])  # Required to make Response work properly
        # Response is more flexible than JsonReposne
        # Usage:
        #   return Response({'message': 'success'})                     # Can return a dict
        #   return Response([1, 2, 3])                                  # Can return a list
        #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
        #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
        return Response(response_dict)

    # Incase of any exception, return the exception
    except Exception as e:
        response_dict = dict()
        response_dict["Exception occured"] = str(e)

        # @api_view(['GET'])  # Required to make Response work properly
        # Response is more flexible than JsonReposne
        # Usage:
        #   return Response({'message': 'success'})                     # Can return a dict
        #   return Response([1, 2, 3])                                  # Can return a list
        #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
        #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
        return Response(response_dict)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_late_task_report(request):
    """
    Function definition: This function will generate a report for us that will -
    - Count total number of task that were delayed

    UPDATE: This API was not paginated. I would have paginated it, but it is returning a pdf so we will leave it as it is.

    :return: pdf file
    """
    user_id = request.user.id
    today = timezone.now().date()

    tasks = Task.objects.filter(user_id=user_id)

    # Q is used to combine multiple conditions using logical operations (| for OR, & for AND).
    # It’s helpful when you want to filter by more than one rule, especially if they are alternatives (as we have here).
    late_tasks = tasks.filter(
        # completion_date__gt means "completion date is greater than..."
        # F('due_date') means you're comparing to the value of the due_date in the same row. comparing self completion date with self due date
        Q(completion_date__gt=F('due_date')) |  # Case 1
        Q(completion_date__isnull=True, due_date__lt=today)  # Case 2
    )

    # Creating pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tasks.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Number of task past due date")
    # draw string expects a string
    p.drawString(100, 780, str(len(late_tasks)))

    p.showPage()
    p.save()
    return response

# Since time of account creation, on what date, maximum number of tasks were completed in a single day
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_day_on_which_max_number_of_task_completed(request):
    """
    Function definition: In this function we will get the day on which the most task were completed
    Logic 1: We can try each day, from the account creation date and count the number of completed task in each day. But this is too brute force.
    Logic 2: Try to somehow group by date and count the entries. It's a little tricky in django, but adding comments for clarifications

    Update: THis API is not paginated. And will not be paginated. As it is returning a single dict.
        Also dict are not paginable objects

    :param request:
    :param user_id:
    :return: a dict
    """

    try:
        user_id = request.user.id

        # Some explanation
        #
        # .values('field'): Tells Django to group by 'field'
        # .annotate(...): Applies aggregation functions (like Count, Sum, Avg, etc.) to each group
        #
        # Group all tasks by completion_date, and count how many tasks are in each group.
        # Task.objects.values('completion_date').annotate(num=Count('id'))
        #
        # This gives each task object a num field with a count — but it won’t group tasks.
        # Task.objects.annotate(num=Count('id'))
        #
        # Instead of returning full Task model instances, this will only return 'title' and 'completion_status' values and groups by them
        # Task.objects.values('title', 'completion_status')


        result = (
            Task.objects
            .filter(
                user_id=user_id,            # The task should belong to the user
                completion_status=True      # The task should be completed
            )
            .values('completion_date')                  # values('completion_date') + annotate(task_count=Count('id'))
            .annotate(task_count=Count('id'))           # Groups by date and counts how many tasks were completed each day
            .order_by('-task_count')                    # This task_count is the one we just calculated, the '-' means descending order. Without it, it would be ascending order
            .first()                                    # Since, we ordered it. By getting the first we get the date with the max tasks completed
        )

        # @api_view(['GET'])  # Required to make Response work properly
        # Response is more flexible than JsonReposne
        # Usage:
        #   return Response({'message': 'success'})                     # Can return a dict
        #   return Response([1, 2, 3])                                  # Can return a list
        #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
        #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
        return Response(result)

    # In case of any exception, return the exception
    except Exception as e:
        response_dict = dict()
        response_dict["Exception occurred"] = str(e)

        # @api_view(['GET'])  # Required to make Response work properly
        # Response is more flexible than JsonReposne
        # Usage:
        #   return Response({'message': 'success'})                     # Can return a dict
        #   return Response([1, 2, 3])                                  # Can return a list
        #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
        #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
        return Response(response_dict)

# Since time of account creation, how many tasks are opened on every day of the week (mon, tue, wed, ....)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_number_of_task_opened_every_day(request):
    """
    Function Definition: This will get us all the task that were opened on each day of the week
    Logic: I would have to annotate days in the data table. Then I would have to Group by (.values()) on a day. -
     - Then I will again use annotate to put an aggregation function on the days (count them)

    Update: THis API is not paginated. And will not be paginated. As it is returning a single dict.
        Also dict are not paginable objects

    :param request:
    :param user_id:
    :return: dict
    """

    try:
        user_id = request.user.id

        result = (
                Task.objects
                .filter(
                    user_id=user_id
                )
                .annotate(weekday=ExtractWeekDay('start_date'))
                .values('weekday')
                .annotate(task_count=Count('id'))
            )

        return Response(result)

    # In case of any exception, return the exception
    except Exception as e:
        response_dict = dict()
        response_dict["Exception occurred"] = str(e)

        # @api_view(['GET'])  # Required to make Response work properly
        # Response is more flexible than JsonReposne
        # Usage:
        #   return Response({'message': 'success'})                     # Can return a dict
        #   return Response([1, 2, 3])                                  # Can return a list
        #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
        #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
        return Response(response_dict)

# Since time of account creation, how many tasks are opened on every day of the week (mon, tue, wed, ....)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_number_of_task_opened_every_day2(request):
    """
    Function Definition: It is similar to the previous report, but this one will give us how many task were opened on each day
    Logic: I would GROUP BY w.r.t creation_date and then add an aggregation function COUNT. This will be done by using -
    - .values() and .annotate

    Update: THis API is not paginated. And will not be paginated. As it is returning a single dict.
        Also dict are not paginable objects

    :param request:
    :param user_id:
    :return: dict
    """

    try:
        user_id = request.user.id

        result = (
                Task.objects
                .filter(
                    user_id=user_id
                )
                .values('start_date')               # Both .values() and .annotate() work together to give us a -
                .annotate(task_count=Count('id'))   # - GROUP BY + aggregation function usage
            )

        return Response(result)

    # In case of any exception, return the exception
    except Exception as e:
        response_dict = dict()
        response_dict["Exception occurred"] = str(e)

        # @api_view(['GET'])  # Required to make Response work properly
        # Response is more flexible than JsonReposne
        # Usage:
        #   return Response({'message': 'success'})                     # Can return a dict
        #   return Response([1, 2, 3])                                  # Can return a list
        #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
        #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
        return Response(response_dict)
