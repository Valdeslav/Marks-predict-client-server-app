from django.urls import path
from groups_app import views

urlpatterns = [
    path('faculty/list/', views.faculty_list, name='faculty-list'),
    path('faculty/<faculty_id>/group/list/', views.group_list, name='group-list'),
]
