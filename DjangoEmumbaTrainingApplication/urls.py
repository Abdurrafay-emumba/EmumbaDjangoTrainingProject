# This is a self made file
# We will map the url and the function that should be called here

from DjangoEmumbaTrainingApplication import views
from django.urls import re_path, path

urlpatterns = [
    re_path('User', views.UserApi, name='User'),
    path('user/<int:user_id>/tasks/', views.SimilarTask, name='similar_tasks'),
    path('user/<int:user_id>/Report1/', views.get_task_status_report, name='Report 1'),
    path('user/<int:user_id>/Report2/', views.get_average_task_per_day, name='Report 2'),
    path('user/<int:user_id>/Report3/', views.get_late_task_report, name='Report 3'),
    path('user/<int:user_id>/Report4/', views.get_day_on_which_max_number_of_task_completed, name='Report 4'),
    path('user/<int:user_id>/Report5/', views.get_number_of_task_opened_every_day, name='Report 5')


    # path('about/', views.about, name='about'),
    # ... other URL patterns using simple paths
]