# This is a self made file
# We will map the url and the function that should be called here

from DjangoEmumbaTrainingApplication import views
from django.urls import re_path, path

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'), # For email verification
    path('login/', views.login_user, name='login_user'),
    path('google-login/', views.google_login, name='google_login'),
    path('initiate_reset_forgotten_password/', views.initiate_reset_forgotten_password, name='initiate_reset_forgotten_password'),
    path('verify_forgotten_password_email/<uidb64>/<token>/', views.verify_forgotten_password_email, name='verify_forgotten_password_email'),
    path('logout/', views.logout_user, name='logout_user'),
    path('get_users/', views.get_users, name='get_users'),

    path('user/tasks/create_task/', views.create_task, name='create_task'),
    path('user/tasks/mark_task_complete/', views.mark_task_complete, name='mark_task_complete'),
    path('user/tasks/delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('user/tasks/getAllTask/', views.getAllTask, name='getAllTask'),
    path('user/tasks/SimilarTask/', views.SimilarTask, name='similar_tasks'),

    path('user/get_task_status_report/', views.get_task_status_report, name='Report 1'),
    path('user/get_average_task_per_day/', views.get_average_task_per_day, name='Report 2'),
    path('user/get_late_task_report/', views.get_late_task_report, name='Report 3'),
    path('user/get_day_on_which_max_number_of_task_completed/', views.get_day_on_which_max_number_of_task_completed, name='Report 4'),
    path('user/get_number_of_task_opened_every_day/', views.get_number_of_task_opened_every_day, name='Report 5'),
    path('user/get_number_of_task_opened_every_day2/', views.get_number_of_task_opened_every_day2, name='Report 6')


    # path('about/', views.about, name='about'),
    # ... other URL patterns using simple paths
]