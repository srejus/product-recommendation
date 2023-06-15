from django.urls import path

from .views import *

urlpatterns = [
    path('',OrderView.as_view(),name='order'),
    path('populate-orders/',PopulateOrderView.as_view(),name='order'),
]