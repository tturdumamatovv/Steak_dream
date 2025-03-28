from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, permissions, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import exception_handler
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from apps.authentication.models import (
    User,
    UserAddress, BonusTransaction, PromoCode, Child, BonusSystemSettings
)
from apps.authentication.utils import (
    send_sms,
    generate_confirmation_code
)
from apps.catalog.models import Product
from apps.orders.models import Order, OrderItem  # Импортируйте модель заказа из приложения orders
from .serializers import (
    CustomUserSerializer,
    VerifyCodeSerializer,
    UserProfileSerializer,
    UserAddressSerializer,
    UserAddressUpdateSerializer,
    NotificationSerializer,
    UserBonusSerializer, QRCodeRequestSerializer, PhoneBonusRequestSerializer, ChildSerializer, ChildListSerializer,
    ApplyPromoCodeSerializer, PromoCodeSerializer
)


class UserBonusView(generics.GenericAPIView):
    serializer_class = UserBonusSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # if not phone_number.startswith("+996"):
        #     return Response({'error': 'Phone number must start with "+996".'}, status=status.HTTP_400_BAD_REQUEST)
        if len(phone_number) != 13:
            return Response({'error': 'Phone number must be 13 digits long including the country code.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif not phone_number[4:].isdigit():
            return Response(
                {'error': 'Invalid characters in phone number. Only digits are allowed after the country code.'},
                status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = generate_confirmation_code()
        send_sms(phone_number, confirmation_code)

        User.objects.update_or_create(
            phone_number=phone_number,
            defaults={'code': confirmation_code}
        )

        response_data = {
            'message': 'Confirmation code sent successfully.',
            'code': confirmation_code
        }
        return Response(response_data, status=status.HTTP_200_OK)


class VerifyCodeView(generics.CreateAPIView):
    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        fcm_token = serializer.validated_data.get('fcm_token')
        receive_notifications = serializer.validated_data.get('receive_notifications')

        # Захардкоженный код и номер телефона
        hardcoded_code = '1234'
        hardcoded_phone_number = '+996123456789'

        user = User.objects.filter(code=code).first()

        # Проверка захардкоженного кода
        if code == hardcoded_code:
            user = User.objects.filter(phone_number=hardcoded_phone_number).first()

        if not user:
            return Response({'error': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.code = None

        if fcm_token is not None:
            user.fcm_token = fcm_token
        if receive_notifications is not None:
            user.receive_notifications = receive_notifications

        user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
            'first_visit': user.first_visit
        }, status=status.HTTP_200_OK)


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        profile_picture = request.data.get('profile_picture')

        # Set default profile picture if none is provided
        if not profile_picture and not instance.profile_picture:
            instance.profile_picture = settings.DEFAULT_PROFILE_PICTURE_URL

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if all(serializer.validated_data.get(field) for field in ['full_name', 'date_of_birth', 'email']):
            instance.first_visit = False
            instance.save()

        return Response(serializer.data)

    def handle_exception(self, exc):
        response = exception_handler(exc, self)
        if response is not None and response.status_code == status.HTTP_400_BAD_REQUEST:
            # Extract first error message
            error_message = next(iter(response.data.values()))[0]
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        return super().handle_exception(exc)


class UserAddressCreateAPIView(generics.ListCreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserAddress.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(user=user)


class UserAddressUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user

        # Check if 'is_primary' is set to True
        if serializer.validated_data.get('is_primary', False):
            # Set 'is_primary' of all other addresses to False for this user
            UserAddress.objects.filter(user=user, is_primary=True).update(is_primary=False)

        # Perform the update
        serializer.save()


class UserAddressDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserAddress.objects.filter(user=user)


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()  # Удаляем пользователя

        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class NotificationSettingsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        fcm_token = request.data.get('fcm_token')
        receive_notifications = request.data.get('receive_notifications')

        if fcm_token is not None:
            user.fcm_token = fcm_token
            user.save()

        if receive_notifications is not None:
            user.receive_notifications = receive_notifications
            user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UseBonusesView(APIView):

    @extend_schema(
        request=QRCodeRequestSerializer,
        responses={200: 'Bonuses used successfully'}
    )
    def post(self, request):
        serializer = QRCodeRequestSerializer(data=request.data)
        if serializer.is_valid():
            qr_data = serializer.validated_data['qr_data']
            spent_bonuses = serializer.validated_data['spent_bonuses']
            earned_bonuses = serializer.validated_data['earned_bonuses']

            try:
                phone_number, secret_key = qr_data.split('%')
                user = User.objects.get(phone_number=phone_number, secret_key=secret_key)

                if user.bonus < spent_bonuses:
                    return Response({"error": "Insufficient bonuses"}, status=status.HTTP_400_BAD_REQUEST)

                user.bonus -= spent_bonuses
                user.bonus += earned_bonuses
                user.regenerate_secret_key()

                BonusTransaction.objects.create(
                    user=user,
                    bonus_spent=spent_bonuses,
                    bonus_earned=earned_bonuses
                )

                # Здесь вы можете добавить товары в заказ, если они известны
                order = Order.objects.create(
                    user=user,
                    bonus_spent=spent_bonuses,  # Или другое значение, если нужно
                    bonus_earned=earned_bonuses,  # Установите значение, если есть
                    status='completed'
                )
                product_ids = request.data.get('product_ids', [])
                print(product_ids)

                for product_id in product_ids:
                    product = Product.objects.get(supplier_id=product_id)
                    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, quantity=1,
                                                                          amount=product.price)
                    if not created:
                        order_item.quantity += 1
                        order_item.amount += product.price
                        order_item.save()
                    order.total += product.price
                    order.save()
                user.save()

                return Response({
                    'message': 'Bonuses used successfully',
                    'new_bonus': user.bonus,
                    'new_qr_code': user.qr_code.url,
                }, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"error": "Invalid QR code"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyPromoCodesView(generics.ListAPIView):
    serializer_class = PromoCodeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        return PromoCode.objects.filter(
            Q(expiration_date__gte=now) | Q(expiration_date__isnull=True),
            Q(users__in=[user]) | Q(is_personal=False),
            usage_limit__gt=0
        )


# class UseBonusesByPhoneView(APIView):
#
#     @extend_schema(
#         request=PhoneBonusRequestSerializer,
#         responses={200: 'Bonuses used successfully'}
#     )
#     def post(self, request):
#         serializer = PhoneBonusRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']
#             spent_bonuses = serializer.validated_data['spent_bonuses']
#             earned_bonuses = serializer.validated_data['earned_bonuses']
#
#             try:
#                 user = User.objects.get(phone_number=phone_number)
#
#                 if user.bonus < spent_bonuses:
#                     return Response({"error": "Insufficient bonuses"}, status=status.HTTP_400_BAD_REQUEST)
#
#                 user.bonus -= spent_bonuses
#                 user.bonus += earned_bonuses
#                 user.regenerate_secret_key()  # Если нужно сгенерировать новый секретный ключ
#
#                 BonusTransaction.objects.create(
#                     user=user,
#                     bonus_spent=spent_bonuses,
#                     bonus_earned=earned_bonuses
#                 )
#
#                 user.save()
#
#                 return Response({
#                     'message': 'Bonuses used successfully',
#                     'new_bonus': user.bonus,
#                     'new_qr_code': user.qr_code.url,  # Если QR код всё ещё нужен
#                 }, status=status.HTTP_200_OK)
#
#             except User.DoesNotExist:
#                 return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplyPromoCodeView(generics.GenericAPIView):
    serializer_class = ApplyPromoCodeSerializer

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        promo_code = PromoCode.objects.filter(code=code).first()
        print(request.user)
        print(promo_code)

        if promo_code and promo_code.apply_to_user(request.user):
            return Response({"message": "Промокод успешно применен!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Промокод недействителен или уже использован."},
                            status=status.HTTP_400_BAD_REQUEST)


class ChildCreateView(generics.CreateAPIView):
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        # Поддержка списка объектов
        if isinstance(self.request.data, list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


class UserChildrenListView(generics.ListAPIView):
    serializer_class = ChildListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Child.objects.filter(user=self.request.user)
