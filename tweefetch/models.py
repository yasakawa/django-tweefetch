from django.db import models


class BaseQuery(models.Model):
    class Meta:
        abstract = True

    # Timing parameters
    fetch_interval_secs = models.IntegerField("Fetch interval secs", default=600)

    # Store parameters
    save_rts = models.BooleanField("Save retweets", default=False)

    # Fetch results
    max_fetched_id = models.BigIntegerField(
        "Max fetched TweetID", null=True, blank=True
    )
    last_fetched_at = models.DateTimeField("Last fetched at", null=True, blank=True)
    error = models.TextField(
        "Error", help_text="When a problem occurs", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SearchQuery(BaseQuery):
    RESULT_TYPE_CHOICES = (
        ("mixed", "mixed"),
        ("recent", "recent"),
        ("popular", "popular"),
    )
    q = models.CharField("Query", max_length=500)
    geocode = models.CharField("Geocode", max_length=50, null=True, blank=True)
    lang = models.CharField("Lang", max_length=10, null=True, blank=True)
    locale = models.CharField("Locale", max_length=10, null=True, blank=True)
    result_type = models.CharField(
        "Result type", max_length=8, default="recent", choices=RESULT_TYPE_CHOICES
    )
    include_entities = models.BooleanField("Include entities", default=False)

    def query_params(self, count=None, max_id=None, since_id=None):
        params = {}
        if count:
            params["count"] = count
        if max_id:
            params["max_id"] = max_id
        if since_id:
            params["since_id"] = since_id

        params["q"] = self.q
        params["result_type"] = self.result_type
        params["include_entities"] = self.include_entities
        if self.geocode:
            params["geocode"] = self.geocode
        if self.lang:
            params["lang"] = self.lang
        if self.locale:
            params["locale"] = self.locale

        return params

    def __str__(self):
        return "SearchQuery(q=%s, geocode=%s, lang=%s, locale=%s, result_type=%s)" % (
            self.q,
            self.geocode,
            self.lang,
            self.locale,
            self.result_type,
        )


class ListQuery(BaseQuery):
    list_id = models.BigIntegerField("List ID", null=True, blank=True)
    slug = models.CharField("Slug", max_length=30, null=True, blank=True)
    owner_id = models.BigIntegerField("Owner ID", null=True, blank=True)
    owner_screen_name = models.CharField(
        "Owner screen name", max_length=50, null=True, blank=True
    )

    def query_params(self, count=None, max_id=None, since_id=None):
        """ Generate Twitter API parameters for list_timeline """
        params = {}
        if count:
            params["count"] = count
        if max_id:
            params["max_id"] = max_id
        if since_id:
            params["since_id"] = since_id

        if self.list_id:
            params["list_id"] = self.list_id
        elif self.slug and self.owner_id:
            params["slug"] = self.slug
            params["owner_id"] = self.owner_id
        elif self.slug and self.owner_screen_name:
            params["slug"] = self.slug
            params["owner_screen_name"] = self.owner_screen_name

        return params

    def __str__(self):
        return "ListQuery(list_id=%s, slug=%s, owner_id=%s, owner_screen_name=%s)" % (
            self.list_id,
            self.slug,
            self.owner_id,
            self.owner_screen_name,
        )
