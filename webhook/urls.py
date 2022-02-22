from django.urls import path
from .views import WebHook


app_name = 'bot'

urlpatterns = [
    path("", WebHook.as_view(), name='webhook')
]