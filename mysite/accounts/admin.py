
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_tokens(modeladmin, request, queryset):
    """
    Admin action to generate JWT refresh and access tokens for selected users.
    """
    for user in queryset:
        refresh = RefreshToken.for_user(user)
        message = (
            f"Tokens for user: {user.username}<br>"
            f"<strong>Access Token:</strong> {str(refresh.access_token)}<br>"
            f"<strong>Refresh Token:</strong> {str(refresh)}"
        )
        messages.success(request, message)

generate_jwt_tokens.short_description = "Generate JWT tokens for selected users"


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    actions = [generate_jwt_tokens] # Add the custom action here

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
