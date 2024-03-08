from django.urls import path
from . import views


urlpatterns = [
    path('create/user', views.MiddlewareCreateUserView.as_view()),
    path('create/company', views.MiddlewareCreateCompanyView.as_view()),
    path('login', views.CompanyPortalLoginView.as_view()),
    # path('feed-snapshot', views.MLModelInputView.as_view()),
]
