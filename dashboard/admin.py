from django.contrib import admin
from .models import Uploads
# Register your models here.

class UploadsAdmin(admin.ModelAdmin):
	model = Uploads
	list_display = ['title','file']


admin.site.register(Uploads,UploadsAdmin)