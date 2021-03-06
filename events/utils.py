from datetime import datetime

from django.conf import settings
from django.db.models import Q


def filter_events(request, queryset):
    if "start" in request.GET and "end" in request.GET:
        start = datetime.fromtimestamp(int(request.GET["start"]))
        end = datetime.fromtimestamp(int(request.GET["end"]))
        q_object = Q(start__gte=start, start__lt=end)
        q_object = q_object | Q(end__isnull=False, end__gte=start, end__lt=end)
        q_object = q_object | Q(start__lt=start, end__gt=end)

        queryset = queryset.filter(q_object)

    section = request.GET.get("section")
    if section:
        source = settings.PREDEFINED_FILTERS[section]["source"]
        exclude_source = settings.PREDEFINED_FILTERS[section]["exclude_source"]
        tag = settings.PREDEFINED_FILTERS[section]["tag"]
        exclude_tag = settings.PREDEFINED_FILTERS[section]["exclude_tag"]
    else:
        source = request.GET.getlist("source")
        exclude_source = request.GET.getlist("exclude_source")
        tag = request.GET.getlist("tag")
        exclude_tag = request.GET.getlist("exclude_tag")

    if source:
        queryset = queryset.filter(source__in=source)

    if exclude_source:
        queryset = queryset.exclude(source__in=exclude_source)

    if tag:
        queryset = queryset.filter(tags__name__in=tag)

    if exclude_tag:
        queryset = queryset.exclude(tags__name__in=exclude_tag)

    return queryset
