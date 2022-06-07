from django.urls import path
from prediction import views

urlpatterns = [
    path('group/<int:group_id>/create-prediction/', views.select_values_to_predict, name='create-prediction'),
    path('group/<int:group_id>/predict/', views.make_prediction, name='predict'),
]
