from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard/", dashboard, name="admin_dashboard"),

    path("category/", category, name="admin_category"),
    path("sub_category/", subcategory, name="admin_subcategory"),
    path("brand/", brands, name="admin_brand"),

    path("products", product, name="admin_product"),
    path("products/create", add_products, name="admin_create_product"),

    path("admin/control_pannel", admin.site.urls),
]