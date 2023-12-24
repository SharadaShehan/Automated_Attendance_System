from django.urls import path
from . import views


urlpatterns = [
    path('create/user', views.MiddlewareCreateUserView.as_view()),
    path('create/company', views.MiddlewareCreateCompanyView.as_view()),
    path('update/user-attendance/entrance/<int:pk>', views.MiddlewareUpdateUserAttendanceEnterView.as_view()),
    path('update/user-attendance/leave/<int:pk>', views.MiddlewareUpdateUserAttendanceLeaveView.as_view()),
    path('feed-snapshot', views.MLModelInputView.as_view()),
    # path('ml-model/output', views.MLModelOutputView.as_view()),
    path('login', views.CompanyPortalLoginView.as_view()),
]
