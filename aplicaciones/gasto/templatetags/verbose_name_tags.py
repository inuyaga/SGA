# verbose_name_tags.py

from django import template

register = template.Library()

@register.filter
def get_field_verbose_name(instance, arg):
    return instance._meta.get_field(arg).verbose_name

@register.filter
def get_queryset_field_verbose_name(queryset, arg):
    return queryset.model._meta.get_field(arg).verbose_name


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


