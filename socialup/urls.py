from django.conf.urls import (
    url,
    include,
    handler400,
    handler403,
    handler404,
    handler500,
)
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from .views import (
    home,
    product_category,
    bad_request,
    permission_denied,
    page_not_found,
    server_error,
)
from accounts.views import dashboard, change_info, account_detail
from markets.views import product_detail, product_upload, product_manage, product_change, product_delete, \
    product_order_manage, product_profit_manage
from billing.views import charge_point, history_point, PointCheckoutAjaxView, PointImpAjaxView, purchase, \
    CheckoutAjaxView, ImpAjaxView, purchase_list, charge_fail, charge_success, pay_success, pay_fail
from carts.views import CartView, WishListView
from messages.views import message_lounge, message_room
from contact.views import contact, contact_history

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'category/(?P<category>\w+)/$', product_category, name='category'),
    # admin app urls
    url(r'^admin/', admin.site.urls),
    # accounts app urls
    url(r'^accounts/', include('accounts.urls')),

    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^dashboard/change/$', change_info, name='change_info'),
    url(r'^dashboard/seller/(?P<seller_id>\d+)/$', account_detail, name='account_detail'),

    url(r'^dashboard/points/charge/$', charge_point, name='point_charge'),
    url(r'^dashboard/points/checkout/$', PointCheckoutAjaxView.as_view(), name='point_checkout'),
    url(r'^dashboard/points/validation/$', PointImpAjaxView.as_view(), name='point_validation'),
    url(r'^dashboard/point/charge/success$', charge_success, name='point_success'),
    url(r'^dashboard/point/charge/fail', charge_fail, name='point_fail'),

    url(r'^dashboard/points/history$', history_point, name='point_history'),
    url(r'^dashboard/purchase/(?P<cart_id>\d+)/$', purchase, name='purchase'),
    url(r'^dashboard/purchase/wishlist/$', WishListView.as_view(), name='wish_list'),
    url(r'^dashboard/purchase/cart/$', CartView.as_view(), name='cart'),
    url(r'^dashboard/purchase/checkout/$', CheckoutAjaxView.as_view(), name='checkout'),
    url(r'^dashboard/purchase/validation/$', ImpAjaxView.as_view(), name='validation'),
    url(r'^dashboard/purchase/list/$', purchase_list, name='purchase_list'),
    url(r'^dashboard/purchase/success/$', pay_success, name='pay_success'),
    url(r'^dashboard/purchase/fail/$', pay_fail, name='pay_fail'),

    url(r'^dashboard/seller/manage/$', product_manage, name='product_manage'),

    url(r'^product/(?P<product_id>\d+)/$', product_detail, name='product_detail'),
    url(r'^product/change/(?P<product_id>\d+)/$', product_change, name='product_change'),
    url(r'^product/order/$', product_order_manage, name='product_order_manage'),
    url(r'^product/profit/$', product_profit_manage, name='product_profit_manage'),
    url(r'^product/delete/$', product_delete, name='product_delete'),
    url(r'^product/upload/$', product_upload, name="product_upload"),

    url(r'^summernote/', include('django_summernote.urls')),

    url(r'^messages/$', message_lounge, name="message_lounge"),
    url(r'^messages/room/$', message_room, name="message_room"),

    url(r'^contact/$', contact, name="contact"),
    url(r'^contact/history/$', contact_history, name="contact_history"),
]

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
