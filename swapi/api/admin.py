from django.contrib import admin

from api.models import People


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    pass
