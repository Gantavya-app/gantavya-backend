from django.contrib import admin
from .models import Photos, Landmark, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name')
    search_fields = ('username', 'email')
    list_filter = ('isAdmin',)

admin.site.register(User, UserAdmin)
admin.site.register(Photos)
admin.site.register(Landmark)

