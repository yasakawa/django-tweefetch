from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now
from tweet.models import create_or_update_from_json
from ...models import SearchQuery, ListQuery
import tweepy
import traceback

TWITTER_CONSUMER_KEY = getattr(settings, "TWITTER_CONSUMER_KEY", None)
TWITTER_CONSUMER_SECRET = getattr(settings, "TWITTER_CONSUMER_SECRET", None)
TWITTER_OAUTH_TOKEN = getattr(settings, "TWITTER_OAUTH_TOKEN", None)
TWITTER_OAUTH_SECRET = getattr(settings, "TWITTER_OAUTH_SECRET", None)
TWITTER_MAX_API_RECURSION = getattr(settings, "TWITTER_MAX_API_RECURSION", 2)
MAX_STATUSES_PER_API = 100


def is_query_executable_for_interval(query):
    executable = None
    if query.last_fetched_at is None:
        executable = True
    elif query.last_fetched_at:
        delta = now() - query.last_fetched_at
        duration_secs = delta.total_seconds()
        executable = True if duration_secs >= query.fetch_interval_secs else False
    return executable


def recursive_fetch_statuses(api_func, query, max_recursion):
    new_max_fetched_id = None
    next_max_id = None
    api_executed_at = None
    fetched_statuses_count = 0

    i = 0
    while i < max_recursion:
        i += 1
        statuses = []

        # Generate Twitter API parameters
        params = query.query_params(
            count=MAX_STATUSES_PER_API,
            max_id=next_max_id,
            since_id=query.max_fetched_id,
        )

        # Execute Twitter API
        try:
            api_executed_at = now()
            statuses = api_func(**params)
        except Exception:
            # Save error message and exit function
            query.last_fetched_at = api_executed_at
            query.error = traceback.format_exc()
            query.save()
            return fetched_statuses_count

        # Process Twitter API results
        if len(statuses) == 0:
            break
        else:
            fetched_statuses_count += len(statuses)
            next_max_id = statuses[-1].id
            if not new_max_fetched_id:
                new_max_fetched_id = statuses[0].id

            # Save tweets and users
            for status in statuses:
                create_or_update_from_json(status._json, save_rts=query.save_rts)

    # Update query entry
    if new_max_fetched_id:
        query.max_fetched_id = new_max_fetched_id
    query.last_fetched_at = api_executed_at
    query.error = ""
    query.save()
    return fetched_statuses_count


def search(api, query):
    return recursive_fetch_statuses(
        api.search, query, max_recursion=TWITTER_MAX_API_RECURSION
    )


def list_timeline(api, query):
    return recursive_fetch_statuses(
        api.list_timeline, query, max_recursion=TWITTER_MAX_API_RECURSION
    )


class Command(BaseCommand):
    help = "Fetches tweets via search and list_timeline"

    def handle(self, *args, **options):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET)
        api = tweepy.API(auth)

        # SearchQuery
        search_queries = SearchQuery.objects.all()
        for query in search_queries:
            self.stdout.write("Start processing %s." % query)
            if is_query_executable_for_interval(query):
                fetched_count = search(api, query)
                self.stdout.write("Finished fetching %d tweets." % fetched_count)
            else:
                self.stdout.write(
                    "Skipping. The duration from last execution is less "
                    "than the defined interval (%d secs)." % (query.fetch_interval_secs)
                )

        # ListQuery
        list_queries = ListQuery.objects.all()
        for query in list_queries:
            self.stdout.write("Start processing %s." % query)
            if is_query_executable_for_interval(query):
                fetched_count = list_timeline(api, query)
                self.stdout.write("Finished fetching %d tweets." % fetched_count)
            else:
                self.stdout.write(
                    "Skipping. The duration from last execution is less "
                    "than the defined interval (%d secs)." % (query.fetch_interval_secs)
                )
