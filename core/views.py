from django.http import JsonResponse
import json
from .models import Product, Banner, Category, MenuItem, Blog, ProductReview, Subscriber, Testimonial,ProductAttribute, SocialMediaLink, ContactDetail
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductReview
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from django.views.decorators.csrf import csrf_exempt
# from .serializers import ProductReviewSerializer
from  core.serializers import ProductSerializer, ProductReviewSerializer
from .models import Product, ProductReview

from rest_framework.views import APIView
from .serializers import ReviewSerializer, ContactMessageSerializer, ContactDetailSerializer
from django.utils.timezone import now

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
            "id" : product.id,
            "name": product.name,
            "slug" : product.slug,
            "image": image_url,
            "category": product.category.category_name,  # or product.category.id if you want the ID
            "descriptions": product.description,
            "meta_title": product.meta_title,
            "meta_description": product.meta_description,
            "og_title": product.og_title,
            "og_decriptions": product.og_description
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


def blog_list(request):
    blogs = Blog.objects.all()
    blog_data = []

    for blog in blogs:
        image_url = request.build_absolute_uri(blog.image.url) if blog.image else None
        blog_data.append({
            "id": blog.id,
            "title": blog.title,
            "slug": blog.slug,
            "description": blog.description,
            "image": image_url,
            "meta_title": blog.meta_title,
            "meta_description": blog.meta_description,
            "content": blog.content,
            "date_posted": blog.date_posted.strftime("%Y-%m-%d %H:%M:%S") if blog.date_posted else None
        })

    response = {
        "current_time": now().strftime("%Y-%m-%d %H:%M:%S"),
        "blogs": blog_data
    }

    return JsonResponse(response)

def product_api(request, pk):
    product = get_object_or_404(Product, id=pk)
    image_url = request.build_absolute_uri(product.image.url) if product.image else None

    # Fetch all attributes related to the product
    attributes = product.attributes.all().values('title', 'value')

    data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "image": image_url,
        "attributes": list(attributes),  # Convert queryset to list of dicts
    }

    return JsonResponse(data)

    
@csrf_exempt
@api_view(['GET'])
def reviews_list(request):
    reviews = list(ProductReview.objects.values())
    return JsonResponse(reviews, safe=False)


@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)


# without popup thankyou page
def submit_review(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')

        ProductReview.objects.create(
            name=name,
            email=email,
            comment=comment,
            is_active=False  # Default; can be omitted
        )
        return redirect('thank_you')  # Redirect after submission

    return render(request, 'reviews/review_form.html')

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
    # if request.method == "GET":
    #     return JsonResponse({"message": "API is working, send POST to subscribe"})
    if request.method == "GET":
        subscribers = Subscriber.objects.all().values('id', 'email')
        return JsonResponse({"subscribers": list(subscribers)}, safe=False)
    
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


def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    testimonial_data = []

    for t in testimonials:
        image_url = request.build_absolute_uri(t.profile_image.url) if t.profile_image else None
        testimonial_data.append({
            "id": t.id,
            "name": t.name,
            "verified": t.verified,
            "profile_image": image_url,
            "rating": t.rating,
            "title": t.title,
            "testimonial": t.testimonial
        })

    response = {
        "current_time": now().strftime("%Y-%m-%d %H:%M:%S"),
        "testimonials": testimonial_data
    }

    return JsonResponse(response)



class CreateReviewAPIView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        reviews = ProductReview.objects.filter(product=product, is_active=True).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['product'] = product.id

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ContactMessageView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message received successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



def social_media_links(request):
    links = SocialMediaLink.objects.all()
    link_data = []

    for link in links:
        link_data.append({
            "id": link.id,
            "platform": link.platform,
            "iconclass" : link.icon_class,
            "url": link.url if hasattr(link, 'url') else None  # Add this field in your model if needed
            
        })

    response = {
        "current_time": now().strftime("%Y-%m-%d %H:%M:%S"),
        "social_media_links": link_data
    }

    return JsonResponse(response)


class ContactDetailView(generics.RetrieveAPIView):
    
    serializer_class = ContactDetailSerializer

    def get_object(self):
        # Return the first ContactDetail entry
        return ContactDetail.objects.first()