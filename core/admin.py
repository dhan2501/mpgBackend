from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Product, MenuItem, SocialMediaLink, Category, Banner, Blog, ProductReview, Subscriber
from django.contrib import admin
from django.contrib.admin import AdminSite

admin.site.site_header = "MPGStone.co.uk"
admin.site.site_title = "MPGStone Admin Portal"
admin.site.index_title = "Welcome to MPGStone Admin"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('category_name', 'slug', 'is_active')  # Columns to display in the admin list
    list_display = ('image_tag','category_name', 'slug', 'is_active')  # add 'image_tag'
    list_display_links = ('image_tag', 'category_name')  # Make 'id' and 'name' clickable

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'name', 'category', 'short_description')  # 👈 Add image_tag here
    list_display_links = ('image_tag', 'name')  # Make 'id' and 'name' clickable

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


# @admin.register(Logo)
# class LogoAdmin(admin.ModelAdmin):
#     list_display = ('title', 'image', 'alt_text')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'parent', 'position','order', 'is_active')
    list_filter = ('parent', 'position', 'is_active')
    ordering = ('order',)


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'location', 'is_active')
    list_filter = ('location', 'is_active')
    search_fields = ('platform', 'url')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'enquiry_button_text', 'enquiry_button_link', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'image_tag')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'date_posted')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'comment')

@admin.register(Subscriber)
class SubscribeAmin(admin.ModelAdmin):
    list_display = ('id','email')