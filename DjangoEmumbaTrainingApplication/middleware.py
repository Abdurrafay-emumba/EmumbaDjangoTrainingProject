"""
File Purpose: This is a self-made file. The purpose of this file to keep the code clean, maintainable and readable.
The logic in the views.py file is getting to big. So, it would be a good idea to add supporting functions here.
"""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from DjangoEmumbaTrainingApplication.models import OurUser


def Custom_Authenticate(userNameOrEmail, password):
    """
    Function Description: Basically this function will authenticate for (username+password) or (email+password).
    Logic: It will simply check in it's database, if the username+password match or email+password match.
    It will check (username+password) first then (email+password). If successful, it will return the user, otherwise -
    - it will return null.

    :param userNameOrEmail: This will be either the username or the email
    :param password: THe password provided by the user
    :return: user obj or None
    """

    # TODO_DONE :: I should make the email and username unique :: email made unique, username already by default unique

    try:
        # Getting a user with this email or username.
        # Q is used to combine multiple conditions using logical operations (| for OR, & for AND).
        # I would have also compared password here, using a 'AND' but our passwords are hashed, so it would not have worked
        user = OurUser.objects.get(Q(username=userNameOrEmail) | Q(email=userNameOrEmail))
    except Exception as e:
        return None

    # This is how you would compare hashed passowrds
    if user.check_password(password):
        return user
    else:
        return None


def paginate_queryset(queryset, request, serializer_class=None):
    """
    Function Description: This function will paginate the data for us. It is useful for paginating multiple views

    :param queryset: The data to paginate (It must be a Django queryset or a list. Dict is NOT accepted).
    :param request: The request object (needed for pagination metadata like ?page=2).
    :param serializer_class: If provided, the data will be serialized using this class.
                             If None, assume data is already serialized or ready to return.
                             The default value is None, so if no parameter is passes to it, it will assume that the data is already -
                             - serialized
    :return: A paginated Response object.
    """

    # For query pagination
    paginator = PageNumberPagination()

    # This below line is redundant, since we have already mentioned page size in settings.py
    # paginator.page_size = 10
    page = paginator.paginate_queryset(queryset, request)

    if page is None:
        # In case pagination isn't applied (e.g., invalid page number)
        return Response([])

    if serializer_class is not None:
        serializer = serializer_class(page, many=True)

        # @api_view(['GET'])  # Required to make Response work properly
        # Response is more flexible than JsonReposne
        # Usage:
        #   return Response({'message': 'success'})                     # Can return a dict
        #   return Response([1, 2, 3])                                  # Can return a list
        #   return Response(TaskSerializer(tasks, many=True).data)      # Can return Serialized data (list or dict)
        #   return Response("Hello", content_type='text/plain')         # Can return a str or plain text
        # This is using Response under the hood
        return paginator.get_paginated_response(serializer.data)
    else:
        # Assume data is already serialized (e.g., a list of dicts)
        return paginator.get_paginated_response(page)


def send_verification_email(user, request):
    """
    Function Definition: This function will send the verification email for us.
    It will use the credentials that we specified in the settings.py

    This function should be called after the user has registered successfully
    :param user:
    :param request:
    :return:
    """

    # This is django default token creation function
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Verify your email'
    message = f'Hi {user.username},\nPlease verify your email by clicking the link below:\n{verification_link}'

    # This is django default email sending function. It is sending the email
    send_mail(subject, message, 'noreply@example.com', [user.email])

