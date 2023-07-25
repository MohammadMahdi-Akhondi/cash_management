from django.urls import path, include


urlpatterns = [
    path('v1/user/', include(('cash.user.urls', 'user'))),
    path('v1/', include(('cash.authentication.urls', 'auth'))),
]
