from django.urls import path
from marks import views

urlpatterns = [
    path('group/<int:group_id>/', views.students_subjects_group_list, name='group-details'),
    path('group/<int:group_id>/upload/', views.upload_marks_file, name='upload-group-marks'),
    path('group/edit/<int:group_id>/', views.edit_group, name='edit-group'),
    path('group/edit/', views.edit_group, name='create-group'),
    path('group/delete/<int:group_id>/', views.delete_group, name='delete-group'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit-student'),
    path('student/edit/', views.edit_student, name='create-student'),
    path('student/delete/<int:student_id>/', views.delete_student, name='delete-student'),
    path('student/<int:student_id>/marks/', views.mark_list, name='mark-list'),
    path('mark/edit/<int:mark_id>/', views.edit_mark, name='edit-mark'),
    path('mark/edit/', views.edit_mark, name='create-mark'),
    path('mark/delete/<int:mark_id>/', views.delete_mark, name='delete-mark'),
]
