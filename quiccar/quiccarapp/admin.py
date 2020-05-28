from django.contrib import admin
from .models import *

# Register your models here.
class PasswordResetAdmin (admin.ModelAdmin):
    readonly_fields = ('added',)

admin.site.register (Ride)
admin.site.register (Profile)
admin.site.register (PasswordReset, PasswordResetAdmin)
admin.site.register (EmailToken)