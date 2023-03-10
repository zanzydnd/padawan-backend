from django.urls import path

from app.views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
