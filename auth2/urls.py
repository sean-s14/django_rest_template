from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import (
    UserList,
    UserDetail,
    UserVerification,
    UserResetPassword,
)

app_name = 'auth2'

urlpatterns = [
    path('verify/', UserVerification.as_view(), name='user_verification'),
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('user/', UserDetail.as_view(), name='user_detail_token'),
    path('user/reset-password/', UserResetPassword.as_view(), name='password_reset'),
    path('user/change-password/', UserDetail.as_view(), name='password_change'),
    path('user/delete-account/', UserDetail.as_view(), name='delete_account'),
]

urlpatterns = format_suffix_patterns(urlpatterns)