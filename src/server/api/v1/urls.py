from django.urls import include, path

from .accounts import urls as urls_accounts

urlpatterns = [
    path('account/', include(urls_accounts))
]
