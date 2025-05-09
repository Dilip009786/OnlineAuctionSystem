"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from mainapp import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('profile/', views.user_profile, name='profile'),
    path('dpprofile/', views.dpuser_profile, name='dpprofile'),
    path('test/', views.test_view, name="test"),
    path('registration/', views.registration, name="registration"),
    path('login/', views.login_view, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('process_registration/', views.register, name='process_registration'),
    path('category/', views.add_or_edit_category, name="add_category"),
    path('category/edit/<int:category_id>/', views.add_or_edit_category, name='edit_category'),
    path('display_category/', views.display_category, name="display_category"),
    path('product/', views.add_edit_product, name="add_product"),
    path('product/edit/<int:product_id>/', views.add_edit_product, name='edit_product'),
    path('display_product/', views.display_product, name="display_product"),
    path('admin_wishlist/', views.admin_wishlist, name='admin_wishlist'),  # View wishlist
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # Add to wishlist
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # Remove from wishlist
    path('create-bid/', views.add_edit_bid, name='admin_create_bid'),
    path('bid/edit/<int:bid_id>/', views.add_edit_bid, name='edit_bid'),
    path('bidding/<int:bid_id>/change_status/', views.change_bidding_status, name='change_bidding_status'),
    path('bidding_list/', views.bidding_list_view, name='bidding_list'),
    path('deliveryperson/', views.add_edit_deliveryperson, name='add_deliveryperson'),
    path('deliveryperson/edit/<int:deliveryperson_id>/', views.add_edit_deliveryperson, name='edit_deliveryperson'),
    path('display_deliveryperson/', views.display_deliveryperson, name='display_deliveryperson'),
    path('order/', views.add_order, name='order'),
    path('order/edit/<int:order_id>/', views.add_order, name='edit_order'),
    path('display_order/', views.display_order, name='display_order'),
    path('delete/<str:model_name>/<int:object_id>/', views.delete_object, name='delete_object'),
    path('admin_wishlist/', views.admin_wishlist, name='admin_wishlist'),
    # user side
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('home/', views.home, name="home"),
    path('auction/', views.all_auction, name='all_auction'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('auction_detail/<int:product_id>/', views.auction_detail, name='auction_detail'),
    path('place_bid/<int:product_id>/', views.place_bid, name='place_bid'),   
    path('sell_product/', views.user_add_product, name="sell_product"),
    path('watch_product/', views.user_watch_product, name="watch_product"),
    path('bids/', views.bids, name="bids"),
    path('order_create/<int:bid_id>/', views.order_create, name='order_create'),
    path('user_order/', views.user_order, name='user_order'),
    # delivery person
    path('deliverydashboard/', views.deliverydashboard, name="deliverydashboard"),
    path('order_delivery/', views.order_delivery, name="order_delivery"),
    path('order_delivery/edit/<int:order_id>/', views.edit_order_delivery, name="edit_order_delivery"),
    path('order/<int:order_id>/invoice/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('upload-products/', views.upload_products, name='upload_products'),
    path('download-products/', views.download_products, name='download_products'),

]
