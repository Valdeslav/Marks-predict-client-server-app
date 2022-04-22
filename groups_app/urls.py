from django.urls import path
from groups_app import views

urlpatterns = [
    path('add/<param>/', views.func, name='delete-user-or-smth')
]