from django import template
import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Mengambil value dari dictionary menggunakan key variabel"""
    return dictionary.get(key)

@register.filter
def format_waktu(seconds):
    """Mengubah detik (int) menjadi string HH:MM:SS"""
    if seconds is None:
        return "-"
    try:
        seconds = int(seconds)
        return str(datetime.timedelta(seconds=seconds))
    except (ValueError, TypeError):
        return "-"