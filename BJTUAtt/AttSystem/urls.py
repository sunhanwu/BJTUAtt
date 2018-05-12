from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'index/$',views.index),
    url(r'index/test2.html/$',views.test2),
]
