from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
       سریالایزر کاربر

       فیلدها:
       - id: شناسه کاربر
       - username: نام کاربری
       - email: آدرس ایمیل
       - first_name: نام
       - last_name: نام خانوادگی
       - role: نقش کاربر (admin, author, user)
       - bio: بیوگرافی کاربر
       - profile_image: آدرس تصویر پروفایل
       """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'bio', 'profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    """
        سریالایزر ثبت‌نام

        فیلدهای مورد نیاز برای ثبت‌نام:
        - username: نام کاربری (حداقل 5 کاراکتر)
        - password: رمز عبور (حداقل 8 کاراکتر)
        - email: آدرس ایمیل (اختیاری)
        - first_name: نام (اختیاری)
        - last_name: نام خانوادگی (اختیاری)
        """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
       سریالایزر ورود

       فیلدهای مورد نیاز:
       - username: نام کاربری
       - password: رمز عبور
       """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('اطلاعات ورود نامعتبر است')