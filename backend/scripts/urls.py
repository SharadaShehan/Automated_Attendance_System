from django.urls import path
from . import views


urlpatterns = [
    path('init', views.InitView.as_view()),
]
