from django.contrib import admin
from mnemosyne.models import Memory

class MemoryAdmin(admin.ModelAdmin):
	pass

admin.site.register(Memory, MemoryAdmin)
