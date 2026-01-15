from django import template
from django.utils.timezone import now

register = template.Library()

@register.filter
def custom_time_since(since_date):
    """returns shorter values time_since like"""

    if not since_date:
        return ""
    
    difference = now() - since_date
    seconds = int(difference.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    weeks = days // 7
    months = days // 30
    if months < 1:
        months = 1
    years = days // 365

    if seconds < 60:
        return f"Ahora mismo"
    
    if minutes < 60:
        return f'hace {minutes} min'
    
    if hours < 24:
        return f'hace {hours} h'
    
    if days < 7:
        return f'hace {days} d'
    
    if weeks <= 4:
        return f'hace {weeks} sem'
    
    if months < 12:
        return f'hace {months} m'
    
    else:
        return f'hace {years} a'
    


