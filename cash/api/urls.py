from django.urls import path, include


urlpatterns = [
    path('v1/user/', include(('cash.user.urls', 'user'))),
]
