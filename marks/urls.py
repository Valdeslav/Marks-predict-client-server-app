from django.urls import path
from marks import views

urlpatterns = [
    path('group/<int:group_id>/', views.students_subjects_group_list, name='group-details'),
    path('group/<int:group_id>/upload/', views.upload_marks_file, name='upload-group-marks'),
    path('group/edit/<int:group_id>/', views.edit_group, name='edit-group'),
    path('group/edit/', views.edit_group, name='create-group'),
    path('group/delete/<int:group_id>/', views.delete_group, name='delete-group'),
]
