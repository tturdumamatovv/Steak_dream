from django.urls import path

from apps.authentication.api.views import (
    UserLoginView,
    VerifyCodeView,
    UserProfileUpdateView,
    UserAddressCreateAPIView,
    UserAddressUpdateAPIView,
    UserAddressDeleteAPIView,
    UserDeleteAPIView,
    NotificationSettingsAPIView,
    UseBonusesView,
    ApplyPromoCodeView,
    ChildCreateView,
    UserChildrenListView,
    MyPromoCodesView,
)


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_registration'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile'),
    path('addresses/', UserAddressCreateAPIView.as_view(), name='create_address'),
    path('addresses/<int:pk>/update/', UserAddressUpdateAPIView.as_view(), name='update_address'),
    path('addresses/<int:pk>/delete/', UserAddressDeleteAPIView.as_view(), name='delete_address'),
    path('user-delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('notification-settings/', NotificationSettingsAPIView.as_view(), name='notification-settings'),
    path('use-bonuses/', UseBonusesView.as_view(), name='use_bonuses'),
    path('my-promo-codes/', MyPromoCodesView.as_view(), name='my_promo_codes'),
    path('apply-promo-code/', ApplyPromoCodeView.as_view(), name='apply_promo_code'),
    path('add-child/', ChildCreateView.as_view(), name='add_child'),
    path('children/', UserChildrenListView.as_view(), name='user_children'),
]
