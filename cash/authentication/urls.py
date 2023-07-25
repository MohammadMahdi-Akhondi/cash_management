from django.urls import path, include
from rest_framework_simplejwt import views


urlpatterns = [
    path('jwt/', include(([
            path('login/', views.TokenObtainPairView.as_view(), name='login'),
            path('refresh/', views.TokenRefreshView.as_view(), name='refresh'),
        ], 'jwt')),
    ),
]
