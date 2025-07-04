from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Product, MenuItem, SocialMediaLink, Category, Banner, Blog, ProductReview, Subscriber, Testimonial, ContactMessage, ProductAttribute, ContactDetail, ProductGallery, Enquiry
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django import forms


admin.site.site_header = "MPGStone.co.uk"
admin.site.site_title = "MPGStone Admin Portal"
admin.site.index_title = "Welcome to MPGStone Admin"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'category_name', 'slug', 'is_active', 'product_count')  # Added product_count
    list_display_links = ('image_tag', 'category_name')  # Make 'image' and 'name' clickable

    def product_count(self, obj):
        return obj.product.count()
    product_count.short_description = 'Product Count'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline, ProductGalleryInline]
    list_display = ('id', 'image_tag', 'name', 'category', 'short_description')  # 👈 Add image_tag here
    list_display_links = ('image_tag', 'name')  # Make 'id' and 'name' clickable
    list_filter = ['category']

    def image_tag(self, obj):
        if obj.image:  # assuming your model has an ImageField named `image`
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'  # 👈 This will set the column name to 'Image'

    def short_description(self, obj):
        # Assuming 'description' is a field in the model and is a string
        words = obj.description.split()[:20]  # Split the description into words and take the first 20
        return ' '.join(words)  # Join the words back into a string
    short_description.short_description = 'Description'  # Set the column name to 'Description'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent', 'position','order', 'is_active')
    list_filter = ('parent', 'position', 'is_active')
    ordering = ('order',)


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'is_active')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'enquiry_button_text', 'enquiry_button_link', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'


# @admin.register(Blog)
# class BlogAdmin(admin.ModelAdmin):
#     list_display = ('title', 'date_posted', 'image_tag')
#     prepopulated_fields = {'slug': ('title',)}
#     list_filter = ('title', 'date_posted')

#     def image_tag(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
#         return "-"
#     image_tag.short_description = 'Image'

# Define a custom form for the Blog model
class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'  # Include all fields in the form
        widgets = {
            'content': CKEditorWidget(),  # Using CKEditor for the content field
        }

# Register Blog model with a custom admin interface
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm  # Use the custom form with CKEditor
    list_display = ('title', 'date_posted', 'image_tag')  # Customize list display
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug from title
    list_filter = ('title', 'date_posted')  # Filter by title and date posted

    # Custom method for displaying image as a thumbnail in the list view
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'  # Customize column name for the image tag

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'display_rating', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'comment')

    def display_rating(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    display_rating.short_description = 'Rating'

@admin.register(Subscriber)
class SubscribeAmin(admin.ModelAdmin):
    list_display = ('id','email')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'verified', 'rating')
    list_filter = ('verified', 'rating')
    search_fields = ('name', 'title', 'testimonial')
    readonly_fields = ('profile_image_preview',)
    fields = ('name', 'verified', 'profile_image', 'profile_image_preview', 'rating', 'title', 'testimonial')
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" width="100" height="100" style="object-fit:cover; border-radius:8px;" />')
        return "No image"

    profile_image_preview.short_description = 'Image Preview'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone_number', 'message', 'created_at']
    search_fields = ['name', 'email', 'phone_number', 'message']
    list_filter = ['created_at']
    readonly_fields = ['id', 'created_at']

@admin.register(ContactDetail)
class ContactDetailAdmin(admin.ModelAdmin):
    list_display = ('display_phones', 'display_emails', 'address')
    search_fields = ('phones', 'emails', 'address')

    def display_phones(self, obj):
        return ", ".join(obj.get_phone_list())
    display_phones.short_description = 'Phone Numbers'

    def display_emails(self, obj):
        return ", ".join(obj.get_email_list())
    display_emails.short_description = 'Email Addresses'


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'name', 'email', 'phone_number', 'created_at')
    search_fields = ('product_name', 'name', 'email')