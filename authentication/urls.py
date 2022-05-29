from django.urls import path
from authentication import views

urlpatterns = [
    path('register/', views.register, name='register-user'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
