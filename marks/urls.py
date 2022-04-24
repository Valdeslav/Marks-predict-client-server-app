from django.urls import path
from marks import views

urlpatterns = [
    path('group/<group_id>/', views.students_subjects_group_list, name='group-details'),
]
