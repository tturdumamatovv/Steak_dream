from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.authentication.models import (
    User,
    UserAddress, BonusTransaction, Child
)
from core import settings


class UserBonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['bonus', 'qr_code']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'full_name', 'date_of_birth', 'email')
        read_only_fields = ('full_name', 'date_of_birth', 'email')


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
    fcm_token = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    receive_notifications = serializers.BooleanField(required=False, allow_null=True)


class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    has_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'profile_picture', 'full_name', 'date_of_birth', 'gender',
                  'email', 'first_visit', 'has_profile_picture', 'receive_notifications', 'bonus', 'qr_code')
        read_only = ('receive_notifications',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if not ret['profile_picture']:
            if request is not None:
                ret['profile_picture'] = request.build_absolute_uri(settings.DEFAULT_PROFILE_PICTURE_URL)
            else:
                ret['profile_picture'] = settings.DEFAULT_PROFILE_PICTURE_URL
        return ret

    @extend_schema_field(serializers.BooleanField)
    def get_has_profile_picture(self, instance):
        return bool(instance.profile_picture)


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'city', 'apartment_number', 'entrance',
                  'floor', 'intercom', 'created_at', 'is_primary', 'longitude', 'latitude']  # Include 'is_primary'
        read_only_fields = ['user', 'created_at']


class UserAddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [field.name for field in UserAddress._meta.fields if field.name not in ('id', 'user')]


class UserAddressUpdateSerializer(serializers.ModelSerializer):
    city = serializers.CharField(required=False)
    is_primary = serializers.BooleanField(required=False)  # Include 'is_primary' as an optional field

    class Meta:
        model = UserAddress
        fields = ['id', 'user', 'city', 'apartment_number', 'entrance',
                  'floor', 'intercom', 'created_at', 'is_primary', 'longitude', 'latitude']  # Include 'is_primary'
        read_only_fields = ['user', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    fcm_token = serializers.CharField(max_length=255, required=False)
    receive_notifications = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = User
        fields = ('fcm_token', 'receive_notifications')


class UserBalanceSerializer(serializers.ModelSerializer):
    bonus_to_deduct = serializers.DecimalField(max_digits=9, decimal_places=2, required=False, default=10)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'bonus', 'bonus_to_deduct']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'bonus', 'qr_code']


class BonusTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusTransaction
        fields = ['user', 'bonus_spent', 'bonus_earned', 'created_at']


class QRCodeRequestSerializer(serializers.Serializer):
    qr_data = serializers.CharField()
    spent_bonuses = serializers.DecimalField(max_digits=10, decimal_places=2)
    earned_bonuses = serializers.DecimalField(max_digits=10, decimal_places=2)


class PhoneBonusRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, help_text="Enter the user's phone number.")
    spent_bonuses = serializers.IntegerField(help_text="The amount of bonuses to be spent.", min_value=0)
    earned_bonuses = serializers.IntegerField(help_text="The amount of bonuses to be earned.", min_value=0)


class ApplyPromoCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'user', 'name', 'date_of_birth']
        read_only_fields = ['user']


class ChildListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['id', 'name', 'date_of_birth']
