from django.urls import path

from .views import *

urlpatterns = [
    path('',ProductView.as_view(),name='products'),
    path('<int:id>/',ProductView.as_view(),name='get-product'),
    path('populate-products/',PopulateProductView.as_view(),name='product-bulk-upload'),
]