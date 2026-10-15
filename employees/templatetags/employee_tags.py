from django import template
register = template.Library()

@register.inclusion_tag("employees/includes/status_badge.html")
def status_badge(employee):
    return {"employee": employee}