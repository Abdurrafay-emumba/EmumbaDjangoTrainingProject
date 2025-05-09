"""
File Purpose: This is a self-made file. The purpose of this file to keep the code clean, maintainable and readable.
The logic in the views.py file is getting to big. So, it would be a good idea to add supporting functions here.
"""
from django.db.models import Q

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


