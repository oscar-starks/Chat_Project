from django.contrib import admin
from django.urls import include, path

from core.k8_views import dapr_subscribe, healthz, orders_handler

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chatapp.urls")),
    path("accounts/", include("accounts.urls")),
    path("healthz", healthz),
    path("dapr/subscribe", dapr_subscribe),
    path("orders", orders_handler),
]
