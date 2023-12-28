from django.urls import path
from . import views
from .custom_token_view import CustomObtainAuthToken


urlpatterns = [
    path('executive/update/employee/<int:pk>', views.ExecutiveUpdateEmployeeView.as_view()),
    path('employee/update/employee/', views.EmployeeUpdateEmployeeView.as_view()),
    path('employee/view/employee/', views.EmployeeViewEmployeeView.as_view()),
    path('executive/view/employee/<int:pk>', views.ExecutiveViewEmployeeView.as_view()),
    path('executive/list-view/employee/', views.ExecutiveListViewEmployeeView.as_view()),
    path('executive/delete/employee/<int:pk>', views.ExecutiveDeleteEmployeeView.as_view()),

    path('executive/view/attendance/<year>/<month>/<day>',views.ExecutiveViewAttendanceView.as_view()),

    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),

    path('executive/view/role/<int:pk>', views.ExecutiveViewRoleView.as_view()),
    path('executive/list-view/role/', views.ExecutiveListViewRoleView.as_view()),
    path('executive/create/role/', views.ExecutiveCreateRoleView.as_view()),
    path('executive/update/role/<int:pk>', views.ExecutiveUpdateRoleView.as_view()),
    path('executive/delete/role/<int:pk>', views.ExecutiveDeleteRoleView.as_view()),

    path('auth/', CustomObtainAuthToken.as_view()),
]
