from rest_framework import serializers
from .models import ProductReview, Product, Testimonial, ContactMessage, ContactDetail
from phonenumber_field.serializerfields import PhoneNumberField as PhoneNumberSerializerField
class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'

        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'verified', 'profile_image', 'rating', 'title', 'testimonial']

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'name', 'email', 'rating', 'comment', 'created_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone_number', 'message']


class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = '__all__'