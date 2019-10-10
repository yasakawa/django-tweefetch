from django.contrib import admin
from . import models


class SearchQueryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "q",
        "max_fetched_id",
        "last_fetched_at",
        "fetch_interval_secs",
        "error",
    )
    ordering = ["-updated_at"]
    fields = (
        "q",
        "geocode",
        "lang",
        "locale",
        "result_type",
        "include_entities",
        "fetch_interval_secs",
        "save_rts",
        "max_fetched_id",
        "last_fetched_at",
        "error",
    )


class ListQueryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "list_id",
        "slug",
        "owner_id",
        "owner_screen_name",
        "max_fetched_id",
        "last_fetched_at",
        "fetch_interval_secs",
        "error",
    )
    ordering = ["-updated_at"]
    fields = (
        "list_id",
        "slug",
        "owner_id",
        "owner_screen_name",
        "fetch_interval_secs",
        "save_rts",
        "max_fetched_id",
        "last_fetched_at",
        "error",
    )


admin.site.register(models.SearchQuery, SearchQueryAdmin)
admin.site.register(models.ListQuery, ListQueryAdmin)
