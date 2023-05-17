from django.contrib import admin
from .models import Review
from .forms import ReviewForm

# 생략

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm