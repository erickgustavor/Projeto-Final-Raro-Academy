from django.urls import path
from .views import ProductListView, RateListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("rates/", RateListView.as_view(), name="rate_list"),
]
