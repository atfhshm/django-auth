from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from users.models import User

admin.site.register(Permission)
@admin.register(User)
class UserAdminConfig(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "date_joined",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
    
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    ordering = ("email",)
