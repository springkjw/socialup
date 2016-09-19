from django.conf.urls import url, include
from .views import login_cancelled

urlpatterns = [
    url(r'^social/login/cancelled/$', login_cancelled),
    url(r'^', include("allauth.urls")),
]