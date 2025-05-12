# This is a self made file
# We will map the url and the function that should be called here

from DjangoEmumbaTrainingApplication import views
from django.urls import re_path, path

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('get_users/', views.get_users, name='get_users'),

    path('user/tasks/create_task/', views.create_task, name='create_task'),
    path('user/tasks/mark_task_complete/', views.mark_task_complete, name='mark_task_complete'),
    path('user/tasks/delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('user/tasks/getAllTask/', views.getAllTask, name='getAllTask'),
    path('user/tasks/SimilarTask/', views.SimilarTask, name='similar_tasks'),

    path('user/Report1/', views.get_task_status_report, name='Report 1'),
    path('user/Report2/', views.get_average_task_per_day, name='Report 2'),
    path('user/Report3/', views.get_late_task_report, name='Report 3'),
    path('user/Report4/', views.get_day_on_which_max_number_of_task_completed, name='Report 4'),
    path('user/Report5/', views.get_number_of_task_opened_every_day, name='Report 5')


    # path('about/', views.about, name='about'),
    # ... other URL patterns using simple paths
]