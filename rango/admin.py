from django.contrib import admin
from rango.models import Category, Page

# Register your models here.

# Page model
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
admin.site.register(Page, PageAdmin)

# Category model
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)
