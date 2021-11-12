from django.urls import path, include
from .views import userAPIView,LoginView,LogoutView,RegistrationView,ResetPasswordView
from .views import ChangePasswordView
from Task .views import TaskView
urlpatterns = [
    path('users', userAPIView.as_view()),
    path('login',LoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(), name='logout'),
    path('register',RegistrationView.as_view(), name='register'),
    # path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('confirm',ResetPasswordView.as_view(), name='confirm'),
    path('change',ChangePasswordView.as_view(), name='change'),
    path('addTask/',TaskView.as_view(), name='addTask')
]