from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, Company


class MyUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
            (None, {'fields': ('email', 'first_name', 'last_name', 'gender', 'encodings', 'picture', 'attendance',
                               'notifications', 'role', 'username', 'is_staff', 'is_superuser', 'is_active')}),
    )


admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Role)
admin.site.register(Company)
