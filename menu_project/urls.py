from django.contrib import admin
from django.urls import path
from tree_menu import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('products/', views.products_view, name='products'),
    path('contacts/', views.contacts_view, name='contacts'),

    # второй уровень
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),

    # третий уровень
    path('products/<int:pk>/<int:subpk>/', views.product_sub_detail_view, name='product_sub_detail'),

    path('term/', views.term_view, name='term'),
    path('privacy/', views.privacy_view, name='privacy'),
]
