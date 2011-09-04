# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
#from django.utils.safestring import mark_safe
#from django.utils.translation import ugettext_lazy as _

from cablegate.cable.models import Cable, CableMetadata


class CableMetadataInline(admin.StackedInline):
    model = CableMetadata


class CableAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'refid', 'classification', 'origin')
    list_filter = ('classification', 'origin')
    date_hierarchy = 'date'
    search_fields = ('content',)
    inlines = [CableMetadataInline]

admin.site.register(Cable, CableAdmin)
