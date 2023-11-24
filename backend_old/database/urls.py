from django.urls import path
from . import views

# app_name = 'api'
urlpatterns =[
    path('login/', views.CustomLoginView.as_view(), name='login-view'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout-view'),
    path('signup/', views.SignUpView.as_view(), name='signup-view'),
    path('account-update/', views.AccountUpdateView.as_view(), name='account-update-view'),
    path('account-delete/', views.AccountDeleteView.as_view(), name='account-delete-view'),

    # Non-User APIs
    path('view/<int:pk>/', views.AccountRetrieveViewByNonOwner.as_view()),
    path('view/', views.AccountListViewByNonOwner.as_view()),
    path('create/', views.AccountCreateViewByNonOwner.as_view()),
    path('update/<int:pk>/', views.AccountUpdateViewByNonOwner.as_view()),
    path('delete/<int:pk>/', views.AccountDeleteViewByNonOwner.as_view()),
]

