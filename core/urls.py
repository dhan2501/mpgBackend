
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
    path('create-blog/', views.create_blog, name='create_blog'),
    path('products/', views.products_list, name='product_list'),
    path('api/products/<int:pk>/', views.product_api, name='product_api'),
    path('products/<int:pk>/', views.products_detail, name='product_detail'),
    path('api/subscribe/', views.subscribe_api, name='subscribe_api'),
    path('subscribe/', views.subscribe_page, name='subscribe_page'),
    path('api/testimonials/', views.testimonial_list, name='testimonial-list'),
    path('api/products/<int:product_id>/reviews/', views.CreateReviewAPIView.as_view(), name='create-review'),
    path('api/contact/', views.ContactMessageView.as_view(), name='contact-message'),
]
