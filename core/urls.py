
from django.urls import path
from . import views
from core.views import index

urlpatterns = [
    path('api/products/', views.product_list_api, name='product_list_api'),
    path('api/banners/', views.banner_api, name='banner-list'),
    path('api/categories/', views.category_list, name='category-list'),
    path('api/menuitems/', views.menu_list, name='menu-list'),
    path('api/blogs/', views.blog_list, name='blog-list'),
    path('api/reviews/', views.reviews_list, name='reviews-list'),
    path('submit-review/', views.submit_review, name='submit_review'),
    # path('thank-you/', views.thank_you, name='thank_you'),  # Add this if you want a thank-you page
    path('create-blog/', views.create_blog, name='create_blog'),
    # path('blog-success/', views.blog_success, name='blog_success'),  # Optional success page

    # path('api/products/<int:pk>/', views.product_detail, name='product-detail'),
    # path('api/products/<int:pk>/reviews/', views.product_reviews, name='product-reviews'),
    # path('api/reviews/', views.reviews_list, name='submit-review'),
    # path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/', views.products_list, name='product_list'),
    path('api/products/<int:pk>/', views.product_api, name='product_api'),
    path('products/<int:pk>/', views.products_detail, name='product_detail'),
    path('api/subscribe/', views.subscribe_api, name='subscribe_api'),
    path('subscribe/', views.subscribe_page, name='subscribe_page'),
    # path('products/<slug:category_slug>/<int:pk>/', views.products_detail, name='product_detail'),
]
