from django.urls import path
from .views import RegistrationView, LoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register'), # registration/ statt register/
    path('login/', LoginView.as_view(), name='login'),
    # Später für den Mail-Check im Frontend:
    # path('email-check/', EmailCheckView.as_view(), name='email_check'),
]