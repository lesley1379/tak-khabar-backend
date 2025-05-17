from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import User


class RegisterView(generics.CreateAPIView):
    """
      register:
      ثبت‌نام کاربر جدید

      پارامترهای مورد نیاز:
      - username: نام کاربری (منحصر به فرد)
      - password: رمز عبور
      - email: آدرس ایمیل (اختیاری)
      - first_name: نام (اختیاری)
      - last_name: نام خانوادگی (اختیاری)

      مثال درخواست:
      {
          "username": "newuser",
          "password": "securepassword123",
          "email": "user@example.com",
          "first_name": "نام",
          "last_name": "خانوادگی"
      }
      """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """
       login:
       ورود کاربر و دریافت توکن JWT

       پارامترهای مورد نیاز:
       - username: نام کاربری
       - password: رمز عبور

       مثال درخواست:
       {
           "username": "existinguser",
           "password": "userpassword"
       }

       پاسخ موفق:
       {
           "refresh": "توکن رفرش",
           "access": "توکن دسترسی",
           "user": {
               "id": 1,
               "username": "existinguser",
               "email": "user@example.com",
               ...
           }
       }
       """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
        get:
        دریافت پروفایل کاربر جاری

        نیاز به احراز هویت دارد.
        توکن دسترسی باید در هدر Authorization ارسال شود.

        put:
        به‌روزرسانی کامل پروفایل کاربر جاری

        نیاز به احراز هویت دارد.
        توکن دسترسی باید در هدر Authorization ارسال شود.

        patch:
        به‌روزرسانی جزئی پروفایل کاربر جاری

        نیاز به احراز هویت دارد.
        توکن دسترسی باید در هدر Authorization ارسال شود.

        فیلدهای قابل به‌روزرسانی:
        - first_name
        - last_name
        - email
        - bio
        - profile_image
        """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AuthorOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_author