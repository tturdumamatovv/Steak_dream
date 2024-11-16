from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "DASHBOARD_CALLBACK": "apps.common.views.dashboard_callback",
    "SITE_TITLE": "Админ панель Steak Dream",
    "SITE_HEADER": "Админ панель Steak Dream",
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
    # # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo-light.svg"),  # light mode
    #     "dark": lambda request: static("logo-dark.svg"),  # dark mode
    # },
    "SITE_SYMBOL": "settings",  # symbol from icon set
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/svg+xml",
    #         "href": lambda request: static("favicon.svg"),
    #     },
    # ],
    "SHOW_HISTORY": False,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    # "ENVIRONMENT": "sample_app.environment_callback",
    # "DASHBOARD_CALLBACK": "sample_app.dashboard_callback",
    # "LOGIN": {
    #     "image": lambda request: static("sample/login-bg.jpg"),
    #     "redirect_after": lambda request: reverse_lazy(
    #         "admin:authentication_user_changelist"
    #     ),
    # },
    "STYLES": [
        lambda request: static("css/style.css"),
        # lambda request: static("css/bootstrap.min.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/admin_notifications.js"),
        # lambda request: static("js/bootstrap.bundle.min.js"),
    ],
    "COLORS": {
        "font": {
            "subtle-light": "107 114 128",
            "subtle-dark": "156 163 175",
            "default-light": "75 85 99",
            "default-dark": "209 213 219",
            "important-light": "17 24 39",
            "important-dark": "243 244 246",
        },
        "primary": {
            "50": "255 244 230",
            "100": "255 230 204",
            "200": "255 215 179",
            "300": "255 196 143",
            "400": "255 171 87",
            "500": "255 145 0",
            "600": "234 128 0",
            "700": "202 111 0",
            "800": "171 92 0",
            "900": "140 74 0",
            "950": "112 59 0",
        },
    },
    # "EXTENSIONS": {
    #     "modeltranslation": {
    #         "flags": {
    #             "en": "🇬🇧",
    #             "fr": "🇫🇷",
    #             "nl": "🇧🇪",
    #         },
    #     },
    # },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Чат"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Чат поддержки"),
                        "icon": "forum",
                        "link": reverse_lazy("admin-chat-list"),
                    },
                ],
            },
            {
                "title": _("Пользователи"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Пользователи"),
                        "icon": "person",
                        "link": reverse_lazy("admin:authentication_user_changelist"),
                    },
                    {
                        "title": _("Группы"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": _("Адреса пользователей"),
                        "icon": "location_on",
                        "link": reverse_lazy(
                            "admin:authentication_useraddress_changelist"
                        ),
                    },
                    {
                        "title": _("Транзакции бонусов"),
                        "icon": "account_balance",
                        "link": reverse_lazy("admin:authentication_bonustransaction_changelist"),
                    },
                ],
            },
            {
                "title": _("Настройки бонусной системы"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Настройки"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:authentication_bonussystemsettings_changelist"),
                    },
                ],
            },
            {
                "title": _("Магазин"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Категории"),
                        "icon": "storefront",
                        "link": reverse_lazy("admin:catalog_category_changelist"),
                    },
                    {
                        "title": _("Товары"),
                        "icon": "package_2",
                        "link": reverse_lazy("admin:catalog_product_changelist"),
                    },
                    {
                        "title": _("Заказы"),
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                    },
                    {
                        "title": _("Акционные товары"),
                        "icon": "deployed_code_alert",
                        "link": reverse_lazy("admin:catalog_promotionalproduct_changelist"),
                    },
                    {
                        "title": _("Промокоды"),
                        "icon": "app_promo",
                        "link": reverse_lazy("admin:authentication_promocode_changelist"),
                    },
                ],
            },
            {
                "title": _("Контент сайта"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Баннеры"),
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:pages_banner_changelist"),
                    },
                    {
                        "title": _("Рекламные объявления"),
                        "icon": "campaign",
                        "link": reverse_lazy("admin:pages_advertisement_changelist"),
                    },
                    {
                        "title": _("Сторисы"),
                        "icon": "web_stories",
                        "link": reverse_lazy("admin:pages_stories_changelist"),
                    },
                    {
                        "title": _("Главная страница"),
                        "icon": "home",
                        "link": reverse_lazy("admin:pages_mainpage_changelist"),
                    },
                    {
                        "title": _("Бонусная страница"),
                        "icon": "request_page",
                        "link": reverse_lazy("admin:pages_bonuspage_changelist"),
                    },
                    {
                        "title": _("Статические страницы"),
                        "icon": "description",
                        "link": reverse_lazy("admin:pages_staticpage_changelist"),
                    },
                    {
                        "title": _("Контакты"),
                        "icon": "phone_in_talk",
                        "link": reverse_lazy("admin:pages_contacts_changelist"),
                    },
                    {
                        "title": _("Настройки сайта"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:pages_sitesettings_changelist"),
                    },
                    {
                        "title": _("Доступные способы оплаты"),
                        "icon": "payment",
                        "link": reverse_lazy("admin:pages_availablepaymentmethods_changelist"),
                    },
                ],
            },
            {
                "title": _("ЯРОС"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Поставщики"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:yaros_connector_supplier_changelist"),
                    },
                    # {
                    #     "title": _("Выполненные задачи"),
                    #     "icon": "checklist",
                    #     "link": reverse_lazy("admin:background_task_completedtask_changelist"),
                    # },
                    # {
                    #     "title": _("Задачи в очереди"),
                    #     "icon": "sync",
                    #     "link": reverse_lazy("admin:background_task_task_changelist"),
                    # },
                ],
            },
{
                "title": _("Общие Настройки"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Настройки Google Карты"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:orders_googlemap_changelist"),
                    },
                ],
            },
            {
                "title": _("Рестораны"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Список ресторанов"),
                        "icon": "restaurant",
                        "link": reverse_lazy("admin:orders_restaurant_changelist"),
                    },
                ],
            },
        ],
    },
    # "TABS": [
    #     {
    #         "models": [
    #             "app_label.model_name_in_lowercase",
    #         ],
    #         "items": [
    #             {
    #                 "title": _("Your custom title"),
    #                 "link": reverse_lazy("admin:app_label_model_name_changelist"),
    #                 "permission": "sample_app.permission_callback",
    #             },
    #         ],
    #     },
    # ],
}