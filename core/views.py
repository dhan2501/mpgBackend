from django.http import JsonResponse
import json
from .models import Product, Banner, Category, MenuItem, Blog, ProductReview, Subscriber
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductReview
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
# from .serializers import ProductReviewSerializer
from  core.serializers import ProductSerializer, ProductReviewSerializer
from .models import Product, ProductReview

def index(request):
    return render(request, "index.html")

def menu_list(request):
    menuitems = list(MenuItem.objects.values())
    return JsonResponse(menuitems, safe=False)

# def product_list(request):
#     products = list(Product.objects.values())
#     return JsonResponse(products, safe=False)
def product_list_api(request):
    products = Product.objects.all()
    data = []

    for product in products:
        image_url = request.build_absolute_uri(product.image.url) if product.image else None
        data.append({
            "name": product.name,
            "image": image_url,
        })

    return JsonResponse(data, safe=False)

def category_list(request):
    # categories = list(Category.objects.values())
    # return JsonResponse(categories, safe=False)
    categories = Category.objects.filter(is_active=True)
    data = []

    for category in categories:
        data.append({
            "id": category.id,
            "category_name": category.category_name,
            "slug": category.slug,
            "image": request.build_absolute_uri(category.image.url) if category.image else None,
            "is_active": category.is_active
        })

    return JsonResponse(data, safe=False)


def banner_api(request):
    banners = Banner.objects.all()
    data = []

    for banner in banners:
        image_url = request.build_absolute_uri(banner.image.url) if banner.image else None

        data.append({
            "id": banner.id,
            "title": banner.title,
            "subtitle": banner.subtitle,
            "image": image_url,
            "enquiry_button_text": banner.enquiry_button_text,
            "enquiry_button_link": banner.enquiry_button_link,
        })

    return JsonResponse(data, safe=False)

# def blog_list(request):
#     blogs = list(Blog.objects.values())
#     return JsonResponse(blogs, safe=False)

def blog_list(request):
    blogs = Blog.objects.all()
    blog_data = []

    for blog in blogs:
        image_url = request.build_absolute_uri(blog.image.url) if blog.image else None
        blog_data.append({
            "id": blog.id,
            "title": blog.title,
            "descriptions": blog.description,
            "image": image_url,
            "meta_title" : blog.meta_title,
            "meta_description" : blog.meta_description
            # add other fields if needed
        })
    
    return JsonResponse(blog_data, safe=False)

def product_api(request, pk):
    product = get_object_or_404(Product, id=pk)
    image_url = request.build_absolute_uri(product.image.url) if product.image else None
    data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "image": image_url,
    }
    return JsonResponse(data)
    
@csrf_exempt
@api_view(['GET'])
def reviews_list(request):
    reviews = list(ProductReview.objects.values())
    return JsonResponse(reviews, safe=False)

# csrf_exempt
# @api_view(['POST'])
# def reviews_list(request):
#     print("POST DATA:", request.data)  # 👈 Debug
#     serializer = ProductReviewSerializer(data=request.data)
#     if serializer.is_valid():
#         review = serializer.save()
#         print("Saved Review:", review)  # 👈 Debug
#         return Response({'message': 'Review submitted successfully!'}, status=status.HTTP_201_CREATED)
#     else:
#         print("Serializer errors:", serializer.errors)  # 👈 Debug
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt  # Exempt CSRF for frontend JS forms
# @api_view(['GET', 'POST'])
# def reviews_list(request):
#     if request.method == 'GET':
#         reviews = ProductReview.objects.all()
#         serializer = ProductReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ProductReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Review submitted!'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt  # Allow AJAX POST without CSRF token
# @api_view(['GET', 'POST'])
# def reviews_list(request):
#     if request.method == 'GET':
#         reviews = ProductReview.objects.all()
#         serializer = ProductReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ProductReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Review submitted!'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

@api_view(['GET'])
def product_reviews(request, pk):
    try:
        reviews = ProductReview.objects.filter(product_id=pk, is_active=True)
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except ProductReview.DoesNotExist:
        return Response([], status=200)

@api_view(['GET', 'POST'])
def reviews_list(request):
    if request.method == 'GET':
        reviews = ProductReview.objects.filter(is_active=True)
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Review submitted!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# without popup thankyou page
# def submit_review(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         comment = request.POST.get('comment')

#         ProductReview.objects.create(
#             name=name,
#             email=email,
#             comment=comment,
#             is_active=False  # Default; can be omitted
#         )
#         return redirect('thank_you')  # Redirect after submission

#     return render(request, 'reviews/review_form.html')

# With popup
def submit_review(request):
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')

        ProductReview.objects.create(
            name=name,
            email=email,
            comment=comment,
            is_active=False
        )
        success = True  # trigger popup

    return render(request, 'reviews/review_form.html', {'success': success})

def thank_you(request):
    return render(request, 'thank_you.html')



from django.shortcuts import render
from .models import Blog

def create_blog(request):
    success = False

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        content = request.POST.get('content')

        Blog.objects.create(
            title=title,
            description=description,
            image=image,
            meta_title=meta_title,
            meta_description=meta_description,
            content=content
        )

        success = True

    return render(request, 'blog/blog_form.html', {'success': success})

# def blog_success(request):
#     return render(request, 'blog/blog_success.html')


def products_list(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'product.html', {'products': products})

def products_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})


@csrf_exempt  # For simplicity, exempt CSRF (better to use csrf token in production)
def subscribe_api(request):
    if request.method == "GET":
        return JsonResponse({"message": "API is working, send POST to subscribe"})
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)
            
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                return JsonResponse({"message": "Successfully subscribed"}, status=201)
            else:
                return JsonResponse({"message": "Email already subscribed"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

def subscribe_page(request):
    return render(request, 'subscribe.html')