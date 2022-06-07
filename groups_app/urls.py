from django.urls import path
from groups_app import views

urlpatterns = [
    path('faculty/list/', views.faculty_list, name='faculty-list'),
    path('faculty/<int:faculty_id>/group/list/', views.group_list, name='group-list'),
    path('faculty/edit/<int:faculty_id>/', views.edit_faculty, name='edit-faculty'),
    path('faculty/edit/', views.edit_faculty, name='create-faculty'),
    path('faculty/delete/<int:faculty_id>/', views.delete_faculty, name='delete-faculty'),
]
