from django.contrib import admin
from django.urls import path

from .views import *




urlpatterns = [
    path('index/', Index.as_view()),
    path('filters/first/', filter_1),
    path('filters/second/<slug:thing>/', filter_2),
    path('filters/third/', filter_3),
    path('filters/fourth/', filter_4),
]