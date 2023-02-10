from django.contrib import admin

from .models import Profile, ProfileItem


class ProfileItemInline(admin.TabularInline):
    model = ProfileItem
    autocomplete_fields = ("item",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (ProfileItemInline,)
    list_display = ("user",)
    search_fields = ("user",)
