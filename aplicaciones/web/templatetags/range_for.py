from django import template
register = template.Library() 

@register.filter
def get_range(min,max):
    rango = range(min,max)
    return rango
