from django.contrib import admin
from .models import Post, Categories

# Register your models here.
admin.site.register(Categories)
admin.site.register(Post)