from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import (
    UserList,
    UserCreate,
    UserDetail,
    ForeignUserDetail,
    ForeignUserList,
    UserVerification,
    UserResetPassword,
)

app_name = 'auth2'

urlpatterns = [
    # Admin Only
    path('users/admin/', UserList.as_view(), name='user_list'),
    path('users/admin/<int:pk>/', UserDetail.as_view(), name='user_detail_pk'),

    path('user/', UserDetail.as_view(), name='user_detail_token'),
    path('user/create/', UserCreate.as_view(), name='user_create'),
    path('verify/', UserVerification.as_view(), name='user_verification'),
    
    # Search other users by pk, username or email
    path('user/<int:pk>/', ForeignUserDetail.as_view(), name='foreign_user_detail_pk'),
    path('users/', ForeignUserList.as_view(), name='foreign_user_list'),

    # Passwords
    path('user/reset-password/<int:stage>/', UserResetPassword.as_view(), name='password_reset'),
    path('user/change-password/', UserDetail.as_view(), name='password_change'),
    # path('user/delete-account/', UserDetail.as_view(), name='delete_account'),
]

urlpatterns = format_suffix_patterns(urlpatterns)