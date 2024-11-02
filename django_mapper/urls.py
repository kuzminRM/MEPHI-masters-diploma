from django.urls import path
from . import views


app_name = 'django_mapper'


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:product_id>/", views.product_view, name="product_view"),
    path("<int:product_id_1>/map/<int:product_id_2>/", views.map_products, name="map_products"),
]
