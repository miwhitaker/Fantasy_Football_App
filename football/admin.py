from django.contrib import admin
from .models import Players

class FantasyAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'position')

admin.site.register(Players, FantasyAdmin)