from django import template
import math

register = template.Library()

@register.filter
def display_nan(value):
    if value is None or (isinstance(value, float) and (math.isnan(value) or str(value) == "nan")):
        return "-"
    return value
