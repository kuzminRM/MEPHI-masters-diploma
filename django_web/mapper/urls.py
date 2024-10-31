from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:product_id>/map/", views.product_map_view, name="product_map_view"),
]