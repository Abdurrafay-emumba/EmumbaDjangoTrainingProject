# IN this class we will write our APIs
import csv
from django.utils import timezone
from datetime import date

from django.db.models import Q, F
# Importing libraries
from django.shortcuts import render # This is a auto-included library
from django.views.decorators.csrf import csrf_exempt # To allow other domains to access our api method
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser # to parse the incoming data into data model
from django.http.response import JsonResponse, HttpResponse
from rest_framework.response import Response # More flexible than JsonResponse

# importing our models
from DjangoEmumbaTrainingApplication.models import OurUser
from DjangoEmumbaTrainingApplication.models import Task

# Importing their serializers
from DjangoEmumbaTrainingApplication.serializers import OurUserSerializer
from DjangoEmumbaTrainingApplication.serializers import TaskSerializer

from reportlab.pdfgen import canvas

from django.db.models import Count
from django.db.models.functions import TruncDate, ExtractWeekDay


# Create your views here.

@csrf_exempt
def UserApi(request, id=0):
    # If the request is of type GET, then return all of the users
    if(request.method == 'GET'):

        # This objects is not being recognized as it is a field that will be dynamically created on run time
        users = OurUser.objects.all()

        # This will give us a list, not a dict
        user_serializer = OurUserSerializer(users, many=True)

        # Now we will convert it to JSON format
        # safe = True means that we are sure the input is dict and it can be converted to json
        # safe = False means that we are not sure if the input is dict
        return JsonResponse(user_serializer.data, safe=False)


@api_view(['GET'])  # Required to make Response work properly
def SimilarTask(request, user_id):
    """
    Function Description: This function will get all task of the user. And will check one-by-one -
    - If the description of task A is present in task B or vice versa, return true. Other wise false

    :param request, user_id is the id of the current logged in user
    :Assumption: We will not check which request type it is, since this function will only do one thing
    :return: return a json or list
    """

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
                'task_1': TaskSerializer(task).data,
                'task_2': TaskSerializer(filtered_task).data
            })

    # @api_view(['GET'])  # Required to make Response work properly
    # Response is more flexible than JsonReposne
    # Usage:
    #   return Response({'message': 'success'})                     # Can return a dict
    #   return Response([1, 2, 3])                                  # Can return a list
    #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
    #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
    return Response(resultant_task)

# Reports start from here

# TODO :: Implement a landing page sort of for these download report functions
@api_view(['GET'])
def get_task_status_report(request, user_id):
    """
    TFunction definition: This function will generate a report for us that will -
    - Count of total tasks, completed tasks, and remaining tasks
    :return:
    """

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
def get_average_task_per_day(request, user_id):
    """
    Function Definition: This function will give us the average number of task completed per day
    Logic: To keep it optimized, we will use this formula:
            (number of completed task)/(total number of days till today since joining)
    :param request:
    :param user_id:
    :return: Not a csv or pdf report, but rather a json/dict
    """
    try:
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
def get_late_task_report(request, user_id):
    """
    Function definition: This function will generate a report for us that will -
    - Count total number of task that were delayed
    :return: pdf
    """

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
def get_day_on_which_max_number_of_task_completed(request, user_id):
    """
    Function definition: In this function we will get the day on which the most task were completed
    Logic 1: We can try each day, from the account creation date and count the number of completed task in each day. But this is too brute force.
    Logic 2: Try to somehow group by date and count the entries. It's a little tricky in django, but adding comments for clarifications

    :param request:
    :param user_id:
    :return: a dict
    """

    try:
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
def get_number_of_task_opened_every_day(request, user_id):
    """
    Function Definition: This will get us all the task that were opened on each day of the week
    Logic: I would have to annotate days in the data table. Then I would have to Group by (.values()) on a day. -
     - Then I will again use annotate to put an aggregation function on the days (count them)

    :param request:
    :param user_id:
    :return: dict
    """

    try:
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
