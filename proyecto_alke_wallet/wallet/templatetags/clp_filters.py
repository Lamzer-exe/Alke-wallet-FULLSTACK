from django import template
register = template.Library()

@register.filter
def clp(value):
    try:
        return f"$ {int(value):,}".replace(',', '.')
    except Exception:
        return '$ 0'
