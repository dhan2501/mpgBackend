from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField

# class Logo(models.Model):
#     title = models.CharField(max_length=255, blank=True, null=True)
#     image = models.ImageField(
#         upload_to='logos/',
#         validators=[FileExtensionValidator(['jpg', 'jpeg', 'svg', 'webp'])],
#     )
#     alt_text = models.CharField(max_length=255, blank=True, null=True)

#     def clean(self):
#         # Validate image content type
#         if self.image:
#             if not self.image.name.endswith(('.jpg', '.jpeg', '.svg', '.webp', '.png')):
#                 raise ValidationError('Invalid file type: only JPG, SVG, and WEBP are allowed.')

#         # Check dimensions or other properties (optional)
#         if self.image.name.endswith(('.jpg', '.jpeg', '.webp')):
#             try:
#                 img = Image.open(self.image)
#                 img.verify()
#             except Exception as e:
#                 raise ValidationError('Uploaded file is not a valid image.')

#     def __str__(self):
#         return self.title if self.title else "Website Logo"
    

class MenuItem(models.Model):
    title = models.CharField(max_length=100, help_text="The display name of the menu item.")
    url = models.CharField(max_length=255, unique=True, blank=True, help_text="URL or path for the menu item.")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        help_text="Parent menu item, if any (for dropdown menus)."
    )
    POSITION_CHOICES = [
        ('header', 'Header'),
        ('footer', 'Footer'),
        ('both', 'Both'),
    ]
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='both')
    order = models.PositiveIntegerField(default=0, help_text="Order of the menu item.")
    is_active = models.BooleanField(default=True, help_text="Whether the menu item is active.")

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(self.title)
        super().save(*args, **kwargs)
    # def __str__(self):
    #     return self.title
    def __str__(self):
        return self.title or (self.category.name if self.category else "Unnamed Item")
    


class SocialMediaLink(models.Model):
    
    platform = models.CharField(max_length=50, choices=[
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('other', 'Other'),
    ])
    url = models.URLField(max_length=200, unique=True, blank=True)

    icon_class = models.CharField(max_length=100, blank=True, null=True)  # Font Awesome or custom icon classes
    is_active = models.BooleanField(default=True)  

    class Meta:
        ordering = ['platform']

class Category(models.Model):
    category_name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True) 
    short_description = models.TextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)  # <-- CKEditor field
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('category_name',)

    def __str__(self):
        return self.category_name 


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True) # example slug field
    category = models.ForeignKey(Category,related_name='product', on_delete= models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # SEO fields
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.alt_text or 'Gallery Image'}"


class Banner(models.Model):
    title = models.CharField(max_length=255, help_text="Main title text for the banner.")
    subtitle = models.CharField(max_length=255, blank=True, null=True, help_text="Subtitle or supporting text.")
    image = models.ImageField(
        upload_to='banners/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Upload a banner image (JPG, PNG, WEBP)."
    )
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    enquiry_button_text = models.CharField(max_length=100, default='Enquire Now', help_text="Text shown on the enquiry button.")
    enquiry_button_link = models.URLField(help_text="URL the enquiry button should link to.")

    def __str__(self):
        return self.title or "Banner" 


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    # category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blogs', blank=True)
    meta_title = models.CharField(max_length=255, help_text="Meta title for SEO", blank=True)
    meta_description = models.TextField(help_text="Meta description for SEO", blank=True)
    # content = models.TextField(help_text="Page content")
    content = RichTextField()
    date_posted = models.DateTimeField(default=now)
    # total_views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)  # Inactive by default

    def __str__(self):
        return f"Review by {self.name} on {self.product.name}"
    

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)  # e.g. Materials, Application
    value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.product.name}"
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveIntegerField(default=5)
    title = models.CharField(max_length=255)
    testimonial = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = PhoneNumberField(blank=False, null=False) # Default region can be changed
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    


class ContactDetail(models.Model):
    phones = models.TextField(help_text="Separate multiple numbers with commas")
    emails = models.TextField(help_text="Separate multiple emails with commas")
    address = models.TextField()

    def get_phone_list(self):
        return [p.strip() for p in self.phones.split(',') if p.strip()]

    def get_email_list(self):
        return [e.strip() for e in self.emails.split(',') if e.strip()]

    def __str__(self):
        return f"{self.phones} - {self.emails}"
    

class Enquiry(models.Model):
    product_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Enquiry by {self.name} for {self.product_name}'