from django.urls import path
from rest_framework.routers import DefaultRouter

from server.api.v1.accounts.views import AccountDetailView

router = DefaultRouter()

urlpatterns = [
    path('<str:lookup_value>/', AccountDetailView.as_view(), name='account-detail'),
]

urlpatterns += router.urls
