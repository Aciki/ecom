from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.contrib.auth import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic.base import RedirectView


from apps.cart.views import cart_detail, succes
from apps.core.views import frontpage, contact, about , order_confirmation
from apps.store.views import product_detail, search ,category_detail
from apps.coupon.api import api_can_use
from apps.userprofile.views import signup, myaccount 
from apps.store.api import api_add_to_cart, api_remove_from_cart , api_checkout

from .sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {'static': StaticViewSitemap, 'product': ProductSitemap, 'category': CategorySitemap}




urlpatterns = [
    path("favicon.ico",RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),),
    path('', frontpage, name='frontpage'),
    path('search/', search, name='search'),
    path('signup/', signup, name='signup'),
    path('login/',views.LoginView.as_view(template_name = 'login.html'),name='login'),
    path('logout/',views.LogoutView.as_view(),name = 'logout'),
    path('myaccount/', myaccount, name ='myaccount'),

    path('cart/', cart_detail, name='cart'),
    path('cart/succes/',succes,name = 'succes'),
    path('order_confirmation/',order_confirmation,name = 'order_confirmation'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),

    # API
    path('api/can_use/', api_can_use, name='api_can_use'),
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/checkout/', api_checkout, name='api_checkout'),

     # reset pasword
    path('reset_password/',views.PasswordResetView.as_view(template_name = "password_reset.html"), name="reset_password"),
    path('reset_password_sent/',views.PasswordResetDoneView.as_view(template_name = "password_reset_done.html"), name="password_reset_done"),
    path('reset_password_complete/',views.PasswordResetCompleteView.as_view(template_name = "password_reset_complete.html"), name="password_reset_complete"),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"),name="password_reset_confirm"),


    # Store
    path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:slug>/', category_detail, name='category_detail'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
