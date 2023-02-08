from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_market, name="market"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('add_basket/', views.add_product_basket, name="add_basket"),
    path('search/', views.search, name="search"),
    path('check_basket/', views.check_basket, name="check_basket"),
    path('product/<int:product_id>/', views.product, name="product"),
    path('new_product/', views.new_product, name="new_product"),
    path('basket/', views.page_basket, name="basket"),
    path('catalog/<int:category_id>', views.subcategory, name="catalog"),
    path('basket_delete/', views.basket_delete, name="basket_delete"),
    path('basket/order/<int:basket_id>/', views.new_order, name="new_order")
]