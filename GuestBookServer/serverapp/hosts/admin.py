# Copyright Mark B. Skouson, 2019
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# from .models import Host
from .models import Event, User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active', )
    list_filter = ('email', 'is_staff', 'is_active', )
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields =('email',)
    ordering = ('email',)


class EventsInLine(admin.TabularInline):
    model = Event
    extra = 0


class HostAdmin(admin.ModelAdmin):
    inlines = [ EventsInLine ]


admin.site.register(User, HostAdmin)



