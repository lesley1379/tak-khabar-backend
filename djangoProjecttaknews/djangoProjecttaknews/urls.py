"""
URL configuration for djangoProjecttaknews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import LoginView, RegisterView, UserProfileView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
                  # احراز هویت
                  path('api/auth/register/', RegisterView.as_view(), name='register'),  # ثبت‌نام کاربر جدید
                  path('api/auth/login/', LoginView.as_view(), name='login'),  # ورود و دریافت توکن JWT
                  path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # تمدید توکن دسترسی
                  path('api/auth/profile/', UserProfileView.as_view(), name='user_profile'),  # مدیریت پروفایل کاربر

                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('api/', include('news.urls')),  # مسیرهای API اپ نیوز
                  # داکیومنت
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
