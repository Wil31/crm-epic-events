from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from crm.views import ClientViewset, ContractViewset, EventViewset
from users.views import SignupViewset

router = routers.SimpleRouter()

router.register("client", ClientViewset, basename="client")
router.register("contract", ContractViewset, basename="contract")
router.register("event", EventViewset, basename="event")
router.register("signup", SignupViewset, basename="signup")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
