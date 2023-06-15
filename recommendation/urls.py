from django.urls import path

from .views import *

urlpatterns = [
    path('<int:id>/',RecommendationView.as_view(),name='products-recommendation'),
]